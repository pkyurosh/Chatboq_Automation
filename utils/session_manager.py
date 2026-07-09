import json 
from config import APP_URL

def inject_session(sb):
    sb.open(APP_URL)

    with open("session.json", "r") as f:
        cookies = json.load(f)
    
    for cookie in cookies:
        cookie.pop("sameSite", None)
        cookie.pop("expiry", None)
        try:
            sb.add_cookie(cookie)
        except Exception:
            pass
    
    sb.open(APP_URL)
    return sb