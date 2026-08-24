import json
from config import INBOX_URL


class InboxPage:
    URL = INBOX_URL
    CONVERSATION_SELECTOR = 'p:contains("Automation")'
    TYPE_CONVERSATION = 'div[aria-placeholder="Type here..."]'
    SEND_BUTTON = 'button[data-variant="default"]:has(svg path[d^="M9.50929"])'

    MESSAGE_ACTION_BUTTON = 'button[data-slot="dropdown-menu-trigger"]:has(svg path[d^="M14 5C14 3.89543 13.1046 3 12"])'
    REPLY_MENU_ITEM = '[role="menuitem"]:has(span[data-slot="dropdown-menu-shortcut"])'

    def __init__(self, sb):
        self.sb = sb

    def open(self):
        self.sb.open(self.URL)
        self.sb.wait_for_element_visible(self.CONVERSATION_SELECTOR, timeout=20)
        return self

    def select_conversation(self):
        self.sb.click(self.CONVERSATION_SELECTOR)
        self.sb.sleep(2)
        return self

    def is_loaded(self) -> bool:
        return "/app" in self.sb.get_current_url()

    def type_message(self, message: str):
        self.sb.click(self.TYPE_CONVERSATION)
        self.sb.type(self.TYPE_CONVERSATION, message)
        self.sb.sleep(0.3)

        self.sb.wait_for_element_present(self.SEND_BUTTON, timeout=5)
        self.sb.click(self.SEND_BUTTON)

        self.sb.sleep(1)
        return self

    def send_bulk_messages(
        self, count: int, prefix: str = "Hello this is testing message"
    ):
        for i in range(1, count + 1):
            message = f"{prefix} {i}"
            self.type_message(message)
        return self

    def _get_row_uuid(self, message_text: str) -> str:
        """Finds the LAST message row containing message_text and returns
        its data-message-uuid, so we can build a plain, parseable CSS
        selector instead of nesting :contains() inside :has() (which
        SeleniumBase's CSS-to-XPath converter cannot parse)."""
        uuid = self.sb.execute_script(f"""
            (function() {{
                var rows = document.querySelectorAll('div[data-message-uuid]');
                for (var i = rows.length - 1; i >= 0; i--) {{
                    if (rows[i].textContent.includes({json.dumps(message_text)})) {{
                        return rows[i].getAttribute('data-message-uuid');
                    }}
                }}
                return null;
            }})();
        """)
        if not uuid:
            raise Exception(f"No message row found containing: {message_text!r}")
        return uuid

    def reply_to_message(self, message_text: str, reply_text: str):
        """Hovers the row for message_text, clicks its 3-dot menu,
        clicks Reply, and sends reply_text."""
        uuid = self._get_row_uuid(message_text)
        row = f'div[data-message-uuid="{uuid}"]'

        self.sb.cdp.select(row, timeout=5)
        self.sb.cdp.gui_hover_element(row)
        self.sb.sleep(1)

        action_button = f"{row} {self.MESSAGE_ACTION_BUTTON}"
        self.sb.cdp.select(action_button, timeout=5)
        self.sb.cdp.click(action_button)
        self.sb.sleep(0.5)

        self.sb.cdp.select(self.REPLY_MENU_ITEM, timeout=5)
        self.sb.cdp.click(self.REPLY_MENU_ITEM)
        self.sb.sleep(0.5)

        self.type_message(reply_text)
        return self
