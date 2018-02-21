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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from markdownx import urls as markdownx
from photologue.views import GalleryListView

from content import views



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),

    url(r'^.*index.php$', views.redirect_index, name='redirect_index'),
    url(r'^.*event.php$', views.redirect_event, name='redirect_event'),
    url(r'^.*(/images/.*)$', views.redirect_images, name='redirect_images'),
    url(r'directions.html', RedirectView.as_view(url='/directions/')),
    url(r'campstudio.html', RedirectView.as_view(url='/directions/')),

    url(r'^contact/$', views.contact),

    url(r'^texts/index/$', views.section_list, {'section': 'Texts'}, name='texts_list'),
    url(r'^events/index/$', views.section_list, {'section': 'Events'}, name='events_list'),
    url(r'^projects/index/$', views.section_list, {'section': 'Projects'}, name='projects_list'),
    url(r'^works/index/$', views.section_list, {'section': 'Works'}, name='works_list'),

    url(r'^texts/(?P<shortname>.+)/$', views.texts, name='texts'),
    url(r'^events/(?P<shortname>.+)/$', views.events, name='events'),
    url(r'^projects/(?P<shortname>.+)/$', views.projects, name='projects'),
    url(r'^works/(?P<shortname>.+)/$', views.works, name='work'),
    url(r'^works/$', views.works, name='works'),
    url(r'^projects/$', views.projects),
    url(r'^events/$', views.events),
    url(r'^texts/$', views.texts),
    url(r'^search/$', views.search),
    url(r'^markdownx/', include(markdownx)),
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),
    url(r'^gallerylist/$', GalleryListView.as_view(), name='gallery-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    url(r'^(?P<shortname>\w+)/$', views.page, name='page')
]

