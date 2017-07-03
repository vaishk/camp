# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Content
from django.db.models import Q
from django.views.generic.list import ListView
from photologue.views import GalleryListView 
from photologue.models import Photo, Gallery
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index(request):
    latest_content_list = Content.objects.order_by('-datestart')[:8]
    context = {'latest_content_list': latest_content_list}
    return render(request, 'index.html', context)

def project(request):
    content = Content.objects.filter(type=3)
    return render(request, 'project.html', {'content': content})

def events(request, shortname):
	events = get_object_or_404(Content, shortname=shortname)
	gallery = get_or_none(Gallery, slug=shortname)
	latest_content_list = Content.objects.filter(Q(type=0) | Q(type=1)).order_by('-datestart')
	return render(request, 'events.html', {'events': events, 'latest_content_list': latest_content_list, 'gallery': gallery})

def projects(request, shortname):
	projects = get_object_or_404(Content, shortname=shortname)
	latest_content_list = Content.objects.filter(type=3)
	return render(request, 'projects.html', {'projects': projects, 'latest_content_list': latest_content_list})

class GalleryListViews(ListView):
    queryset = Gallery.objects.on_site().is_public()
    paginate_by = 20
    template_name = 'gallery_list.html'

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None



