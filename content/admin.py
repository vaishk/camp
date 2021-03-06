# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery

from .models import *

class ContentParentsInline(admin.TabularInline):
    model = ContentContent
    fk_name = 'contentid2'
    raw_id_fields = ['contentid1']
    extra = 0

class ImagesInline(admin.StackedInline):
    extra = 0
    model = Image

class FileInline(admin.StackedInline):
    extra = 0
    model = File

class LinkInline(admin.StackedInline):
    extra = 0
    model = Link

'''
class SubdomainInline(admin.StackedInline):
    model = Subdomain
    
class DomainAliasInline(admin.StackedInline):
    model = DomainAlias
    
class ServerAdmin(admin.ModelAdmin):
    pass
'''

class MaxLengthAdminMarkdownxWidget(AdminMarkdownxWidget):
    def get_context(self, name, value, attrs=None):
        if name == 'teaser':
            if not attrs:
                attrs = {}
            attrs['maxlength'] = 250
            print(dir(self))
        return super(MaxLengthAdminMarkdownxWidget, self).get_context(name, value, attrs)

    class Media:
        js = (
            'js/maxlength_count.js',
        )

class GalleryAdminForm(forms.ModelForm):
    """Users never need to enter a description on a gallery."""

    class Meta:
        model = Gallery
        exclude = ['description']


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm

class ContentAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id', '__str__', 'datestart', 'shortname', 'type')
    list_filter = ['datestart', 'type']
    search_fields = ['title', 'body', 'header', 'shortname']
    raw_id_fields = ['photo']
    inlines = [ContentParentsInline, FileInline, LinkInline]
    formfield_overrides = {
        models.TextField: {'widget': MaxLengthAdminMarkdownxWidget},
    }


admin.site.register(Content, ContentAdmin)
admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)

