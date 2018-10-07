# CHANGES: Addied multiple tests. Demonstrated dictionary and list manipulation.

# ${returned_os_version} = 
# (
#     True,
#     {
#         "login_mode": "netconf",
#         "login_target": "172.16.198.31",
#         "login_user": "root",
#         "login_password": "juniper1",
#         "online": True,
#         "connected_at": "2018-10-07T22:56:50.429086Z",
#         "os_version": "18.2R1.9",
#         "device_model": "vSRX",
#         "hostname": "dcsmgrtest",
#         "device_sn": "93c207bfd0dd",
#         "connected_diff": "now",
#         "os_name": "junos",
#     },
# )


*** Settings ***
Library          JunosDevice.py
Library          Collections
Test Setup       Setup Actions
Test Teardown    Teardown Actions


*** Variables ***
&{login_opts}  login_mode=netconf  login_target=172.16.198.31  login_user=root  login_password=juniper1


*** Keywords ***
Setup Actions
    Log    Setup Actions done here
    Set Login Opts  ${login_opts}
    Connect
Teardown Actions
    Log    Teardown Actions done here
    Close Connection


*** Test Cases ***
Verify OS Version
    ${returned_os_version}=  Get OS Version
    Should Be Equal As Strings  ${returned_os_version}  18.2R1.9

Log Device Info
    @{returned_dev_info}=  Get Device Info
    Log  ${returned_dev_info}
    :FOR  ${value}  IN  @{returned_dev_info[1].values()}  
    \  Log  ${value}

Log tests
    @{returned_dev_info}=  Get Device Info
    Log  ${returned_dev_info}
    Log  ${returned_dev_info[0]}
    Log  ${returned_dev_info[1]}
    Log  ${returned_dev_info[1]["device_model"]}
    Log  ${returned_dev_info[1]["device_sn"]}

Verify Device hostname
    ${returned_os_version}=  Get Device Info
    Should Be Equal As Strings  ${returned_os_version[1]["hostname"]}  dcsmgrtest