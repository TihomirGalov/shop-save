"""shopassist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views
from .forms import UserLoginForm
import os
from django.conf import settings
from .views import register, privacy_policy, toc
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path(
        'login/',
         views.LoginView.as_view(
            template_name=os.path.join(settings.BASE_DIR, "shopassist/templates/admin/login.html"),
            authentication_form=UserLoginForm
        ),
        name='login'
    ),
    path('register/', register, name='register'),
    path('privacy-policy/', privacy_policy, name='privacy-policy'),
    path('toc/', toc, name='toc'),
    path('', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n'))
]

urlpatterns += (
        i18n_patterns(path(r"", admin.site.urls), prefix_default_language=False)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

admin.site.site_url = None