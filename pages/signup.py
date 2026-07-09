import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import AUTH_URL


class SignupPage:
    URL = f"{AUTH_URL}/auth/login"

    SIGNUP_BUTTON      = 'a[href="/auth/sign-up"]'
    EMAIL_INPUT        = "#email"
    PASSWORD_INPUT     = "#password"
    VERIFICATION_INPUT = "#token"
    CONTINUE_BUTTON    = "button[type='submit']"
    FULL_NAME_INPUT    = "#fullName"
    DARK_MODE_BUTTON   = "#dark"
    GOOGLE_SELECT      = 'span:contains("Google")'
    ORG_NAME_INPUT     = "#name"
    ORG_DOMAIN_INPUT   = "#domain"
    ORG_DESC_INPUT     = "#description"
    INDUSTRY_DROPDOWN  = "#onboarding\\.industry"
    LOGO_UPLOAD        = "input[type='file']"
    TEAM_SIZE          = 'span:contains("50-100 Employees")'
    TOOL_NAME          = 'span:contains("Zendesk")'
    SUCCESS_QUESTION   = 'span:contains("Automate Support Task")'
    EMAIL_EXISTS       = "span.text-alert-500"

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.sleep(2)
        return self

    def click_signup(self):
        self.sb.click(self.SIGNUP_BUTTON)
        self.sb.uc_gui_handle_cf()
        self.sb.wait_for_element_visible(self.EMAIL_INPUT, timeout=60)
        return self

    def enter_email(self, email: str):
        self.sb.type(self.EMAIL_INPUT, email)
        self.sb.sleep(2)
        return self

    def click_continue_email(self):
        self.sb.uc_gui_handle_cf()
        self.sb.sleep(2)
        self.sb.js_click(self.CONTINUE_BUTTON)
        self.sb.sleep(3)
        return self

    def enter_password(self, password: str):
        self.sb.type(self.PASSWORD_INPUT, password)
        self.sb.sleep(2)
        return self

    def enter_verification_code(self, code: str):
        self.sb.type(self.VERIFICATION_INPUT, code)
        self.sb.sleep(2)
        return self

    def click_continue_verification(self):
        self.sb.uc_click(self.CONTINUE_BUTTON)
        self.sb.sleep(10)
        return self

    def enter_full_name(self, name: str):
        self.sb.type(self.FULL_NAME_INPUT, name)
        self.sb.sleep(1)
        return self

    def click_dark_mode(self):
        self.sb.uc_click(self.DARK_MODE_BUTTON)
        self.sb.sleep(2)
        return self

    def click_google_sel(self):
        self.sb.uc_click(self.GOOGLE_SELECT)
        self.sb.sleep(2)
        return self

    def click_next_btn(self):
        # uses JavaScript to find exact "Next" button — avoids clicking Skip
        self.sb.execute_script("""
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Next') {
                    btn.click();
                    break;
                }
            }
        """)
        self.sb.sleep(3)
        return self

    def enter_org_details(self, org_name: str, domain: str, description: str):
        self.sb.type(self.ORG_NAME_INPUT, org_name)
        self.sb.sleep(1)
        self.sb.type(self.ORG_DOMAIN_INPUT, domain)
        self.sb.sleep(1)
        self.sb.type(self.ORG_DESC_INPUT, description)
        self.sb.sleep(1)
        return self

    def click_org_continue(self):
        # clicks Continue button by exact text
        self.sb.execute_script("""
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Continue') {
                    btn.click();
                    break;
                }
            }
        """)
        self.sb.sleep(3)
        return self

    def select_industry(self, industry: str):
        self.sb.click(self.INDUSTRY_DROPDOWN)
        self.sb.sleep(2)
        self.sb.click(f'[role="option"]:contains("{industry}")')
        self.sb.sleep(1)
        return self

    def upload_logo(self, file_path: str):
        self.sb.choose_file(self.LOGO_UPLOAD, file_path)
        self.sb.sleep(2)
        return self

    def click_continue_industry(self):
        self.sb.execute_script("""
            const buttons = document.querySelectorAll('button');
            for (const btn of buttons) {
                if (btn.textContent.trim() === 'Continue') {
                    btn.click();
                    break;
                }
            }
        """)
        self.sb.sleep(3)
        return self

    def click_team_size(self):
        self.sb.uc_click(self.TEAM_SIZE)
        self.sb.sleep(2)
        return self

    def select_prev_tool(self):
        self.sb.wait_for_element_visible(self.TOOL_NAME, timeout=15)
        self.sb.uc_click(self.TOOL_NAME)
        self.sb.sleep(2)
        return self

    def select_success(self):
        self.sb.wait_for_element_visible(self.SUCCESS_QUESTION, timeout=15)
        self.sb.uc_click(self.SUCCESS_QUESTION)
        self.sb.sleep(2)
        return self

    def click_submit_onboarding(self):
        self.sb.uc_click(self.CONTINUE_BUTTON)
        self.sb.sleep(3)
        return self

    def click_org_onboarding_success(self):
        self.sb.js_click('button:contains("Start")')
        self.sb.sleep(3)
        return self
    
    def clear_and_continue(self, email: str, password: str):
        self.sb.clear(self.EMAIL_INPUT)
        self.sb.clear(self.PASSWORD_INPUT)
        self.enter_email(email)
        self.enter_password(password)
        self.click_continue_email()
        return self
    
    def get_error_message(self) -> str:
        self.sb.wait_for_element_visible(self.EMAIL_EXISTS, timeout=15)
        return self.sb.get_text(self.EMAIL_EXISTS)
    
    
    def is_continue_button_disabled(self) -> bool:
        return self.sb.get_attribute(self.CONTINUE_BUTTON, "disabled") is not None 
    
    def is_continue_button_enabled(self) -> bool:
        return self.sb.get_attribute(self.CONTINUE_BUTTON, "disabled") is None 
    

    