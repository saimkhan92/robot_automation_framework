import logging
import maya
import humanize
import re
from jnpr.junos import Device
from jnpr.junos.exception import (
    ConnectAuthError,
    ConnectRefusedError,
    ConnectTimeoutError,
    ConnectError,
)
from jnpr.junos.exception import LockError, UnlockError, ConfigLoadError, CommitError
from jnpr.junos.utils.config import Config
from lxml.etree import tostring

logger = logging.getLogger(__name__)


class JunosDevice(object):
    """Worker class for performing all Junos operations using PyEZ library."""

    def __init__(self):
        self.device_info = {}
        self.login_at = None
        self.login_opts = {}
        self.device = None
        self.config_opts = {}
        self.device_config = {}

    def is_busy(self):
        if self.device == None:
            return False
        return True

    def set_config_opts(self, config_opts):
        self.config_opts.update(config_opts)

    def set_login_opts(self, login_opts):
        self.login_opts.update(login_opts)

    def get_device_info(self):

        try:
            self._retrieve_dev_info()
        except Exception as exc:
            return False, f"Unspecific Error while getting device information: {exc}"

        login_diff = maya.now() - self.login_at
        self.device_info["connected_diff"] = humanize.naturaltime(login_diff)
        self.device_info["os_name"] = "junos"
        return (True, self.device_info)

    def get_os_version(self):
        response = self.get_device_info()
        logger.info(response)
        return response[1]["os_version"]

    def _retrieve_dev_info(self):
        self.login_at = maya.now()
        self.device_info["online"] = True
        self.device_info["connected_at"] = self.login_at.iso8601()
        device_info = self.device_info

        logger.info("Pulling device information")

        show_version_response = self.device.rpc.cli("show version", format="xml")
        show_hardware_response = self.device.rpc.cli(
            "show chassis hardware", format="xml"
        )

        device_info["os_version"] = show_version_response.findtext(".//junos-version")

        # there are older versions of Junos that do not support the junos-version XML tag,
        # so therefore need to check for this, and find the value from the "junos" package element

        if not device_info["os_version"]:

            pkg = show_version_response.xpath(
                './/package-information[name="junos"]/comment'
            )

            if not pkg:
                # TODO then we have a real propblem, and should handle accordingly
                # return False, "Unable to find Junos OS version string"
                raise Exception("Unable to find Junos OS version string")

            # use the comment string content so we can regex process it.  Example
            # comment string looks like this: 'JUNOS EX  Software Suite [13.2X50-D15.3]'
            # so match on content within the brackets that are at the end of the string

            content = pkg[0].text
            found = re.search(r"\[(.*)\]$", content)
            if not found:
                raise Exception("Unable to extract version from string: %s" % content)

            device_info["os_version"] = found.group(1)

        device_info["device_model"] = show_version_response.findtext(".//product-model")
        device_info["hostname"] = show_version_response.findtext(".//host-name")
        device_info["device_sn"] = show_hardware_response.findtext(".//serial-number")

        login_diff = maya.now() - self.login_at
        self.device_info["connected_diff"] = humanize.naturaltime(login_diff)

    def close_connection(self):
        self.device.close()
        self.device = None
        logger.info("Connection closed")

    def get_configuration(self):
        logger.info("Getting configuration")
        try:
            retrieved_configuration = self.device.rpc.get_config()
        except Exception as exc:
            return (False, f"Unspecific Error while getting configuration: {exc}")
        self.device_config["configuration"] = tostring(
            retrieved_configuration, encoding="unicode"
        )
        return (True, self.device_config)

    def post_configuration(self):
        try:
            config_opts = self.config_opts

            kwargs = {}
            if config_opts["action"]:
                kwargs[config_opts["action"]] = True
            logger.info("Locking the configuration")

            with Config(self.device, mode="private") as cu:

                logger.info("Loading configuration changes")

                cu.load(
                    config_opts["configuration"], format=config_opts["format"], **kwargs
                )

                diff = cu.diff()

                if bool(diff):
                    self.device_config["configuration_difference"] = diff
                else:
                    self.device_config["configuration_difference"] = None
                logger.info(f"diff: {diff}")

                logger.info("Committing configuration")
                cu.commit(comment="Loaded by DCS-CI-Junos")

        except LockError as err:
            return (False, f"Unable to lock configuration: LockError")
        except (ConfigLoadError) as err:
            return (
                False,
                "Unable to load configuration changes. Unlocking the configuration: ConfigLoadError",
            )
        except UnlockError:
            return (False, f"Configuration load error: UnlockError")
        except CommitError as err:
            return (False, f"Unable to commit configuration: CommitError")
        except Exception as exc:
            return (False, f"Unspecific Error posting configuration: {exc}")
        return (True, self.device_config)

    def connect(self):
        logger.info("Entering connect function")
        login_opts = self.login_opts
        self.device_info.update(login_opts)

        logger.info("Trying to connect")

        # Only telnet and serial values can be passed directly to mode.
        # In case of ssh, mode needs to be passed as a null string.
        # PyEZ does not yet support termserv-ssh. As per a recent PR,support
        # coming very soon.

        if login_opts["login_mode"] == "netconf":
            self.device = Device(
                host=login_opts["login_target"],
                user=login_opts["login_user"],
                password=login_opts["login_password"],
            )
        else:
            self.device = Device(
                host=login_opts["login_target"],
                user=login_opts["login_user"],
                password=login_opts["login_password"],
                mode=login_opts["login_mode"],
                port=login_opts["login_port"],
            )
        try:
            self.device.open()
            logger.info(self.device)

            return (True, "Connection to device opened")
        except ConnectAuthError as exc:
            return (False, "Authentication error: ConnectAuthError")
        except ConnectRefusedError as exc:
            return (
                False,
                "The device does not have NETCONF enabled: ConnectRefusedError",
            )
        except ConnectTimeoutError as exc:
            return (False, "Timeout value exceeded: ConnectTimeoutError")
        except ConnectError as exc:
            return (False, "Connect Error: ConnectError")
        except RuntimeError as exc:
            return (False, "Runtime Error: RuntimeError")
        except Exception as exc:
            return (False, f"Unspecific Error while opening device connection: {exc}")


a = (
    True,
    {
        "login_mode": "netconf",
        "login_target": "172.16.198.31",
        "login_user": "root",
        "login_password": "juniper1",
        "online": True,
        "connected_at": "2018-10-07T22:56:50.429086Z",
        "os_version": "18.2R1.9",
        "device_model": "vSRX",
        "hostname": "dcsmgrtest",
        "device_sn": "93c207bfd0dd",
        "connected_diff": "now",
        "os_name": "junos",
    },
)

