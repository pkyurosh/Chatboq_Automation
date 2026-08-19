import json
from config import APP_URL

def inject_session(sb):
    with open("session.json", "r") as f:
        cookies = json.load(f)

    sb.execute_cdp_cmd("Network.setCookies", {"cookies": cookies})
    sb.open(APP_URL)
    return sb