*** Settings ***
Library	JunosDevice.py

*** Test Cases ***
Get Facts
	Connect Device  host=${HOST}  user=${USER}  password=${PASSWORD}
	&{facts}=	Gather Facts
        Log	${facts}
	Close Device

