import pytest
from seleniumbase import SB
from pages.login import LoginPage
from config import VALID_USER, VALID_PASS


@pytest.fixture(scope="class")
def login_page(request):
    with SB(uc=True) as sb:
        page = LoginPage(sb)
        page.open()  # open and solve Cloudflare ONCE
        request.cls.page = page
        request.cls.sb = sb
        yield page


@pytest.mark.run(order=2)
class TestLogin:

    def test_happy_path(self):
        with SB(uc=True) as sb:
            page = LoginPage(sb)
            page.open()
            page.login(VALID_USER, VALID_PASS)
            assert page.is_logged_in(), "Should be logged in after UI login"


@pytest.mark.usefixtures("login_page")
class TestLoginNegative:

    def test_invalid_email(self):
        self.page.clear_and_login("nonexistent@test.com", "Hello123@")
        error = self.page.get_error_message()
        assert "Invalid credentials" in error, f"Expected 'Invalid credentials' but got: {error}"

    def test_invalid_password(self):
        self.page.clear_and_login(VALID_USER, "wrongpassword123")
        error = self.page.get_error_message()
        assert "Invalid credentials" in error, f"Expected 'Invalid credentials' but got: {error}"

    def test_both_invalid(self):
        self.page.clear_and_login("fake@fake.com", "fakepassword")
        error = self.page.get_error_message()
        assert "Invalid credentials" in error, f"Expected 'Invalid credentials' but got: {error}"

    def test_edge_case_email(self):
        self.page.clear_and_login("0000000)))))@gmsssssssssssssssssssssssssss.com", "999999999999999999999")
        error = self.page.get_error_message()
        assert "Please enter a valid email address" in error, f"Expected 'Please enter a valid email address' but got: {error}"


    def test_blank_email(self):
        self.sb.clear(self.page.USERNAME_INPUT)
        self.sb.clear(self.page.PASSWORD_INPUT)
        self.page.enter_password("fakepassword")
        # don't enter email — button should be disabled
        assert self.page.is_login_button_disabled(), "Login button should be disabled when email is empty"

    def test_blank_password(self):
        self.sb.clear(self.page.USERNAME_INPUT)
        self.sb.clear(self.page.PASSWORD_INPUT)
        self.page.enter_username("fake@fake.com")
        # don't enter password — button should be disabled
        assert self.page.is_login_button_disabled(), "Login button should be disabled when password is empty"

    def test_both_blank(self):
        self.sb.clear(self.page.USERNAME_INPUT)
        self.sb.clear(self.page.PASSWORD_INPUT)
        # enter nothing — button should be disabled
        assert self.page.is_login_button_disabled(), "Login button should be disabled when both fields are empty"

