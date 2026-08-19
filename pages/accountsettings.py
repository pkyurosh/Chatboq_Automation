from config import ACCOUNT_SETTINGS


class AccountSettingsPage:
    URL = ACCOUNT_SETTINGS

    FULL_NAME = "#fullName"
    FILE_INPUT = 'input[type="file"]'
    PHONE_COUNTRY_SELECTOR = 'button[aria-label="Select country calling code"]'
    PHONE_NUMBER_INPUT = "#phoneNumber"
    COUNTRY_SELECTOR = "//label[contains(text(),'Country')]/following::button[@data-slot='popover-trigger'][1]"
    UPDATE_BUTTON = "button:contains('Update')"
    ERROR_MESSAGE = "span.text-alert-500"
    LOGO_PREVIEW = 'img[src*="chatboq-blog-storage-s3"]'
    REMOVE_IMG_BUTTON = '(//button[@aria-label="Remove image"])'

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.sleep(2)
        return self

    def is_loaded(self):
        return self.sb.is_text_visible("Account Information")

    def upload_logo(self, file_path: str):
        self.sb.click(self.REMOVE_IMG_BUTTON)
        file_input = self.sb.cdp.find_element(self.FILE_INPUT)
        file_input.send_file(file_path)
        self.sb.sleep(1)
        return self

    def enter_account_name(self, random_account_name):
        self.sb.type(self.FULL_NAME, random_account_name)
        self.sb.sleep(1)
        return self

    def enter_phone_details(self, country: str, number: str):
        self.sb.click(self.PHONE_COUNTRY_SELECTOR)
        self.sb.sleep(2)
        self.sb.type('[data-state="open"] input', country)
        self.sb.sleep(1)
        self.sb.click(f'[role="option"]:contains("{country}")')
        self.sb.sleep(1)
        self.sb.type(self.PHONE_NUMBER_INPUT, number)
        self.sb.sleep(1)
        return self

    def enter_phone_number(self, number: str):
        self.sb.clear(self.PHONE_NUMBER_INPUT)
        self.sb.type(self.PHONE_NUMBER_INPUT, number)
        self.sb.sleep(1)
        return self

    def enter_country(self, country: str):
        self.sb.click(self.COUNTRY_SELECTOR)
        self.sb.sleep(1)
        self.sb.type('[data-state="open"] input', country)
        self.sb.sleep(1)
        self.sb.click(f'[role="option"]:contains("{country}")')
        self.sb.sleep(2)
        return self

    def click_update_button(self):
        self.sb.click(self.UPDATE_BUTTON)
        self.sb.sleep(2)
        return self

    def get_error_message(self) -> str:
        self.sb.wait_for_element_visible(self.ERROR_MESSAGE, timeout=10)
        return self.sb.get_text(self.ERROR_MESSAGE)
