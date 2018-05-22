"""smartgym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from tracker.consumers.SetConsumer import SetConsumer
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = i18n_patterns(
    url(r'^landing_page/', include('landing_page.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', RedirectView.as_view(url='/landing_page/', permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r'^tracker/', include('tracker.urls.urls')),
    url(r'^/ws/tracker', SetConsumer),
]

urlpatterns = [
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
