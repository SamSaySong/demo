***Settings***
Library    SeleniumLibrary
Resource    common_keywords.robot
Variables    ../variables/data_reader.py




***Test Cases***
Verify Successful Login
    [Documentation]  This test case verifies successful login functionality
    Open Browser  ${URL}  ${BROWSER}
    Login To Application    ${USERNAME}    ${PASSWORD}
    ${welcome_text}=    Get Text    ${MESSAGE}
    Log To Console  ${welcome_text}
    Element Should Contain  ${MESSAGE}  You logged into a secure area!
    # Page Should Contain  You logged into a secure area!
    [Teardown]  Close Browser

Verify Unsuccessful Login
    [Documentation]  This test case verifies unsuccessful login functionality
    Open Browser  ${URL}  ${BROWSER}
    Login To Application    ${USERNAME}    ${PASSWORD}
    ${welcome_text}=    Get Text    ${MESSAGE}
    Log To Console  ${welcome_text}
    Element Should Contain  ${MESSAGE}  Your username is invalid!
    # Page Should Contain  You logged into a secure area!
    [Teardown]  Close Browser 


