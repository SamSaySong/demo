***Settings***
Library    SeleniumLibrary
Variables    ../variables/browser_options.py

*** Variables ***

${BROWSER}  Chrome

${URL}  https://the-internet.herokuapp.com/login

${SEARCH_TEXT}  Robot Framework Tutorial
${SEARCH_INPUT_LOCATOR}  xpath = //*[@id="APjFqb"]
${SEARCH_BUTTON_LOCATOR}  xpath = /html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]

***Test Cases***
Verify Google Search Functionality
    [Documentation]  This is my first test case
    ${chrome_options_object}=    Evaluate    browser_options.get_chrome_options()    browser_options

    Open Browser  ${URL}    ${BROWSER}    options=${chrome_options_object}
    Click Element  ${SEARCH_INPUT_LOCATOR}
    Input Text  ${SEARCH_INPUT_LOCATOR}  ${SEARCH_TEXT} 
    Click Element  xpath= /html/body/div[1]/div[2]/div
    Click Button  ${SEARCH_BUTTON_LOCATOR}
    Sleep  5s
    Page Should Contain  Robot Framework Tutorial
    Log To Console  Search completed successfully!
    [Teardown]  Close Browser

Verify Successful Login
    [Documentation]  This test case verifies successful login functionality
    Open Browser  ${URL}  ${BROWSER}
  

