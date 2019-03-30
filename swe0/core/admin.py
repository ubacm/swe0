from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView


# Redirect the admin log-in view to the normal log-in view.
admin.site.login = RedirectView.as_view(
    pattern_name=settings.LOGIN_URL,
    query_string=True,
)
