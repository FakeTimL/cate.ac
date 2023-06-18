"""
URL configuration for drp49 project.

The `urlpatterns` list routes URLs to views. For more information please see:
  https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
  1. Add an import: from me/app import views
  2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
  1. Add an import: from other_app.views import Home
  2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
  1. Import the include() function: from django.urls import include, path
  2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path
from django.conf import settings
from django.templatetags.static import static
from django.conf.urls.static import static as media
from django.views.generic import RedirectView, TemplateView
from django.contrib import admin

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/auth/', include('rest_framework.urls')),
  path('api/accounts/', include('accounts.urls')),
  path('api/main/', include('main.urls')),
]

# Serve media files at static URL under debug mode.
if settings.DEBUG:
  urlpatterns += media(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Ensure that `favicon.ico` is also available in the root URL.
urlpatterns.append(path('favicon.ico', RedirectView.as_view(url=static("favicon.ico"))))

# All other URLs are routed to the frontend `index.html`.
urlpatterns.append(re_path(r'^.*', TemplateView.as_view(template_name='index.html')))

# See: https://www.django-rest-framework.org/api-guide/exceptions/#generic-error-views
handler400 = 'rest_framework.exceptions.bad_request'
handler500 = 'rest_framework.exceptions.server_error'
