# variables/browser_options.py
from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    options = Options()
    options.add_argument('--guest')
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
    # options.add_argument("--allow-running-insecure-content")
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    prefs = {
        "credentials_enable_service": False,  
        "profile.password_manager_enabled": False ,  # tắt arlert save password chrome
        "profile.default_content_settings.popups": 0,
      }
    options.add_experimental_option( "excludeSwitches", ["enable-automation",'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('prefs', prefs)
    return options


# Hàm get_variables() mà Robot Framework sẽ gọi để lấy các biến động
def get_variables():
    return {
        "OPTIONS": get_chrome_options()
    }