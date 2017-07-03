"""camp URL Configuration

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
from markdownx import urls as markdownx
from content import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from photologue.views import GalleryListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^events/(?P<shortname>\w+)/$', views.events, name='events'),
    url(r'^projects/(?P<shortname>\w+)/$', views.projects, name='projects'),
    url(r'^project/', views.project),
    url(r'^markdownx/', include(markdownx)),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    url(r'^gallerylist/$', GalleryListView.as_view(), name='gallery-list'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

