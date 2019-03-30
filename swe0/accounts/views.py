from django.conf import settings
from django.contrib.auth.views import (
    LoginView as DjangoLogInView,
    LogoutView as DjangoLogOutView,
)
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView


class LogInView(TemplateView):
    template_name = 'accounts/log_in.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('core:home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, show_local_login_link=settings.DEBUG)


class LocalLogInView(DjangoLogInView):
    template_name = 'accounts/local_log_in.html'


class LogOutView(DjangoLogOutView):
    next_page = 'core:home'
