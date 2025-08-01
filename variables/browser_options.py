# variables/browser_options.py
from selenium.webdriver.chrome.options import Options
import os
import tempfile
import shutil
# Khởi tạo biến global ngay từ đầu với giá trị None
# Điều này đảm bảo chúng luôn được định nghĩa, ngay cả khi hàm tạo profile chưa được gọi.
_temp_chrome_user_data_dir = None
_temp_firefox_user_data_dir = None


def get_chrome_options_object():
    options = Options()
    # chạy chế độ khách
    options.add_argument('--headless')
    
    
    # options.add_argument('--guest')
    
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
    options.add_argument("--allow-running-insecure-content")
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    # --- Thêm logic tạo thư mục user data tạm thời ---
    _temp_chrome_user_data_dir = tempfile.mkdtemp(prefix='chrome_profile_jenkins_')
    print(f"Using unique temporary Chrome user data directory: {_temp_chrome_user_data_dir}")
    options.add_argument(f"--user-data-dir={_temp_chrome_user_data_dir}")
    # ----------------------------------------------------
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.notifications": 2
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    return options

def cleanup_temp_chrome_user_data_directory():
    """
    Cleans up the temporary Chrome user data directory created by get_chrome_options().
    This function should be called in a Robot Framework Teardown.
    """
    global _temp_chrome_user_data_dir
    if _temp_chrome_user_data_dir and os.path.exists(_temp_chrome_user_data_dir):
        print(f"Cleaning up temporary Chrome user data directory: {_temp_chrome_user_data_dir}")
        try:
            shutil.rmtree(_temp_chrome_user_data_dir)
            print(f"Successfully removed directory: {_temp_chrome_user_data_dir}")
        except OSError as e:
            print(f"Error removing directory {_temp_chrome_user_data_dir}: {e}")
        finally:
            _temp_chrome_user_data_dir = None # Reset biến sau khi xóa
            
            
# Hàm get_variables() mà Robot Framework sẽ gọi để lấy các biến động
# def get_variables():
#     return {
#         "OPTIONS": get_chrome_options(),
#         "CLEANUSERDATA": cleanup_temp_chrome_user_data_directory(),
#     }