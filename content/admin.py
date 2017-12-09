# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from . import models

'''
class SubdomainInline(admin.StackedInline):
    model = Subdomain
    
class DomainAliasInline(admin.StackedInline):
    model = DomainAlias
    
class ServerAdmin(admin.ModelAdmin):
    pass
'''

class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'type', 'mime')
    search_fields = ['href']
    list_filter = ['type', 'mime']

admin.site.register(models.Resources, ResourcesAdmin)


class ResourcesInline(admin.StackedInline):
    model = models.ContentResource
    extra = 2 # how many rows to show


class ContentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('__unicode__', 'datestart', 'type')
    list_filter = ['datestart', 'type', 'view', 'published']
    search_fields = ['title', 'body', 'header']
    raw_id_fields = ['parent']

    inlines = (ResourcesInline,)

#    inlines = [SubdomainInline, DomainAliasInline]
#    list_display = ('url', 'server', 'manage_nameserver', 'domain_registrar', 'email', 'is_active')
#    list_editable = ('server', 'manage_nameserver', 'domain_registrar', 'email', 'is_active')


admin.site.register(models.Content, ContentAdmin)
