# variables/browser_options.py
from selenium.webdriver.chrome.options import Options
import os
def get_chrome_options():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--safebrowsing-disable-download-protection')
    options.add_argument("--no-sandbox") 
    options.add_argument("--start-maximized") 
    options.add_argument("--disable-dev-shm-usage") 
    options.add_argument("--disable-web-security")
    options.add_argument('disable-infobars')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument('ignore-certificate-errors') ## fixx ssl
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    # options.add_argument("--allow-running-insecure-content")
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.notifications": 2
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    #  # Tạo thư mục người dùng tạm thời
    # # Lấy thư mục tạm thời của hệ thống
    # temp_dir = os.path.join(os.getenv('JENKINS_HOME', '/tmp'), 'chrome_profile_jenkins')
    # if not os.path.exists(temp_dir):
    #     os.makedirs(temp_dir)

    # Nếu muốn tạo thư mục duy nhất cho mỗi lần chạy (tốt hơn)
    # import tempfile
    # temp_user_data_dir = tempfile.mkdtemp(prefix='chrome_profile_')
    # print(f"Using temporary user data directory: {temp_user_data_dir}")
    # options.add_argument(f"--user-data-dir={temp_user_data_dir}")

    # Ở đây tôi sẽ sử dụng một cách đơn giản hơn, tạo thư mục tạm trong workspace của Jenkins
    # Đảm bảo bạn dọn dẹp thư mục này sau khi test (thông qua Robot Framework Teardown)
    jenkins_workspace = os.getenv('WORKSPACE')
    if jenkins_workspace:
        # Tạo thư mục con trong workspace cho profile user data
        user_data_dir = os.path.join(jenkins_workspace, 'chrome_user_data')
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        print(f"Using Chrome user data directory in workspace: {user_data_dir}")
    else:
        print("WARNING: WORKSPACE environment variable not found. Using default temp dir for Chrome profile.")
        options.add_argument("--user-data-dir=/tmp/chrome_profile_default") # Fallback
    return options


# Hàm get_variables() mà Robot Framework sẽ gọi để lấy các biến động
def get_variables():
    return {
        "OPTIONS": get_chrome_options()
    }