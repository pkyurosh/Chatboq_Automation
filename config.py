import os

# URLs
AUTH_URL = os.getenv("AUTH_URL", "https://stagingv2.chatboq.com")
APP_URL = os.getenv("APP_URL", "https://stagingv2.chatboq.com/app/")
ACCOUNT_SETTINGS = os.getenv(
    "ACCOUNTSETTINGS_URL",
    "https://stagingv2.chatboq.com/app/e9c01680-2c88-43b8-a55c-dcfc1ce0b4f9/settings/account-settings/account-information",
)
OPERATING_HOURS = os.getenv(
    "OPERATINGHOURS_URL",
    "https://stagingv2.chatboq.com/app/e9c01680-2c88-43b8-a55c-dcfc1ce0b4f9/settings/organization-settings/operating-hours",
)
LEAD_URL = os.getenv(
    "LEAD_URL",
    "https://stagingv2.chatboq.com/app/e9c01680-2c88-43b8-a55c-dcfc1ce0b4f9/lead",
)

INBOX_URL = os.getenv(
    "INBOX_URL",
    "https://stagingv2.chatboq.com/app/e9c01680-2c88-43b8-a55c-dcfc1ce0b4f9/default-inbox",
)


TIMEOUT = int(os.getenv("TIMEOUT", 10))

# Login credentials
VALID_USER = os.getenv("LOGIN_USER", "jneirixs@sharklasers.com")
VALID_PASS = os.getenv("LOGIN_PASS", "Hello123@")

# Signup
SIGNUP_PASSWORD = os.getenv("SIGNUP_PASSWORD", "Hello123@")

# Mailsac — paste your regenerated key here
MAILSAC_API_KEY = os.getenv(
    "MAILSAC_API_KEY", "k_GC6dkgOchBXpqFLXJkQ77qpW7yKzceC0jL1v6YBsc5"
)

# ONBOARDING SIGNUP
SIGNUP_NAME = os.getenv("SIGNUP_NAME", "Test User")

# ONBOARDING DESCRIPTION
SIGNUP_ORG_DESCRIPTION = os.getenv(
    "SIGNUP_ORG_DESCRIPTION", "This is a test organization created by automation."
)

# SELECT INDUSTRY
SIGNUP_INDUSTRY = os.getenv("SIGNUP_INDUSTRY", "IT")

# SELECT FILE PATH
SIGNUP_LOGO_PATH = os.getenv("SIGNUP_LOGO_PATH", r"C:\Users\user\Downloads/message.png")
