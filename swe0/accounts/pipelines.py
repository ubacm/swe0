from django.conf import settings
from social_core.exceptions import AuthForbidden
from social_core.pipeline.user import create_user


def create_user_if_allowed(strategy, details, backend, user=None, *args, **kwargs):
    """Create new Users if the domain of the email address is whitelisted."""
    if user is None:
        whitelisted_domains = getattr(settings, 'SWE0_CREATE_USER_WHITELISTED_DOMAINS', [])
        if whitelisted_domains:
            email = details.get('email')
            email_domain = email.split('@')[1]
            if email_domain not in whitelisted_domains:
                # TODO: Create a middleware to gracefully handle this.
                raise AuthForbidden(backend)
        return create_user(strategy, details, backend, *args, **kwargs)


def populate_user_name(details, *_args, **_kwargs):
    """Populate details['name'] with the user's name from details['fullname'].

    Python Social Auth uses 'fullname', while we use 'name', so this pipeline
    maps it so that users' names can still be properly identified and stored.
    """
    name = details.get('fullname')
    if name:
        return {'details': {'name': name, **details}}
