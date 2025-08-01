# variables/browser_options.py
from selenium.webdriver.chrome.options import Options
import os
import tempfile
import shutil

import atexit
# Khởi tạo biến global ngay từ đầu với giá trị None
# Điều này đảm bảo chúng luôn được định nghĩa, ngay cả khi hàm tạo profile chưa được gọi.
_temp_user_data_dir  = None
_temp_firefox_user_data_dir = None


def get_chrome_options_object():
    
    # --- Thêm logic tạo thư mục user data tạm thời ---
    global _temp_user_data_dir
    # Luôn tạo một thư mục tạm thời MỚI nếu chưa có,
    # hoặc nếu nó đã tồn tại từ lần chạy trước nhưng không được dọn dẹp
    # (Đây là một biện pháp an toàn để tránh lỗi "already in use")
    if _temp_user_data_dir and os.path.exists(_temp_user_data_dir):
        # Nếu thư mục cũ vẫn tồn tại (do lỗi dọn dẹp trước đó), hãy thử xóa nó
        try:
            _cleanup_temp_dir_function()
        except Exception as e:
            print(f"Warning: Could not cleanup stale temp directory {_temp_user_data_dir}: {e}")
            _temp_user_data_dir = None # Đặt lại để tạo cái mới

    if not _temp_user_data_dir:
        _temp_user_data_dir = tempfile.mkdtemp(prefix="chrome_profile_") # Thêm prefix cho dễ nhận biết
        atexit.register(_cleanup_temp_dir_function) # Đăng ký hàm dọn dẹp
    
    
    # ----------------------------------------------------
    
    
    
    options = Options()
    # chạy chế độ khách
    options.add_argument('--headless')
    options.add_argument(f"--user-data-dir={_temp_user_data_dir}")
    
    
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
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_settings.popups": 0,
        "profile.default_content_setting_values.notifications": 2
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    return options


# Hàm nội bộ để dọn dẹp thư mục tạm thời
def _cleanup_temp_dir_function():
    global _temp_user_data_dir
    if _temp_user_data_dir and os.path.exists(_temp_user_data_dir):
        # Log để biết khi nào dọn dẹp được gọi
        print(f"Attempting to cleanup temporary user data directory: {_temp_user_data_dir}")
        try:
            shutil.rmtree(_temp_user_data_dir)
            print(f"Successfully cleaned up temporary user data directory: {_temp_user_data_dir}")
        except Exception as e:
            # Ghi lại lỗi nếu không xóa được
            print(f"ERROR: Could not cleanup temp directory {_temp_user_data_dir}: {e}")
            # Để nguyên _temp_user_data_dir nếu xóa thất bại để có thể điều tra
        # finally: # Không nên đặt _temp_user_data_dir = None ở đây nếu xóa thất bại
            # _temp_user_data_dir = None 
            
def cleanup_temp_chrome_user_data_directory():
    """
    Cleans up the temporary Chrome user data directory created by get_chrome_options().
    This function should be called in a Robot Framework Teardown.
    """
    _cleanup_temp_dir_function()
            
            
# Hàm get_variables() mà Robot Framework sẽ gọi để lấy các biến động
# def get_variables():
#     return {
#         "OPTIONS": get_chrome_options(),
#         "CLEANUSERDATA": cleanup_temp_chrome_user_data_directory(),
#     }