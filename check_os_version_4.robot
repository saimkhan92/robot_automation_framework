# CHANGES: Adding new tests

*** Settings ***
Library           JunosDevice.py
Suite Setup       Setup Actions
Suite Teardown    Teardown Actions


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


Verify Device Model
    ${returned_dev_info}=  Get Device Info
    Log    Teardown Actions done here