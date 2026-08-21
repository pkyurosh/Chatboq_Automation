import pytest
from seleniumbase import SB
from utils.session_manager import inject_session


def make_authenticated_page_fixture(page_class):
    """Factory: returns a pytest fixture that logs in, opens the given
    page object, and attaches it to the test class as self.page / self.sb."""

    @pytest.fixture(scope="class")
    def _fixture(request):
        with SB(uc=True) as sb:
            inject_session(sb)
            page = page_class(sb)
            page.open()
            request.cls.page = page
            request.cls.sb = sb
            yield page

    return _fixture
