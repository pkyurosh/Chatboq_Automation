from config import OPERATING_HOURS


class OperatingHoursPage:
    URL = OPERATING_HOURS

    SAVE_CHANGES_BUTTON = "button[type='submit']"

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.sleep(2)
        return self

    def is_loaded(self):
        return self.sb.is_text_visible("Monday")

    def _checkbox(self, day_index: int) -> str:
        return f'#hours\\.{day_index}\\.isOpen'

    def _start_time(self, day_index: int) -> str:
        return f'#hours\\.{day_index}\\.startTime'

    def _end_time(self, day_index: int) -> str:
        return f'#hours\\.{day_index}\\.endTime'

    def is_day_enabled(self, day_index: int) -> bool:
        return self.sb.get_attribute(self._checkbox(day_index), "aria-checked") == "true"

    def get_start_time(self, day_index: int) -> str:
        return self.sb.get_property(self._start_time(day_index), "value")

    def get_end_time(self, day_index: int) -> str:
        return self.sb.get_property(self._end_time(day_index), "value")
    
    def set_time_value(self, selector: str, hour: str, minute: str, meridiem: str):
        """hour: '09', minute: '00', meridiem: 'A' or 'P'"""
        self.sb.click(selector)
        self.sb.type(selector, f"{hour}{minute}{meridiem}")
        self.sb.sleep(0.5)

    def set_day_hours(self, day_index: int, start_time: tuple = None, end_time: tuple = None, enabled: bool = True):
        checkbox = self._checkbox(day_index)
        is_checked = self.is_day_enabled(day_index)

        if enabled and not is_checked:
            self.sb.click(checkbox)
        elif not enabled and is_checked:
            self.sb.click(checkbox)

        if enabled and start_time and end_time:
            start_input = self._start_time(day_index)
            end_input = self._end_time(day_index)
            self.set_time_value(start_input, *start_time)
            self.set_time_value(end_input, *end_time)

        self.sb.sleep(1)
        return self

    def click_save_changes_button(self):
        self.sb.click(self.SAVE_CHANGES_BUTTON)
        self.sb.sleep(2)
        return self