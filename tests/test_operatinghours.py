import pytest
from seleniumbase import SB
from pages.operatinghours import OperatingHoursPage
from utils.session_manager import inject_session


OFFICE_HOURS = {
    0: ("09:00", "1700"),  # Monday
    1: ("09:00", "1700"),  # Tuesday
    2: ("09:00", "1700"),  # Wednesday
    3: ("09:00", "1700"),  # Thursday
    4: ("09:00", "1700"),  # Friday
}
CLOSED_DAYS = [5, 6]  # Saturday, Sunday


@pytest.fixture(scope="class")
def operating_hours_page(request):
    with SB(uc=True) as sb:
        inject_session(sb)
        page = OperatingHoursPage(sb)
        page.open()
        request.cls.page = page
        request.cls.sb = sb
        yield page


@pytest.mark.usefixtures("operating_hours_page")
class TestOperatingHours:

    def test_operating_hours_loads(self):
        assert self.page.is_loaded(), "Operating hours page should load"

    def test_set_weekday_hours(self):
        for index, (start, end) in OFFICE_HOURS.items():
            self.page.set_day_hours(index, start, end, enabled=True)

        for index, (start, end) in OFFICE_HOURS.items():
            assert self.page.is_day_enabled(index), f"Day index {index} should be enabled"
            assert start in self.page.get_start_time(index), \
                f"Day index {index} expected start '{start}' but got '{self.page.get_start_time(index)}'"
            assert end in self.page.get_end_time(index), \
                f"Day index {index} expected end '{end}' but got '{self.page.get_end_time(index)}'"

    def test_set_weekend_closed(self):
        for index in CLOSED_DAYS:
            self.page.set_day_hours(index, enabled=False)

        for index in CLOSED_DAYS:
            assert not self.page.is_day_enabled(index), f"Day index {index} should be disabled"

    def test_click_save_changes_button(self):
        self.page.click_save_changes_button()
        assert self.sb.is_text_visible("Operating schedule updated successfully"), \
            "Success message should appear"