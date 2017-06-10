# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Content

# Create your views here.

def index(request):
    latest_content_list = Content.objects.order_by('-datestart')[:5]
    context = {'latest_content_list': latest_content_list}
    return render(request, 'index.html', context)

def content(request, shortname):
    content = get_object_or_404(Content, shortname = shortname)
    return render(request, 'detail.html', {'content': content})

def project(request):
    content = Content.objects.filter(type=3)
    return render(request, 'project.html', {'content': content})