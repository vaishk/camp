# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from .models import Content


def index(request):
    content = Content.objects.all()
    content = content.filter(published=True)
    latest_content_list = content.order_by('-datestart')[:5]
    context = {'latest_content_list': latest_content_list}
    return render(request, 'index.html', context)

def content(request, shortname):
    if request.user.is_staff:
        content = get_object_or_404(Content, shortname=shortname)
    else:
        content = get_object_or_404(Content, shortname=shortname, published=True)
    return render(request, 'detail.html', {'content': content})

def projects(request):
    content = Content.objects.filter(type__name='ongoing').exclude(shortname='').order_by('-datestart')
    content = content.filter(published=True)
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Projects'
    })

def events(request):
    content = Content.objects.filter(type__name='events').exclude(shortname='')
    content = Content.objects.filter(type__name='events').exclude(shortname='').order_by('-datestart')
    content = content.filter(published=True)
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Upcoming Events'
    })

def works(request):
    content = Content.objects.filter(type__name='works').exclude(shortname='').order_by('-datestart')
    content = content.filter(published=True)
    return render(request, 'projects.html', {
        'content': content,
        'title': 'Works'
    })

def texts(request):
    content = Content.objects.filter(type__name='texts').exclude(shortname='')
    content = content.filter(published=True)
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

def redirect_images(request, image):
    return redirect(image)

