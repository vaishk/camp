# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.urls import reverse


class Content(models.Model):
    published = models.BooleanField(default=False)
    view = models.ForeignKey("Views", null=True, blank=True, db_column="view")
    parent = models.ForeignKey('Content', null=True, blank=True, related_name='children', db_index=True, db_column='parentId')

    type = models.ForeignKey("ContentTypes", db_column="type")
    shortname = models.CharField(db_column='shortName', max_length=255)
    title = models.CharField(max_length=255)
    header = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)    
    schedulebutton = models.CharField(db_column='scheduleButton', max_length=255, blank=True, null=True)
    optbtn2 = models.CharField(db_column='optBtn2', max_length=127, blank=True, null=True)
    opttext2 = models.TextField(db_column='optText2', blank=True, null=True)
    optbtn3 = models.CharField(db_column='optBtn3', max_length=127, blank=True, null=True)
    opttext3 = models.TextField(db_column='optText3', blank=True, null=True)
    technotes = models.TextField(db_column='technotes', blank=True, null=True)
    image = models.CharField(max_length=150, blank=True, null=True)
    postedby = models.CharField(db_column='postedBy', max_length=50, blank=True, null=True)
    datestart = models.DateField(db_column='dateStart', blank=True, null=True)
    dateend = models.DateField(db_column='dateEnd', blank=True, null=True)
    dateadded = models.DateTimeField(db_column='dateAdded', auto_now_add=True, null=True)
    datemodified = models.DateTimeField(db_column='dateModified', blank=True, null=True, auto_now=True)

    place = models.CharField(max_length=255, null=True, blank=True)

    resources = models.ManyToManyField('Resources', through='ContentResource', related_name="content")

    def __unicode__(self):
        return self.title or 'Untitled'

    class Meta:
        db_table = 'content'

    @property
    def image_url(self):
        if self.image:
            return settings.IMAGE_PREFIX + self.image

    def get_absolute_url(self):
        if self.shortname:
            return reverse('content', kwargs={'shortname': self.shortname})

    def links(self):
        return self.resources.filter(type=3).order_by('orderno')

    def images(self):
        return self.resources.filter(type=2).exclude(href=self.image).order_by('orderno')

class Resources(models.Model):

    TYPE_CHOICES = (
        (1, "Resources"),
        (2, "Images"),
        (3, "Links"),
    )

    type = models.IntegerField(choices=TYPE_CHOICES)
    href = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mime = models.CharField(max_length=10, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    istech = models.BooleanField(db_column='isTech')
    dateadded = models.DateTimeField(db_column='dateAdded', auto_now_add=True, null=True)
    orderno = models.IntegerField(db_column='orderNo', blank=True, null=True)

    def __unicode__(self):
        return self.href

    def get_absolute_url(self):
        href = self.href
        if not href.startswith('http') and not href.startswith('/'):
            href = '/' + href
        if href.startswith('/'):
            href = 'https://studio.camp' + href
        return href

    @property
    def is_image(self):
        if self.mime:
            return self.mime.lower() in ('gif', 'jpeg', 'jpg', 'png')

    @property
    def is_audio(self):
        if self.mime:
            return self.mime.lower() in ('mp3', 'ogg')

    @property
    def is_video(self):
        if self.mime:
            return self.mime.lower() in ('ogv', 'mp4')

    class Meta:
        db_table = 'resources'

'''
class ContentContent(models.Model):
    contentid1 = models.ForeignKey('Content', db_column='contentID1', related_name='child')
    contentid2 = models.ForeignKey('Content', db_column='contentID2', related_name='parent')

    def __unicode__(self):
        return "%s is child of %s" % (self.contentid1.title, self.contentid2.title,)

    class Meta:
        managed = False
        db_table = 'content_content'
'''

class ContentResource(models.Model):
    content = models.ForeignKey('Content', db_column='contentID')
    resource = models.ForeignKey('Resources', db_column='resourceID')

    def __unicode__(self):
        return self.resource.href

    class Meta:
        db_table = 'content_resource'


class ContentTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'content_types'


class Views(models.Model):
    name = models.CharField(max_length=255)
    href = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'views'

# unused but has values in db

class Acrolike(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        db_table = 'acrolike'


class Acronym(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    c = models.CharField(max_length=50, blank=True, null=True)
    a = models.CharField(max_length=50, blank=True, null=True)
    m = models.CharField(max_length=50, blank=True, null=True)
    p = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'acronym'

class People(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    type = models.IntegerField()

    resources = models.ManyToManyField('Resources', through='PersonResource', related_name='people')
    content = models.ManyToManyField('Content', through='PersonContent', related_name='people')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'people'


class PersonContent(models.Model):
    personid = models.ForeignKey("people", db_column="personID")
    contentid = models.ForeignKey("content", db_column="contentID")
    level = models.IntegerField()

    class Meta:
        db_table = 'person_content'


class PersonResource(models.Model):
    personid = models.ForeignKey("people", db_column="personID")
    resourceid = models.ForeignKey("resources", db_column="resourceID")

    class Meta:
        db_table = 'person_resource'


class Videos(models.Model):
    sha1 = models.CharField(max_length=50)
    href = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    thumbno = models.IntegerField(db_column='thumbNo')
    image = models.CharField(max_length=255, blank=True, null=True)
    contentid = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'videos'

    def image_url(self):
        return settings.IMAGE_PREFIX + self.image


# UNUSED

class Audios(models.Model):
    filename = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'audios'


class Comments(models.Model):
    comment = models.TextField()
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    personid = models.IntegerField(db_column='personID', blank=True, null=True)
    dateadded = models.DateTimeField(db_column='dateAdded', auto_now_add=True, null=True)
    datemodified = models.DateTimeField(db_column='dateModified', blank=True, null=True, auto_now=True)
    parentid = models.IntegerField(db_column='parentID', blank=True, null=True)
    parent = models.ForeignKey('Comments', null=True, blank=True, related_name='comments', db_index=True, db_column='parentId')
    content = models.ForeignKey('Content', null=True, blank=True, related_name='comments', db_index=True, db_column='contentID')
    ip = models.CharField(db_column='IP', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'comments'


class Keywords(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'keywords'

class ContentKeyword(models.Model):
    content = models.ForeignKey('Content', db_column='contentID')
    keyword = models.ForeignKey('Keywords', db_column='keywordID')

    class Meta:
        db_table = 'content_keyword'


