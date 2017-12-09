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
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView

from content import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),

    url(r'^.*index.php$', views.redirect_index, name='redirect_index'),
    url(r'^.*event.php$', views.redirect_event, name='redirect_event'),
    url(r'^.*(/images/.*)$', views.redirect_images, name='redirect_images'),
    url(r'directions.html', RedirectView.as_view(url='/directions/')),

    url(r'^projects/', views.projects, name='projects'),
    url(r'^events/', views.events, name='events'),
    url(r'^works/', views.works, name='works'),
    url(r'^texts/', views.texts, name='texts'),

    url(r'^about/', views.about, name='about'),
    url(r'^contact/', views.contact, name='contact'),


    url(r'^(?P<shortname>.+)/$', views.content, name='content'),
]

