# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from models import *

'''
class SubdomainInline(admin.StackedInline):
    model = Subdomain
    
class DomainAliasInline(admin.StackedInline):
    model = DomainAlias
    
class ServerAdmin(admin.ModelAdmin):
    pass
'''

class ContentAdmin(admin.ModelAdmin):
    save_on_top = True
#    inlines = [SubdomainInline, DomainAliasInline]
#    list_display = ('url', 'server', 'manage_nameserver', 'domain_registrar', 'email', 'is_active')
#    list_editable = ('server', 'manage_nameserver', 'domain_registrar', 'email', 'is_active')


admin.site.register(Content, ContentAdmin)
