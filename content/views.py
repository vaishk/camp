# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Content


def index(request):
    latest_content_list = Content.objects.order_by('-datestart')[:5]
    context = {'latest_content_list': latest_content_list}
    return render(request, 'index.html', context)

def content(request, shortname):
    content = get_object_or_404(Content, shortname=shortname)
    return render(request, 'detail.html', {'content': content})

def projects(request):
    content = Content.objects.filter(type__name='ongoing').exclude(shortname='').order_by('-datestart')
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Projects'
    })

def events(request):
    content = Content.objects.filter(type__name='events').exclude(shortname='')
    content = Content.objects.filter(type__name='events').exclude(shortname='').order_by('-datestart')
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Upcoming Events'
    })

def works(request):
    content = Content.objects.filter(type__name='works').exclude(shortname='').order_by('-datestart')
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Works'
    })

def texts(request):
    content = Content.objects.filter(type__name='texts').exclude(shortname='')
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Texts'
    })

def about(request):
    content = get_object_or_404(Content, shortname='about')
    return render(request, 'detail.html', {'content': content})

def contact(request):
    content = get_object_or_404(Content, shortname='contact')
    return render(request, 'detail.html', {'content': content})


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
