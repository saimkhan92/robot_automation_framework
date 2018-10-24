*** Settings ***
Library	JunosDevice_Stage1.py

*** Test Cases ***
Check OS Version
	@{os_version}= 	Get OS Version
	Should Be Equal As Strings  ${os_version}  18.2R1.9
