from django.contrib.auth.views import LogoutView as DjangoLogOutView
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView


class LogInView(TemplateView):
    template_name = 'accounts/log_in.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('core:home'))
        return super().dispatch(request, *args, **kwargs)


class LogOutView(DjangoLogOutView):
    next_page = 'core:home'
