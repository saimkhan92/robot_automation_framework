*** Settings ***
Library	JunosDevice.py
Test Setup  Setup Actions
Test Teardown   Teardown Actions

*** Keywords ***
Setup Actions
    Log     Setup Actions done here
    Connect Device  host=${HOST}	user=${USER}	password=${PASSWORD}

Teardown Actions
    Log    Teardown Actions done here
    Close Device

Validate Facts
	&{facts}=	Gather Device Info
    Should Be Equal As Strings  ${facts["hostname"]}  vsrx-robot
    Should Be Equal As Strings  ${facts["model"]}  VSRX

*** Test Cases ***
Verify Facts
	Validate Facts