*** Settings ***
Library	substring.py

*** Test Cases ***
CheckSubstring1
	is a substring  Jun		Juniper

CheckSubstring2
	is a substring  June	Juniper
