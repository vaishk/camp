# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from photologue.views import GalleryListView 
from photologue.models import Photo, Gallery

from .models import Content, ContentContent

# Create your views here.

def index(request):
    now = datetime.now()
    display_events = ['news', 'events']
    base = Content.objects.filter(type__name__in=display_events).order_by('-datestart')
    base = base.filter(published=True)
    upcoming_events = base.filter(datestart__gt=now)[:12]
    ongoing_events = base.filter(datestart__lt=now, dateend__gte=now)[:12]
    past_events = base.filter(Q(dateend__lt=now)|Q(dateend=None, datestart__lt=now))[:12]

    homepage = Content.objects.filter(type__name='homepage').order_by('-datestart')[:1]
    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events,
        'homepage': homepage}
    return render(request, 'index.html', context)


def section_index(request, types, section):
    featured = Content.objects.filter(type__name__in=types, featured=True).order_by('-datestart')[:1]
    content = Content.objects.filter(type__name__in=types).order_by('-datestart')
    if featured:
        content = content.exclude(pk=featured[0].pk)
    content = content.filter(published=True)
    return render(request, 'section_index.html', {
        'section': section,
        'featured': featured,
        'content': content
    })

def event(request):
    now = datetime.now()
    display_events = ['events']
    featured = Content.objects.filter(type__name='events', featured=True).order_by('-datestart')[:1]
    base = Content.objects.filter(type__name__in=display_events).order_by('-datestart')
    base = base.filter(published=True)
    if featured:
        base = base.exclude(pk=featured[0].pk)

    upcoming_events = base.filter(datestart__gt=now).order_by('-datestart')
    ongoing_events = base.filter(datestart__lt=now, dateend__gte=now).order_by('-datestart')
    past_events = base.filter(Q(dateend__lt=now)|Q(dateend=None, datestart__lt=now))[:10]

    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events,
        'featured': featured,
    }
    return render(request, 'event.html', context)


def events(request, shortname=None):
    if not shortname:
        return event(request)
    events = get_object_or_404(Content, shortname=shortname, type__name__in=['news', 'events'])
    if not events.published and not request.user.is_staff:
        raise Http404
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='events').order_by('-datestart')[:10]
    return render(request, 'events.html', {'events': events, 'latest_content_list': latest_content_list, 'gallery': gallery})

def projects(request, shortname=None):
    if not shortname:
        return section_index(request, ['projects'], 'Projects')
    projects = get_object_or_404(Content, shortname=shortname, type__name='projects')
    if not projects.published and not request.user.is_staff:
        raise Http404
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='projects').order_by('-datestart')
    return render(request, 'projects.html', {
        'projects': projects,
        'latest_content_list': latest_content_list,
        'gallery': gallery
    })

def works(request, shortname=None):
    if not shortname:
        return section_index(request, ['works'], 'Works')
    works = get_object_or_404(Content, shortname=shortname, type__name='works')
    if not works.published and not request.user.is_staff:
        raise Http404
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='works')
    return render(request, 'works.html', {'works': works, 'latest_content_list': latest_content_list, 'gallery':gallery})

def texts(request, shortname=None):
    if not shortname:
        return section_index(request, ['texts'], 'Texts')
    texts = get_object_or_404(Content, shortname=shortname, type__name='texts')
    gallery = get_or_none(Gallery, slug=shortname)
    latest_content_list = Content.objects.filter(type__name='texts')
    return render(request, 'texts.html', {
        'texts': texts,
        'latest_content_list': latest_content_list,
        'gallery': gallery
    })


def page(request, shortname):
    content = get_object_or_404(Content, shortname=shortname, type__name='page')
    if not content.published and not request.user.is_staff:
        raise Http404
    return render(request, 'page.html', {'content': content})


def search(request):
    q = request.GET.get('q')
    results = Content.objects.filter(Q(body__icontains=q) | Q(title__icontains=q) | Q(header__icontains=q)).distinct()
    results = results.filter(published=True)
    results = results.order_by('-datestart')
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 5)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    return render(request, 'results.html', {
        'results': results,
        'query': q
    })


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
        content = get_object_or_404(Content, shortname=shortname)
        return redirect(content.get_absolute_url())
    id = request.GET.get('id')
    if id:
        content = get_object_or_404(Content, id=id)
        return redirect(content.get_absolute_url())

    return redirect(reverse('events'))

def redirect_images(request, image):
    return redirect(image)

