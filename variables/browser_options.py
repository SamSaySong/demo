from selenium.webdriver.chrome.options import Options
import os
import shutil
import tempfile
import atexit

_temp_user_data_dir = None

def get_chrome_options_object():
    """
    Tạo và trả về một đối tượng ChromeOptions đã cấu hình mạnh mẽ
    để tắt popup lưu mật khẩu và các thông báo khác,
    đặc biệt khi chạy headless trên Linux.
    """
    global _temp_user_data_dir

    # Logic dọn dẹp thư mục tạm thời cũ (giữ nguyên)
    if _temp_user_data_dir and os.path.exists(_temp_user_data_dir):
        try:
            _cleanup_temp_dir_function()
        except Exception as e:
            print(f"Warning: Could not cleanup stale temp directory {_temp_user_data_dir}: {e}")
            _temp_user_data_dir = None

    if not _temp_user_data_dir:
        _temp_user_data_dir = tempfile.mkdtemp(prefix="chrome_profile_")
        atexit.register(_cleanup_temp_dir_function)
        print(f"Created temporary user data directory: {_temp_user_data_dir}")

    options = Options()
    
    # -------------------------------------------------------------
    # Cấu hình Chrome Arguments - Quan trọng cho Headless & Tắt Popup
    # -------------------------------------------------------------
    
    # Kích hoạt chế độ headless MỚI (Chrome 109+) - Cần thiết cho headless
    options.add_argument("--headless=new") 
    # options.add_argument("--incognito") 
    # options.add_argument("--guest") # Chế độ khách, không cần đăng nhập
    
    
    # QUAN TRỌNG: Đảm bảo profile sạch cho mỗi lần chạy
    # Đây là nền tảng để các prefs liên quan đến mật khẩu có hiệu lực.
    options.add_argument(f"--user-data-dir={_temp_user_data_dir}")

    # Cấu hình môi trường headless trên Linux
    options.add_argument("--no-sandbox") # Bắt buộc cho Linux và môi trường container
    options.add_argument("--disable-dev-shm-usage") # Giảm yêu cầu về /dev/shm, quan trọng cho môi trường hạn chế
    options.add_argument("--disable-gpu") # Rất quan trọng cho headless trên Linux, tránh lỗi render

    # Kích thước cửa sổ và tối đa hóa (đảm bảo hiển thị đầy đủ các phần tử)
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized") 

    # Các tùy chọn vô hiệu hóa và khắc phục sự cố chung
    options.add_argument("--disable-extensions") # Tắt tất cả các extension
    options.add_argument("--disable-infobars") # Tắt các thanh thông tin "Chrome is being controlled by automated test software"
    options.add_argument("--disable-web-security") # Có thể cần cho một số trang có CORS
    options.add_argument("--disable-popup-blocking") # Tắt popup blocker
    options.add_argument("--disable-notifications") # Tắt thông báo cấp trình duyệt (ví dụ: "Do you want to allow notifications?")
    
    # Tùy chọn SSL/TLS
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--allow-running-insecure-content")

    # Arguments để ẩn dấu hiệu tự động hóa (rất quan trọng để tránh bị phát hiện là bot)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36") # Cập nhật lên Chrome 137+ của bạn nếu có
    # Ví dụ User-Agent cho Chrome 137 (bạn có thể tìm trên trang chrome://version/ của mình)
    # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36")


    # -------------------------------------------------------------
    # Cấu hình Experimental Options (prefs và excludeSwitches) - Cốt lõi để tắt Popup
    # -------------------------------------------------------------

    # Prefs để tắt hoàn toàn quản lý mật khẩu, tự động điền và các dịch vụ liên quan đến tài khoản Google
    # Đây là phần quan trọng nhất để cố gắng tắt popup "Save password"
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,        # Tắt gợi ý lưu thông tin đăng nhập từ Chrome/Google Password Manager
        "profile.password_manager_enabled": False,  # Tắt tính năng quản lý mật khẩu tích hợp của Chrome
        "profile.default_content_settings.popups": 0, # Tắt popup chung
        "profile.default_content_setting_values.notifications": 2, # Tắt thông báo trang web (cho phép/chặn)
        "profile.gaia_info_service.enabled": False,  # RẤT QUAN TRỌNG: Tắt dịch vụ thông tin Google Account
        "profile.password_manager_force_migration": False, # Ngăn chặn việc di chuyển mật khẩu
        "autofill.enabled": False, # Vô hiệu hóa tính năng tự động điền chung
        "autofill.autofill_enabled": False, # Vô hiệu hóa tính năng tự động điền chung
        "password_manager_reauthentication.enabled": False # Vô hiệu hóa xác thực lại cho trình quản lý mật khẩu
    })
    
    # Các switches để loại bỏ hành vi tự động hóa và lời nhắc cụ thể
    # Đã thêm nhiều switch hơn để đảm bảo vô hiệu hóa mọi cơ chế liên quan
    options.add_experimental_option("excludeSwitches", [
        "enable-automation", 
        "enable-logging",
        "disable-password-manager-reauthentication", # Yêu cầu xác thực lại cho trình quản lý mật khẩu
        "disable-sync-credential-provider-based-filling", # Điền thông tin đăng nhập từ đồng bộ hóa
        "disable-offer-uploading-passwords", # Tải mật khẩu lên Google
        "disable-smart-lock-for-passwords", # Smart Lock cho mật khẩu
        "disable-password-generation", # Gợi ý tạo mật khẩu mới
        "disable-autofill-type-predictions", # Dự đoán loại tự động điền
        "save-password-primary-action-button", # Nút lưu mật khẩu
        "show-autofill-type-predictions", # Hiện dự đoán loại tự động điền
        "enable-save-password", # Thử tắt luôn cờ "enable-save-password"
        "enable-credential-manager" # Tắt Credential Manager API
    ])
    options.add_experimental_option("useAutomationExtension", False)

    # -------------------------------------------------------------
    # Các chiến lược bổ sung (Thử từng cái một nếu vẫn không được)
    # -------------------------------------------------------------

    # Chiến lược 1: Chế độ Browser Without Sign-In (CÔ LẬP TÀI KHOẢN GOOGLE)
    # Đây là cờ rất mạnh mẽ để chạy Chrome mà không liên kết với bất kỳ tài khoản Google nào.
    # Thường thì các popup "Change your password" xuất hiện khi Chrome đang cố gắng
    # đồng bộ hóa với tài khoản Google hoặc quản lý mật khẩu của Google.
    # options.add_argument("--bwsi") 

    # Chiến lược 2: Vô hiệu hóa các tính năng qua cờ (Features) - Ít dùng nhưng đôi khi hiệu quả
    options.add_argument("--disable-features=PasswordManagerV2") 
    options.add_argument("--disable-features=AutofillPasswordGeneration")
    options.add_argument("--disable-features=SafeBrowse") # Có thể tắt nhưng có rủi ro bảo mật
    options.add_argument("--disable-background-networking") # Ngăn chặn các hoạt động nền không cần thiết
    options.add_argument("--disable-default-browser-check") # Ngăn Chrome hỏi có phải trình duyệt mặc định không

    return options

