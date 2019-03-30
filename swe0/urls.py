"""swe0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('swe0.core.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('swe0.accounts.urls')),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('events/', include('swe0.events.urls')),
    path('polls/', include('swe0.polls.urls')),
    path('profiles/', include('swe0.profiles.urls')),
    path('slack/', include('swe0.slack.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
