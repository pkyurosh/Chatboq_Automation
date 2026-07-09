import json
import time
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.open("https://auths.chatboq.com/auth/login")
    print("Log in manually, then press Enter...")
    input()
    
    while "apps.chatboq.com" not in sb.get_current_url() and "apps.chatboq.com" not in sb.get_current_url():
        time.sleep(1)
    
    cookies = sb.get_cookies()
    with open("session.json", "w") as f:
        json.dump(cookies, f, indent=2)
    
    print("Session saved!")