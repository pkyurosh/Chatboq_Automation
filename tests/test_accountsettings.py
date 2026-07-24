import pytest
from seleniumbase import SB
from pages.accountsettings import AccountSettingsPage
from utils.session_manager import inject_session
from utils.test_data import get_random_account_name
from config import SIGNUP_LOGO_PATH


INVALID_PHONE_NUMBERS = [
    ("89893893893849839489", "too_long"),
    ("123", "too_short"),
  
]


@pytest.fixture(scope="class")
def account_settings_page(request):                    
    with SB(uc=True) as sb:
        inject_session(sb)
        page = AccountSettingsPage(sb)
        page.open()
        request.cls.page = page
        request.cls.sb = sb
        yield page


@pytest.mark.usefixtures("account_settings_page")
class TestAccountSettings:

    def test_account_settings_loads(self):
        assert self.page.is_loaded(), "Account settings page should load"
        
    def test_upload_account_photo(self):
        old_src = self.sb.get_attribute(self.page.LOGO_PREVIEW, "src")
        self.page.upload_logo(SIGNUP_LOGO_PATH)
        self.sb.sleep(2)
        new_src = self.sb.get_attribute(self.page.LOGO_PREVIEW, "src")
        assert new_src == old_src, f"Logo src should not change after upload as its the same picture, still: {new_src}"

    def test_update_full_name(self):
        self.account_name = get_random_account_name()
        self.page.enter_account_name(self.account_name)
        error = self.sb.get_attribute(self.page.FULL_NAME, "value")
        assert self.account_name in error, f"Expected '{self.account_name}' but got: {error}"

    def test_enter_phone_details(self):
        self.page.enter_phone_details("Nepal", "9812345678")
        value = self.sb.get_attribute(self.page.PHONE_NUMBER_INPUT, "value")
        assert "9812345678" in value or "981 2345678" in value, f"Expected phone number but got: {value}"

    def test_enter_country(self):
        self.page.enter_country("Nepal")
        assert self.sb.is_text_visible("Nepal"), "Nepal should be visible after selection"

    def test_click_update_button(self):
        self.page.click_update_button()
        assert self.sb.is_text_visible("User information updated successfully"), "Success message should appear"


@pytest.mark.usefixtures("account_settings_page")
class TestAccountSettingsNegative:

    @pytest.mark.parametrize("invalid_number, case_id", INVALID_PHONE_NUMBERS)
    def test_invalid_phone_number(self, invalid_number, case_id):
        self.page.open()
        print(self.sb.get_current_url())
        self.page.enter_phone_number(invalid_number)
        self.page.click_update_button()
        error = self.page.get_error_message()
        assert "please enter a valid phone number" in error.lower(), \
            f"[{case_id}] Expected valid phone number error but got: {error}"