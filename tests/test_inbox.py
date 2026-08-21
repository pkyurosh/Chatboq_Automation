import pytest
from pages.inbox import InboxPage
from tests.conftest import make_authenticated_page_fixture

inbox_page = make_authenticated_page_fixture(InboxPage)


@pytest.mark.run(order=7)
@pytest.mark.usefixtures("inbox_page")
class TestInbox:

    def test_inbox_loads(self):
        assert self.page.is_loaded(), "Inbox page should load"

    def test_select_conversation(self):
        self.page.select_conversation()
        self.sb.assert_url_contains(
            "conversation=7cfb3f59-6863-4989-8c87-a8e0331d3651"
        )  # Confirms if the conversatio is successfully selected by checking the URL for the conversation ID

    def test_type_message(self):
        message = "Hello, this is a test message."
        self.page.type_message(message)
        # Here you might want to add an assertion to check if the message was sent successfully
