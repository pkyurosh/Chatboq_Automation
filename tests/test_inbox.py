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
        self.sb.assert_url_contains("conversation=7cfb3f59-6863-4989-8c87-a8e0331d3651")

    def test_send_5_messages(self):
        self.page.send_bulk_messages(count=5)

    def test_reply_to_last_message(self):
        self.page.reply_to_message(
            "Hello this is testing message 5",
            "Replied text......",
        )
