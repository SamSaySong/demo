***Settings***
Library    SeleniumLibrary
Resource    common_keywords.robot
Variables    variables/data_reader.py
Variables    variables/browser_options.py

***Test Cases***
Verify Successful Login
    [Documentation]  This test case verifies successful login functionality
    # ${GET_OPTIONS}=    Get Chrome Options
    Open Browser  ${URL}  ${BROWSER}    options=${OPTIONS}
    Login To Application    ${USERNAME}    ${PASSWORD}
    ${welcome_text}=    Get Text    ${MESSAGE}
    Log To Console  ${welcome_text}
    Element Should Contain  ${MESSAGE}  You logged into a secure area!
    # Page Should Contain  You logged into a secure area!s
    [Teardown]  Close Browser

Verify Unsuccessful Login
    [Documentation]  This test case verifies unsuccessful login functionality
    # ${GET_OPTIONS}=    Get Chrome Options

    Open Browser  ${URL}  ${BROWSER}    options=${OPTIONS}

    Login To Application    ${USERNAME}    ${PASSWORD}
    # ${welcome_text}=    Get Text    ${MESSAGE}
    # Log To Console  ${welcome_text}
    Click Element    xpath=//*[@id="content"]/div/a
    Element Should Contain  ${MESSAGE}  You logged out of the secure area!
    # Page Should Contain  You logged into a secure area!
    [Teardown]  Close Browser 