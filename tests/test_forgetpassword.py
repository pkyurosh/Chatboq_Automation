import json
import pytest
from seleniumbase import SB
from pages.forgetpassword import ForgetPasswordPage
from utils.mailsac import get_reset_link
from config import MAILSAC_API_KEY


@pytest.mark.run(order=5)
class TestForgetPassword:

    def test_forget_password_flow(self):
        with open("known_account.json", "r") as f:
            data = json.load(f)
        email = data["email"]
        print(f"Using known account: {email}")

        with SB(uc=True, time_limit=300) as sb:
            page = ForgetPasswordPage(sb)
            page.open()
            page.click_forgot_password()
            page.enter_reset_email(email)
            page.click_reset_submit()

            sb.sleep(15)  # give the email time to actually arrive before checking

            reset_link = get_reset_link(email, MAILSAC_API_KEY)
            print(f"Reset link: {reset_link}")
            sb.open(reset_link)

            new_password = "NewPassword123!"
            page.enter_new_password(new_password)
            page.enter_confirm_password(new_password)
            page.click_reset_password_submit()

            sb.sleep(3)

            assert (
                sb.is_text_visible("Password reset successfully")
                or "login" in sb.get_current_url()
            ), f"Expected confirmation or redirect after password reset, but URL was: {sb.get_current_url()}"
