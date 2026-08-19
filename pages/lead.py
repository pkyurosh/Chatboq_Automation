from config import LEAD_URL


class LeadPage:
    URL = LEAD_URL

    NEWLEAD_BUTTON = 'button:contains("New Lead")'
    FULL_NAME_INPUT = "#full_name"
    EMAIL_INPUT = "#email"
    PHONE_COUNTRY_SELECTOR = 'button[aria-label="Select country calling code"]'
    PHONE_NUMBER_INPUT = "#phone_number"
    LOCATION_INPUT = "#address"
    LEAD_TYPE_SELECTOR = "#lead_type"
    LEAD_SOURCE_SELECTOR = "#lead_source"
    ADDLEAD_BUTTON = 'button:contains("Add Lead")'
    REQUIREMENTS_NOTES_INPUT = (
        'textarea[placeholder="Add any specific requirement here..."]'
    )

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.sleep(2)
        return self

    def is_loaded(self):
        return self.sb.is_text_visible("Leads")

    def click_new_lead(self):
        self.sb.click(self.NEWLEAD_BUTTON)
        self.sb.wait_for_element_visible(self.FULL_NAME_INPUT, timeout=10)
        return self

    # ---------- shared dropdown helper ----------

    def _select_dropdown_option(self, dropdown_selector: str, option_text: str):
        """Opens a plain Radix-style dropdown (Lead Type, Lead Source)
        and clicks the matching option directly — no search box involved."""
        self.sb.click(dropdown_selector)
        self.sb.sleep(2)
        self.sb.click(f'[role="option"]:contains("{option_text}")')
        self.sb.sleep(1)
        return self

    # ---------- individual field methods ----------

    def enter_full_name(self, name: str):
        self.sb.input(self.FULL_NAME_INPUT, name)
        return self

    def enter_email(self, email: str):
        self.sb.input(self.EMAIL_INPUT, email)
        return self

    def select_phone_country(self, country: str):
        self.sb.click(self.PHONE_COUNTRY_SELECTOR)
        self.sb.sleep(2)
        self.sb.type('input[placeholder="Search country..."]', country)
        self.sb.sleep(1)
        self.sb.click(f'[role="option"]:contains("{country}")')
        self.sb.sleep(1)
        return self

    def enter_phone_number(self, phone: str):
        self.sb.input(self.PHONE_NUMBER_INPUT, phone)
        return self

    def enter_location(self, location: str):
        self.sb.input(self.LOCATION_INPUT, location)
        return self

    def select_lead_type(self, lead_type: str):
        return self._select_dropdown_option(self.LEAD_TYPE_SELECTOR, lead_type)

    def select_lead_source(self, lead_source: str):
        return self._select_dropdown_option(self.LEAD_SOURCE_SELECTOR, lead_source)

    def enter_requirements_notes(self, notes: str):
        self.sb.input(self.REQUIREMENTS_NOTES_INPUT, notes)
        return self

    # ---------- combined flow ----------

    def enter_lead_details(
        self,
        name: str,
        email: str,
        phone: str,
        lead_type: str,
        lead_source: str,
        country: str,
        location: str = None,
        notes: str = None,
    ):
        self.enter_full_name(name)
        self.enter_email(email)
        self.select_phone_country(country)
        self.enter_phone_number(phone)
        if location:
            self.enter_location(location)
        self.select_lead_type(lead_type)
        self.select_lead_source(lead_source)
        self.enter_requirements_notes(notes)
        return self

    def click_save_button(self):
        self.sb.click(self.ADDLEAD_BUTTON)
        self.sb.sleep(2)
        return self
