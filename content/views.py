# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Content, ContentContent
from django.db.models import Q
from django.views.generic.list import ListView
from photologue.views import GalleryListView 
from photologue.models import Photo, Gallery
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request):
    latest_content_list = Content.objects.order_by('-datestart')[:12]
    homepage = Content.objects.filter(type=2).order_by('-datestart')[:1]
    context = {'latest_content_list': latest_content_list, 'homepage': homepage}
    return render(request, 'index.html', context)

def project(request):
    content = Content.objects.filter(type=3).order_by('-datestart')
    return render(request, 'project.html', {'content': content})

def work(request):
    content = Content.objects.filter(type=4)
    return render(request, 'text.html', {'content': content})

def event(request):
    latest_content_list = Content.objects.filter(Q(type=0) | Q(type=1)).order_by('-datestart')[:8]
    featured = Content.objects.filter(type=0).order_by('-datestart')[:1]
    context = {'latest_content_list': latest_content_list, 'featured': featured}
    return render(request, 'event.html', context)

def text(request):
    content = Content.objects.filter(type=5)
    return render(request, 'text.html', {'content': content})


def events(request, shortname):
    events = get_object_or_404(Content, shortname=shortname)
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type=0).order_by('-datestart')
    return render(request, 'events.html', {'events': events, 'latest_content_list': latest_content_list, 'gallery': gallery})

def projects(request, shortname):
    projects = get_object_or_404(Content, shortname=shortname)
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type=3)
    return render(request, 'projects.html', {'projects': projects, 'latest_content_list': latest_content_list, 'gallery':gallery})

def works(request, shortname):
    works = get_object_or_404(Content, shortname=shortname)
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type=4)
    return render(request, 'works.html', {'works': works, 'latest_content_list': latest_content_list, 'gallery':gallery})

def texts(request, shortname):
    texts = get_object_or_404(Content, shortname=shortname)
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type=5)
    return render(request, 'texts.html', {'texts': texts, 'latest_content_list': latest_content_list, 'gallery':gallery})


class GalleryListViews(ListView):
    queryset = Gallery.objects.on_site().is_public()
    paginate_by = 20
    template_name = 'gallery_list.html'

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None



