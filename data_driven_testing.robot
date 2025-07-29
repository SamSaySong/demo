***Settings***
Library    SeleniumLibrary
Variables    ../variables/data_reader.py
Variables    ../variables/browser_options.py
Resource    ../common_keywords.robot



*** Test Cases ***
Verify Login With Data From Excel
    [Documentation]  This test case verifies login functionality using data from Excel
    Open Browser  ${URL}  ${BROWSER}    options=${OPTIONS}
    FOR  ${user}  IN  @{ROBOT_USERS_PANDAS}
        Login To Application    ${user['username']}    ${user['password']}
        # ${welcome_text}=    Get Text    ${MESSAGE}
        # Log To Console  ${welcome_text}
        ${actual_message}=    Run Keyword And Return Status    Element Should Contain    ${PRODUCT_TITLE_LOCATOR}     Products
        IF    ${actual_message}
            Log To Console    Đăng nhập thành công với ${user['username']}
            Logout To Application
        ELSE
            ${error_text}=    Get Text    ${MESSAGE}
            Log To Console    Đăng nhập thất bại: ${error_text}
            Should Contain    ${error_text}    ${user['expected_message']} 
            Reload Page
        END
    END
    [Teardown]  Close Browser