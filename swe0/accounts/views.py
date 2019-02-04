from django.contrib.auth.views import LogoutView as DjangoLogOutView


class LogOutView(DjangoLogOutView):
    next_page = 'core:home'
