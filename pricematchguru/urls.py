"""
URL configuration for pricematchguru project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls import handler404
from home import views
from django.conf import settings
from django.conf.urls.static import static
from theme.views import changeTheme

# Custom 404 handler
handler404 = "home.views.custom_404"

admin.site.site_header = 'Admin Portal'
admin.site.site_title = 'Akhilesh Admin Portal'
admin.site.site_url = 'Welcome to {admin.site.site_title}'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('switch-theme/',changeTheme, name='change-theme'),
    path('',include('home.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)