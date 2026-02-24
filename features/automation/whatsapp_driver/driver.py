from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

class WhatsAppDriver:
    _instance = None
    _driver = None

    @classmethod
    def get_driver(cls):
        # Check if existing driver is valid
        if cls._driver is not None:
            try:
                # This will raise an exception if the window is closed/crashed
                _ = cls._driver.current_url
            except Exception:
                print("Driver found but unresponsive. Cleaning up...")
                try:
                    cls._driver.quit()
                except Exception:
                    pass
                cls._driver = None
                
        if cls._driver is None:
            cls._driver = cls._init_driver()
        return cls._driver

    @staticmethod
    def _init_driver():
        print("Initializing Chrome Driver for Windows...")
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = Options()
            # Keep browser open and use user profile to maintain WhatsApp login
            options.add_argument("--user-data-dir=" + os.path.join(os.path.expanduser("~"), ".jarvis_chrome_profile"))
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            driver.maximize_window()
            return driver
        except Exception as e:
            print(f"Failed to initialize Chrome: {e}")
            print("Make sure Google Chrome is installed.")
            raise e
