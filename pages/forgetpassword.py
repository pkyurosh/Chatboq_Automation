from config import AUTH_URL


class ForgetPasswordPage:
    URL = f"{AUTH_URL}/auth/login"

    FORGOT_PASSWORD_BUTTON = "a[href='/auth/forgot-password']"
    RESET_EMAIL_INPUT = "#email"
    REQUEST_RESET_BUTTON = "button[type='submit']"
    NEW_PASSWORD_INPUT = "#password"
    CONFIRM_PASSWORD_INPUT = "#confirmPassword"
    CHANGE_PASSWORD_BUTTON = 'button:contains("Change Password")'

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.sleep(2)
        return self

    def click_forgot_password(self):
        self.sb.click(self.FORGOT_PASSWORD_BUTTON)
        self.sb.sleep(2)
        return self

    def enter_reset_email(self, email: str):
        self.sb.type(self.RESET_EMAIL_INPUT, email)
        self.sb.sleep(1)
        return self

    def click_reset_submit(self):
        self.sb.click(self.REQUEST_RESET_BUTTON)
        self.sb.sleep(2)
        return self

    def enter_new_password(self, password: str):
        self.sb.type(self.NEW_PASSWORD_INPUT, password)
        self.sb.sleep(1)
        return self

    def enter_confirm_password(self, password: str):
        self.sb.type(self.CONFIRM_PASSWORD_INPUT, password)
        self.sb.sleep(1)
        return self

    def click_reset_password_submit(self):
        self.sb.click(self.CHANGE_PASSWORD_BUTTON)
        self.sb.sleep(2)
        return self
