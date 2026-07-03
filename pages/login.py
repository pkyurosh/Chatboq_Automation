
from config import AUTH_URL


class LoginPage:
    URL = f"{AUTH_URL}/auth/login"

    USERNAME_INPUT = "#email"       # CSS selector for By.ID "email"
    PASSWORD_INPUT = "#password"    # CSS selector for By.ID "password"
    LOGIN_BUTTON   = "button[type='submit']"
    ERROR_MESSAGE  = "span.text-alert-500"

    def __init__(self, sb):
        self.sb = sb  # SeleniumBase instance, not raw driver

    def open(self):
        self.sb.uc_open_with_reconnect(self.URL, 4)
        self.sb.sleep(3)  # wait for Cloudflare to resolve
        return self

    def enter_username(self, username: str):
        self.sb.type(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.sb.type(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.sb.click(self.LOGIN_BUTTON)
        self.sb.sleep(5)
        return self

    def login(self, username: str, password: str):
        return self.enter_username(username).enter_password(password).click_login()

    def is_logged_in(self) -> bool:
        try:
            self.sb.sleep(5)
            return"/app" in self.sb.get_current_url()
        except Exception:
            return False
        
    def get_error_message(self) -> str:
        self.sb.wait_for_element_visible(self.ERROR_MESSAGE, timeout=10)
        return self.sb.get_text(self.ERROR_MESSAGE)
    
    def clear_and_login(self, username: str, password: str):
        self.sb.clear(self.USERNAME_INPUT)
        self.sb.clear(self.PASSWORD_INPUT)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
    
    def is_login_button_disabled(self) -> bool:
        return self.sb.get_attribute(self.LOGIN_BUTTON, "disabled") is not None 