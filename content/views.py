# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.list import ListView

from photologue.views import GalleryListView 
from photologue.models import Photo, Gallery

from .models import Content, ContentContent

# Create your views here.

def index(request):
    now = datetime.now()
    display_events = ['news', 'events']
    upcoming_events = Content.objects.filter(datestart__gt=now).filter(type__name__in=display_events).order_by('-datestart')[:12]
    ongoing_events = Content.objects.filter(datestart__lt=now, dateend__gte=now).filter(type__name__in=display_events).order_by('-datestart')[:12]
    past_events = Content.objects.filter(dateend__lt=now).filter(type__name__in=display_events).order_by('-datestart')[:12]
    homepage = Content.objects.filter(type__name='homepage').order_by('-datestart')[:1]
    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events,
        'homepage': homepage}
    return render(request, 'index.html', context)

def project(request):
    type = 'projects'
    featured = Content.objects.filter(type__name=type, featured=True).order_by('-datestart')[:1]
    content = Content.objects.filter(type__name=type).order_by('-datestart')
    return render(request, 'section_index.html', {
        'section': 'Projects',
        'featured': featured,
        'content': content
    })

def work(request):
    type = 'works'
    featured = Content.objects.filter(type__name=type, featured=True).order_by('-datestart')[:1]
    content = Content.objects.filter(type__name=type).order_by('-datestart')
    return render(request, 'section_index.html', {
        'section': 'Works',
        'featured': featured,
        'content': content
    })

def event(request):
    now = datetime.now()
    display_events = ['events']
    upcoming_events = Content.objects.filter(datestart__gt=now).filter(type__name__in=display_events).order_by('-datestart')
    ongoing_events = Content.objects.filter(datestart__lt=now, dateend__gte=now).filter(type__name__in=display_events).order_by('-datestart')
    past_events = Content.objects.filter(Q(dateend__lt=now)|Q(dateend=None, datestart__lt=now)).filter(type__name__in=display_events).order_by('-datestart')[:10]

    featured = Content.objects.filter(type__name='events', featured=True).order_by('-datestart')[:1]
    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events,
        'featured': featured,
    }
    return render(request, 'event.html', context)

def text(request):
    type = 'texts'
    featured = Content.objects.filter(type__name=type, featured=True).order_by('-datestart')[:1]
    content = Content.objects.filter(type__name=type).order_by('-datestart')
    return render(request, 'section_index.html', {
        'section': 'Texts',
        'featured': featured,
        'content': content
    })


def events(request, shortname):
    if not shortname:
        return event(request)
    events = get_object_or_404(Content, shortname=shortname, type__name__in=['news', 'events'])
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='events').order_by('-datestart')[:10]
    return render(request, 'events.html', {'events': events, 'latest_content_list': latest_content_list, 'gallery': gallery})

def projects(request, shortname):
    if not shortname:
        return project(request)
    projects = get_object_or_404(Content, shortname=shortname, type__name='projects')
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='projects').order_by('-datestart')
    return render(request, 'projects.html', {'projects': projects, 'latest_content_list': latest_content_list, 'gallery':gallery})

def works(request, shortname):
    if not shortname:
        return work(request)
    works = get_object_or_404(Content, shortname=shortname, type__name='works')
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='works')
    return render(request, 'works.html', {'works': works, 'latest_content_list': latest_content_list, 'gallery':gallery})

def texts(request, shortname):
    if not shortname:
        return text(request)
    texts = get_object_or_404(Content, shortname=shortname, type__name='texts')
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='texts')
    return render(request, 'texts.html', {
        'texts': texts,
        'latest_content_list': latest_content_list,
        'gallery':gallery
    })


def page(request, shortname):
    content = get_object_or_404(Content, shortname=shortname, type__name='page')
    return render(request, 'page.html', {'content': content})


def search(request):
    q = request.GET.get('q')
    results = Content.objects.filter(body__contains=q).order_by('-datestart')
    return render(request, 'results.html', {'results': results})


class GalleryListViews(ListView):
    queryset = Gallery.objects.on_site().is_public()
    paginate_by = 20
    template_name = 'gallery_list.html'

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None


def redirect_index(request):
    segment = request.GET.get('show')
    if segment == 'pastevents':
        return redirect(reverse('works'))
    elif segment == 'contact':
        return redirect(reverse('contact'))
    return redirect(reverse('index'))

def redirect_event(request):
    shortname = request.GET.get('this')
    if shortname:
        return redirect(reverse('content', kwargs={'shortname': shortname}))
    id = request.GET.get('id')
    if id:
        content = get_object_or_404(Content, id=id)
        return redirect(reverse('content', kwargs={'shortname': content.shortname}))

    return redirect(reverse('events'))

def redirect_images(request, image):
    return redirect(image)

