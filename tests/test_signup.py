from seleniumbase import SB
from pages.signup import SignupPage
from utils.mailsac import get_temp_email, get_verification_code
from utils.test_data import get_random_org_name, get_random_domain
from config import SIGNUP_PASSWORD, MAILSAC_API_KEY, SIGNUP_NAME, SIGNUP_ORG_DESCRIPTION, SIGNUP_INDUSTRY, SIGNUP_LOGO_PATH


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

            print("\nOrganization setup complete!")
            input("Press Enter to close browser...")
            print("Press Enter to close browser...")