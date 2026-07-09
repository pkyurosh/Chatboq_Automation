"""from seleniumbase import SB
from pages.accountsettings import AccountSettingsPage
from utils.session_manager import inject_session



class TestInbox:

    def test_settings_loads(self):
        with SB(uc=True) as sb:
            inject_session(sb)      # ← logged in instantly, no Cloudflare
            page = AccountSettingsPage(sb)
            page.open()
            assert page.is_loaded(), "Inbox should load after session injection" 
            """