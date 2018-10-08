# CHANGES: Created two new keywords for setup and teardown. Used the self created
# keywords for centralized setup and teardown in the settings section after every test run.

*** Keywords ***
Setup Actions
    Log    Setup Actions done here
    Set Login Opts  ${login_opts}
    Connect

Teardown Actions
    Log    Teardown Actions done here
    Close Connection


*** Settings ***
Library           JunosDevice.py
Test Setup       Setup Actions
Test Teardown    Teardown Actions


*** Variables ***
&{login_opts}  login_mode=netconf  login_target=172.16.198.31  login_user=root  login_password=juniper1


*** Test Cases ***
Verify OS Version
    ${returned_os_version}=  Get OS Version
    Should Be Equal As Strings  ${returned_os_version}  18.2R1.9