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
    past_events = base.filter(Q(dateend__lt=now) | Q(dateend=None, datestart__lt=now))[:12]

    homepage = Content.objects.filter(type__name='homepage').order_by('-datestart')[:1]
    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events,
        'homepage': homepage}
    return render(request, 'index.html', context)


SECTION_TYPE = {
    'Projects': ['projects'],
    'Works': ['works'],
    'Texts': ['texts'],
    'Events': ['events', 'news'],
}

def section_content(section):
    types = SECTION_TYPE.get(section, [section.lower()])
    content = Content.objects.filter(type__name__in=types).order_by('-datestart')
    content = content.filter(published=True)
    return content


def section_index(request, section):
    types = SECTION_TYPE.get(section, [section.lower()])
    featured = Content.objects.filter(type__name__in=types, featured=True).order_by('-datestart')[:1]
    content = section_content(section)
    if featured:
        content = content.exclude(pk=featured[0].pk)
    return render(request, 'section_index.html', {
        'section': section,
        'featured': featured,
        'content': content
    })


def section_list(request, section):
    content = section_content(section)

    q = request.GET.get('q')
    content = limit_content(content, q)

    page = request.GET.get('page', 1)
    paginator = Paginator(content, 5)
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    base_query = ''
    if q:
        base_query = 'q=%s&' % q

    return render(request, 'results.html', {
        'base_query': base_query,
        'content': content,
        'query': q,
        'section': section,
    })

def event(request):
    now = datetime.now()
    display_events = ['events', 'news']
    featured = Content.objects.filter(type__name='events', featured=True).order_by('-datestart')[:1]
    base = Content.objects.filter(type__name__in=display_events).order_by('-datestart')
    base = base.filter(published=True)
    if featured:
        base = base.exclude(pk=featured[0].pk)

    upcoming_events = base.filter(datestart__gt=now).order_by('-datestart')
    ongoing_events = base.filter(datestart__lt=now, dateend__gte=now).order_by('-datestart')
    past_events = base.filter(Q(dateend__lt=now) | Q(dateend=None, datestart__lt=now))[:10]

    context = {
        'upcoming_events': upcoming_events,
        'ongoing_events': ongoing_events,
        'past_events': past_events,
        'featured': featured,
        'section': 'Events',
    }
    return render(request, 'event.html', context)


def get_related_content(types, current=None, max_length=10):
    latest_content_list = Content.objects.filter(type__name__in=types).order_by('-datestart')
    if current:
        latest_content_list = latest_content_list.exclude(pk=current.pk)
    latest_content_list = latest_content_list.filter(published=True)
    more = latest_content_list.count > max_length
    latest_content_list = latest_content_list[:max_length]
    return latest_content_list, more


def render_content(request, shortname, section, template, types):
    if not shortname:
        if section == 'Events':
            return event(request)
        else:
            return section_index(request, section)
    content = get_object_or_404(Content, shortname=shortname, type__name__in=types)
    if not content.published and not request.user.is_staff:
        raise Http404
    latest_content_list, more = get_related_content(types, content)
    return render(request, template, {
        'content': content,
        'latest_content_list': latest_content_list,
        'has_more_content': more,
        'section': section,
    })


def events(request, shortname=None):
    return render_content(request, shortname, 'Events', 'content.html', ['events', 'news'])


def projects(request, shortname=None):
    return render_content(request, shortname, 'Projects', 'content.html', ['projects'])


def works(request, shortname=None):
    return render_content(request, shortname, 'Works', 'content.html', ['works'])


def texts(request, shortname=None):
    return render_content(requests, shortname, 'Texts', 'content.html', ['texts'])


def page(request, shortname):
    content = get_object_or_404(Content, shortname=shortname, type__name='page')
    if not content.published and not request.user.is_staff:
        raise Http404
    return render(request, 'page.html', {'content': content})


def limit_content(content, q):
    if q:
        content = content.filter(Q(body__icontains=q) | Q(title__icontains=q) | Q(header__icontains=q)).distinct()
    return content


def search(request):
    content = Content.objects.filter(published=True).order_by('-datestart')
    content = content.exclude(type__name__in=['page', 'homepage'])
    q = request.GET.get('q')
    content = limit_content(content, q)
    page = request.GET.get('page', 1)
    paginator = Paginator(content, 5)
    try:
        content = paginator.page(page)
    except PageNotAnInteger:
        content = paginator.page(1)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)

    base_query = ''
    if q:
        base_query = 'q=%s&' % q

    return render(request, 'results.html', {
        'base_query': base_query,
        'content': content,
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

