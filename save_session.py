import json
import time
from seleniumbase import SB

with SB(uc=True) as sb:
    sb.open("https://stagingv2.chatboq.com")
    print("Log in manually, then press Enter...")
    input()

    while "stagingv2.chatboq.com/app" not in sb.get_current_url():
        time.sleep(1)
    time.sleep(3)

    result = sb.execute_cdp_cmd("Network.getAllCookies", {})
    cookies = result["cookies"]
    print(f"Captured {len(cookies)} cookies")

    with open("session.json", "w") as f:
        json.dump(cookies, f, indent=2)
    print("Session saved!")