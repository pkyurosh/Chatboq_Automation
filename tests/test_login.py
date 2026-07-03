import pytest
from seleniumbase import SB
from pages.login import LoginPage
from config import VALID_USER, VALID_PASS


@pytest.fixture(scope="module")
def sb_session():
    with SB(uc=True) as sb:
        yield sb


class TestLogin:

    def test_happy_path(self, sb_session):
        page = LoginPage(sb_session)
        page.open()
        page.login(VALID_USER, VALID_PASS)
        assert page.is_logged_in(), "Should be logged in after UI login"


class TestLoginNegative:

    def test_invalid_email(self, sb_session):
        page = LoginPage(sb_session)
        page.open()
        page.login("nonexistent@test.com", "Hello123@")
        error = page.get_error_message()
        assert "Invalid credentials" in error, f"Expected 'Invalid credentials' but got: {error}"

    def test_invalid_password(self, sb_session):
        page = LoginPage(sb_session)
        page.open()
        page.login(VALID_USER, "wrongpassword123")
        error = page.get_error_message()
        assert "Invalid credentials" in error, f"Expected 'Invalid credentials' but got: {error}"

    def test_both_invalid(self, sb_session):
        page = LoginPage(sb_session)
        page.open()
        page.login("fake@fake.com", "fakepassword")
        error = page.get_error_message()
        assert "Invalid credentials" in error, f"Expected 'Invalid credentials' but got: {error}"