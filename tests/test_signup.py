import pytest
from seleniumbase import SB
from pages.signup import SignupPage
from utils.mailsac import get_temp_email, get_verification_code
from utils.test_data import get_random_org_name, get_random_domain
from config import SIGNUP_PASSWORD, MAILSAC_API_KEY, SIGNUP_NAME, SIGNUP_ORG_DESCRIPTION, SIGNUP_INDUSTRY, SIGNUP_LOGO_PATH, VALID_PASS, VALID_USER


@pytest.fixture(scope="class")
def signup_page(request):
    with SB(uc=True, time_limit=300) as sb:
        page = SignupPage(sb)
        page.open()
        page.click_signup()

        email = get_temp_email()
        print(f"\nUsing email: {email}")

        request.cls.email = email
        request.cls.page  = page
        request.cls.sb    = sb
        yield page

class TestSignup:

    def test_signup(self):
        with SB(uc=True, time_limit=300) as sb:
            page = SignupPage(sb)

            # Step 1: open login page
            page.open()

            # Step 2: click sign up + wait for Cloudflare to fully resolve
            page.click_signup()

            # Step 3: generate email ONLY after Cloudflare is solved
            email = get_temp_email()
            print(f"\nUsing email: {email}")

            # Step 4: enter temp email and continue
            page.enter_email(email)
            page.click_continue_email()

            # Step 5: enter password and continue
            page.enter_password(SIGNUP_PASSWORD)
            page.click_continue_email()

            # Step 6: fetch verification code from mailsac inbox
            code = get_verification_code(email, MAILSAC_API_KEY)
            print(f"Entering code: {code}")

            # Step 7: enter code and submit
            page.enter_verification_code(code)
            page.click_continue_verification()

            # Step 8: assert signup was successful
            sb.assert_url_contains("/verify/onboarding")
            print("Signup successful!")

            # Step 9: enter full name in onboarding
            page.enter_full_name(SIGNUP_NAME)

            # Step 10: select dark mode
            page.click_dark_mode()

            # Step 11: select discovery source
            page.click_google_sel()

            # Step 12: click next to complete onboarding
            page.click_next_btn()

            # Step 13: generate org details
            org_name = get_random_org_name()
            domain   = get_random_domain()
            print(f"\nOrg: {org_name} | Domain: {domain}")

            # Step 14: enter org details
            page.enter_org_details(org_name, domain, SIGNUP_ORG_DESCRIPTION)
            page.click_org_continue()

            # Step 15: select industry
            page.select_industry(SIGNUP_INDUSTRY)

            # Step 16: upload logo
            page.upload_logo(SIGNUP_LOGO_PATH)
            page.click_continue_industry()

            # Step 17: click team size
            page.click_team_size()
            page.click_next_btn()

            # Step 18: select previous tool
            page.select_prev_tool()
            page.click_next_btn()

            # Step 19: select success question
            page.select_success()
            page.click_submit_onboarding()

            # Step 20: final org onboarding
            page.click_org_onboarding_success()


            print("Press Enter to close browser...")

@pytest.mark.usefixtures("signup_page")
class TestNegativeSignup:
    def test_already_registered_email(self):
        self.page.open()
        self.page.click_signup()
        self.page.enter_email(VALID_USER)
        self.page.click_continue_email()
        self.page.enter_password(VALID_PASS)
        self.page.click_continue_email()
        error = self.page.get_error_message()
        assert "A user with this email already exists" in error, f"Expected'user already exists but got:' {error}"

    def test_invalid_email(self):
        self.page.clear_and_continue("test@gmaildotcom", "Hello123@")
        error = self.page.get_error_message()
        assert "Please enter a valid email address" in error, f"Expected'enter valid address but got'{error}"
        assert self.page.is_continue_button_disabled(), "Login Button should be disabled"

    @pytest.mark.parametrize("password,expected_error", [
        ("pass",      "Password must be greater than 8 characters"),
        ("password",  "Must contain at least one uppercase letter"),    
        ("PASSWORD",  "Must contain at least one lowercase letter"),
        ("Password",  "Must contain at least one number"),
        ("Password1", "Must contain at least one special character"),
    ])
    def test_weak_password(self, password, expected_error):
        self.page.clear_and_continue("test@gmail.com", password)
        error = self.page.get_error_message()
        assert expected_error in error, f"Expected '{expected_error}' but got: {error}" 
             


    #Signup after all the negtive scenarios
    def test_proceed_to_verification(self):
        self.page.clear_and_continue(self.email, SIGNUP_PASSWORD)
       
        

    def test_wrong_verification_code(self):
        self.page.enter_verification_code("12345532")
        self.page.click_continue_verification()
        error = self.page.get_error_message()
        assert "Code must be exactly 6 digits" in error, f"Expected 'Code must be exactly 6 digits but got {error}'"     


    #get verification code from mailsac and log into the system

    def test_proceed_past_verification(self):
        code = get_verification_code(self.email, MAILSAC_API_KEY)
        print(f"Entering code: {code}")
        self.page.enter_verification_code(code)
        self.page.click_continue_verification()

    @pytest.mark.parametrize("full_name,expected_error",[
        ("nnn",           "Name must be at least 5 characters"),
        ("FullName223", "Must contain only letters, spaces, hyphens, and apostrophes"),
        (" ",           "Name is required"),
    ])

    def test_invalid_full_name(self, full_name, expected_error):
        self.page.enter_full_name(full_name)
        error = self.page.get_error_message()
        assert expected_error in error, f"Expected '{expected_error}' but got: {error}"
        assert self.page.is_continue_button_disabled(), "Login Button should be disabled"
    
    def test_valid_full_name_no_selector(self):
        self.page.enter_full_name(SIGNUP_NAME)
        assert self.page.is_continue_button_enabled(), "Next Button shoould be enabled"

    def test_proceed_past_user_onboarding(self):
        self.page.click_google_sel()
        self.page.click_next_btn()
        self.sb.assert_url_contains("verify/onboarding")
   
    def test_org_onboarding(self):
        self.page.enter_org_details(
            "--OOOOsklsdOOOOOOO",
            "--00900.com",
            "))))))))))))))))))))))))))))))))))))))))))))))))))))"
        )
        assert self.page.is_org_continue_button_disabled()

    def test_org_onboarding_duplicate(self):
        self.page.enter_org_details(
            "chatboq",
            get_random_domain(),
            SIGNUP_ORG_DESCRIPTION
        )
        assert self.page.is_org_continue_button_enabled()

        self.page.click_org_continue()
        self.page.click_continue_industry()
        self.page.click_next_btn()
        self.page.click_next_btn()
        self.page.click_submit_onboarding()
        

        error = self.page.get_error_message()
        assert "chatboq" in error.lower() or "exists" in error.lower(), \
            f"Expected duplicate org name error but got: {error}"
        
    def test_org_domain_duplicate(self):
        self.page.enter_org_details(
            get_random_org_name(),
            "chatboq.com",
            SIGNUP_ORG_DESCRIPTION
        )
        assert self.page.is_org_continue_button_enabled()

        self.page.click_org_continue()
        self.page.click_continue_industry()
        self.page.click_next_btn()
        self.page.click_next_btn()
        self.page.click_submit_onboarding()
            

        error = self.page.get_error_message()
        assert "chatboq" in error.lower() or "exists" in error.lower(), \
            f"Expected duplicate org name error but got: {error}"
            

    def test_negative_testing_complete(self):
        print("\n" + "="*50)
        print("✅ Negative testing completed for Signup")
        print("="*50)
    
    
