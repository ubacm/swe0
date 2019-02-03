from django.conf import settings


def email_address_is_whitelisted(email):
    whitelisted_domains = getattr(settings, 'SWE0_CREATE_USER_WHITELISTED_DOMAINS', [])
    if not whitelisted_domains:
        return True
    email_domain = email.split('@')[1]
    return email_domain in whitelisted_domains
