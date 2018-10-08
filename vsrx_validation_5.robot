# CHANGES: Added new tests to push configuration and verify result. Added new variable.

*** Settings ***
Library          JunosDevice.py
Library          Collections
Test Setup       Setup Actions
Test Teardown    Teardown Actions


*** Variables ***
&{login_opts}  login_mode=netconf  login_target=172.16.198.31  login_user=root  login_password=juniper1
&{config_options}  format=set  action=merge  configuration=set system host-name new_hostname

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

Log Tests
    @{returned_dev_info}=  Get Device Info
    Log  ${returned_dev_info}
    Log  ${returned_dev_info[0]}
    Log  ${returned_dev_info[1]}
    Log  ${returned_dev_info[1]["device_model"]}
    Log  ${returned_dev_info[1]["device_sn"]}

Verify New Hostname
    [Documentation]  First change the hostname and then validate the new hostname.
    Set Config Opts  ${config_options}
    Post Configuration
    ${returned_os_version}=  Get Device Info
    Should Be Equal As Strings  ${returned_os_version[1]["hostname"]}  new_hostname


