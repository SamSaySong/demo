** Settings ***
Library    SeleniumLibrary
Variables    ../variables/data_reader.py

*** Variables ***
${USERNAME_LOCATOR}  id=username
${PASSWORD_LOCATOR}  id=password

${LOGIN_BUTTON_LOCATOR}  xpath=//*[@id="login"]/button

${BROWSER}  Chrome
${URL}  https://the-internet.herokuapp.com/login

${USERNAME}  tomsmith
${PASSWORD}  SuperSecretPassword!

${MESSAGE}  id=flash

# Locators for Product Page
${PRODUCT_TITLE_LOCATOR}  xpath=//*[@data-test='title']

***Keywords***
Login To Application 
    [Arguments]  ${username}  ${password}
 
    Input Text  ${USERNAME_LOCATOR}  ${username}
    Input Text  ${PASSWORD_LOCATOR}  ${password}
    Click Element  ${LOGIN_BUTTON_LOCATOR}
    Sleep  2s


Logout To Application
    Wait Until Element Is Visible    id:react-burger-menu-btn    5s
    Click Element  id:react-burger-menu-btn
    Wait Until Element Is Visible    id:logout_sidebar_link    5s
    Click Element  id:logout_sidebar_link
    Sleep  1s
        
    
