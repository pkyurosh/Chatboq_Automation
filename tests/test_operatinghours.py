import pytest
from seleniumbase import SB
from pages.operatinghours import OperatingHoursPage
from tests.conftest import make_authenticated_page_fixture
from utils.session_manager import inject_session

OFFICE_HOURS = {
    0: (("09", "00", "A"), ("05", "00", "P")),  # Monday: 9:00 AM to 5:00 PM
    1: (("09", "00", "A"), ("05", "00", "P")),  # Tuesday: 9:00 AM to 5:00 PM
    2: (("09", "00", "A"), ("05", "00", "P")),  # Wednesday: 9:00 AM to 5:00 PM
    3: (("09", "00", "A"), ("05", "00", "P")),  # Thursday: 9:00 AM to 5:00 PM
    4: (("09", "00", "A"), ("05", "00", "P")),  # Friday: 9:00 AM to 5:00 PM
}

CLOSED_DAYS = [5, 6]  # Saturday, Sunday


operating_hours_page = make_authenticated_page_fixture(OperatingHoursPage)


@pytest.mark.run(order=4)
@pytest.mark.usefixtures("operating_hours_page")
class TestOperatingHours:

    def test_operating_hours_loads(self):
        assert self.page.is_loaded(), "Operating hours page should load"

    def test_set_weekday_hours(self):
        for index, (start, end) in OFFICE_HOURS.items():
            self.page.set_day_hours(index, start, end, enabled=True)

        for index, (start, end) in OFFICE_HOURS.items():
            assert self.page.is_day_enabled(
                index
            ), f"Day index {index} should be enabled"

            expected_start = f"{start[0]}:{start[1]}"  # e.g. "09:00"
            expected_end_hour = (
                str(int(end[0]) + 12) if end[2] == "P" and end[0] != "12" else end[0]
            )
            expected_end = f"{expected_end_hour}:{end[1]}"  # e.g. "17:00" for 5:00 PM

            actual_start = self.page.get_start_time(index)
            actual_end = self.page.get_end_time(index)

            assert (
                expected_start in actual_start
            ), f"Day {index} expected start '{expected_start}' but got '{actual_start}'"
            assert (
                expected_end in actual_end
            ), f"Day {index} expected end '{expected_end}' but got '{actual_end}'"

    def test_set_weekend_closed(self):
        for index in CLOSED_DAYS:
            self.page.set_day_hours(index, enabled=False)

        for index in CLOSED_DAYS:
            assert not self.page.is_day_enabled(
                index
            ), f"Day index {index} should be disabled"

    def test_click_save_changes_button(self):
        self.page.click_save_changes_button()
        assert self.sb.is_text_visible(
            "Operating schedule updated successfully"
        ), "Success message should appear"
