import random
import string


def get_random_org_name():
    """
    Letters only e.g. 'testorgabcdefgh'
    New name every run so org creation never fails with 'already exists'
    """
    random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"testorg{random_str}"


def get_random_domain():
    """
    Letters only + .com e.g. 'helloabcdefgh.com'
    """
    random_str = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"hello{random_str}.com"

def get_random_account_name():
    """
    Letters only for account holders name
    New name every run so that the update button does not stay on disable state
    """
    random_str = ''.join(random.choices(string.ascii_letters, k=6))
    return f"test{random_str}"