import pytest
from seleniumbase import SB
from pages.lead import LeadPage
from tests.conftest import make_authenticated_page_fixture
from utils.test_data import get_random_email

lead_page = make_authenticated_page_fixture(LeadPage)


@pytest.mark.run(order=6)
@pytest.mark.usefixtures("lead_page")
class TestLead:

    def test_lead_page_loads(self):
        assert self.page.is_loaded(), "Lead page should load"

    def test_create_new_lead(self):
        self.page.click_new_lead()
        self.page.enter_lead_details(
            name="Jane Smith",
            email=get_random_email(),
            phone="9812345678",
            lead_type="Enterprise",
            lead_source="Facebook",
            country="Nepal",
            location="San Fransisco, CA",
            notes="Needs follow-up call",
        )
        self.page.click_save_button()
