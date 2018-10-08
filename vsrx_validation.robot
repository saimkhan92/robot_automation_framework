*** Settings ***
Library  JunosDevice.py


*** Test Cases ***
Verify OS Version
    &{login_opts}=  Create Dictionary  login_mode=netconf  login_target=172.16.198.31  login_user=root  login_password=juniper1
    Set Login Opts  ${login_opts}
    Connect
    ${returned_os_version} =  Get OS Version
    Close Connection
    Should Be Equal As Strings  ${returned_os_version}  18.2R1.9