# Hàm nội bộ để dọn dẹp thư mục tạm thời (giữ nguyên)
# Trong file browser_options.py của bạn

def _cleanup_temp_dir_function():
    global _temp_user_data_dir
    if _temp_user_data_dir and os.path.exists(_temp_user_data_dir):
        print(f"Attempting to cleanup temporary user data directory: {_temp_user_data_dir}")
        try:
            # Đảm bảo thư mục không bị khóa bởi các tiến trình khác
            shutil.rmtree(_temp_user_data_dir, ignore_errors=True) # ignore_errors=True có thể giúp nhưng không phải là giải pháp gốc
            print(f"Successfully cleaned up temporary user data directory: {_temp_user_data_dir}")
        except Exception as e:
            # In ra lỗi chi tiết nếu không thể xóa thư mục
            print(f"ERROR: Failed to cleanup temp directory {_temp_user_data_dir}: {e}")
            # Không đặt _temp_user_data_dir = None ở đây nếu xóa thất bại,
            # để lần chạy tiếp theo có thể cố gắng dọn dẹp lại hoặc báo lỗi rõ ràng.
    _temp_user_data_dir = None # Luôn đặt lại biến sau khi cố gắng dọn dẹp

# Hàm này sẽ trở thành từ khóa "Cleanup Chrome User Data Directory" trong Robot Framework (giữ nguyên)
def cleanup_chrome_user_data_directory():
    _cleanup_temp_dir_function()
    
    
def quit_browser():
    """
    Từ khóa Robot Framework để đóng trình duyệt Chrome.
    """
    from selenium import webdriver
    try:
        driver = webdriver.Chrome(options=get_chrome_options_object())
        driver.quit()
        print("Browser closed successfully.")
    except Exception as e:
        print(f"Error closing browser: {e}")