***Settings***
Library    SeleniumLibrary
Resource    common_keywords.robot
Variables    variables/data_reader.py
Library    variables/browser_options.py
Test Setup    Setup test demo
Test Teardown    Clear and Quit Browser


***Test Cases***
Verify Successful Login
    [Documentation]  This test case verifies successful login functionality
    # ${GET_OPTIONS}=    Get Chrome Options
    # Open Browser  ${URL}  ${BROWSER}    ${GET_OPTIONS}
    Login To Application    ${USERNAME}    ${PASSWORD}
    
    ${welcome_text}=    Get Text    ${MESSAGE}
    Log To Console  ${welcome_text}
    Element Should Contain  ${MESSAGE}  You logged into a secure area!
    # Page Should Contain  You logged into a secure area!s
    # [Teardown]  Clear and Quit Browser

Verify Unsuccessful Login
    [Documentation]  This test case verifies unsuccessful login functionality
    # [Setup]  Setup test demo
    # ${GET_OPTIONS}=    Get Chrome Options

    # Open Browser  ${URL}  ${BROWSER}    options=${GET_OPTIONS}

    Login To Application    ${USERNAME}    ${PASSWORD}
    # ${welcome_text}=    Get Text    ${MESSAGE}
    # Log To Console  ${welcome_text}
    Click Element    xpath=//*[@id="content"]/div/a
    Element Should Contain  ${MESSAGE}  You logged out of the secure area!
    # Page Should Contain  You logged into a secure area!
    # [Teardown]  Clear and Quit Browser



*** Keywords ***
Clear and Quit Browser
    Close Browser    
    Cleanup Temp Chrome User Data Directory

Setup test demo
    ${CHROME_OPTIONS_OBJECT}=    Get Chrome Options Object
    Open Browser    ${URL}    ${BROWSER}    options=${CHROME_OPTIONS_OBJECT}
   
    