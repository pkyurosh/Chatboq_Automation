import requests
import time
import re
import random
import string
from bs4 import BeautifulSoup

MAILSAC_BASE = "https://mailsac.com/api"


def get_temp_email():
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{random_str}@mailsac.com"


def get_verification_code(email, api_key, retries=10, delay=5):
    headers = {"Mailsac-Key": api_key}

    for attempt in range(retries):
        print(f"Checking inbox... attempt {attempt + 1}/{retries}")

        response = requests.get(
            f"{MAILSAC_BASE}/addresses/{email}/messages", headers=headers
        )
        messages = response.json()

        if messages:
            message_id = messages[0]["_id"]

            body_response = requests.get(
                f"{MAILSAC_BASE}/body/{email}/{message_id}", headers=headers
            )
            html = body_response.text

            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()
            print(f"Email text: {text[:500]}")

            match = re.search(r"\b(\d{6})\b", text)
            if match:
                code = match.group(1)
                print(f"Code found: {code}")
                return code

        time.sleep(delay)

    raise Exception("Verification code not received after 50 seconds")


def get_reset_link(email, api_key, retries=10, delay=5):
    headers = {"Mailsac-Key": api_key}

    for attempt in range(retries):
        print(f"Checking inbox for reset link... attempt {attempt + 1}/{retries}")

        response = requests.get(
            f"{MAILSAC_BASE}/addresses/{email}/messages", headers=headers
        )
        messages = response.json()

        if messages:
            messages_sorted = sorted(
                messages, key=lambda m: m["received"], reverse=True
            )
            message_id = messages_sorted[0]["_id"]

            body_response = requests.get(
                f"{MAILSAC_BASE}/body/{email}/{message_id}", headers=headers
            )
            html = body_response.text

            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()

            match = re.search(
                r'https?://[^\s"\'<>]*set-password[^\s"\'<>]*', text, re.IGNORECASE
            )
            if match:
                link = match.group(0)
                print(f"Reset link found: {link}")
                return link

            links = soup.find_all("a", href=True)
            for link_tag in links:
                href = link_tag["href"]
                if "set-password" in href.lower() or "reset" in href.lower():
                    print(f"Reset link found (anchor tag): {href}")
                    return href

        time.sleep(delay)

    raise Exception("Reset link not received after 50 seconds")
