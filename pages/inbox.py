from config import INBOX_URL


class InboxPage:
    URL = INBOX_URL
    CONVERSATION_SELECTOR = 'p:contains("Automation")'
    TYPE_CONVERSATION = 'div [aria-placeholder="Type here..."]'
    SEND_BUTTON = 'button svg[viewBox="0 0 24 24"]'

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.sleep(2)
        return self

    def is_loaded(self):
        return self.sb.is_text_visible("All Conversations")

    def select_conversation(self):
        self.sb.click(self.CONVERSATION_SELECTOR)
        self.sb.sleep(2)
        return self

    def is_loaded(self) -> bool:
        return (
            "/app" in self.sb.get_current_url()
        )  # Check the url if the conversation is selected

    def type_message(self, message: str):
        # Type the message and send it
        self.sb.type(self.TYPE_CONVERSATION, message)
        self.sb.click(self.SEND_BUTTON)

        self.sb.sleep(1)
        return self
