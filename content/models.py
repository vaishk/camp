# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.html import mark_safe

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import ox

# Create your models here.

class Acrolike(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        # managed = False
        db_table = 'acrolike'


class Acronym(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    c = models.CharField(max_length=50, blank=True, null=True)
    a = models.CharField(max_length=50, blank=True, null=True)
    m = models.CharField(max_length=50, blank=True, null=True)
    p = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'acronym'


class Audios(models.Model):
    filename = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'audios'



class Comments(models.Model): #not used
    comment = models.TextField()
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    personid = models.IntegerField(db_column='personID', blank=True, null=True)  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='dateAdded')  # Field name made lowercase.
    datemodified = models.DateTimeField(db_column='dateModified', blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='parentID', blank=True, null=True)  # Field name made lowercase.
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'comments'


class Content(models.Model):
    type = models.ForeignKey("ContentTypes", db_column="type")
    shortname = models.CharField(db_column='shortName', max_length=255)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    header = MarkdownxField(blank=True, null=True, default='')
    body = MarkdownxField(blank=True, null=True, default='')
    teaser = models.TextField(blank=True, null=True, validators=[MaxLengthValidator(200)])
    schedule = models.TextField(blank=True, null=True)    
    schedulebutton = models.CharField(db_column='scheduleButton', max_length=255, blank=True, null=True)  # Field name made lowercase.
    optbtn2 = models.CharField(db_column='optBtn2', max_length=127, blank=True, null=True)  # Field name made lowercase.
    opttext2 = models.TextField(db_column='optText2', blank=True, null=True)  # Field name made lowercase.
    optbtn3 = models.CharField(db_column='optBtn3', max_length=127, blank=True, null=True)  # Field name made lowercase.
    opttext3 = models.TextField(db_column='optText3', blank=True, null=True)  # Field name made lowercase.
    technotes = models.TextField(db_column='technotes', blank=True, null=True)
    image = models.CharField(max_length=150, blank=True, null=True)
    postedby = models.CharField(db_column='postedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datestart = models.DateField(db_column='dateStart', blank=True, null=True)  # Field name made lowercase.
    dateend = models.DateField(db_column='dateEnd', blank=True, null=True)  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='dateAdded', auto_now_add=True, editable=True)  # Field name made lowercase.
    datemodified = models.DateTimeField(db_column='dateModified', blank=True, null=True, auto_now=True)  # Field name made lowercase.
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    view = models.ForeignKey("Views", null=True, blank=True, db_column="view", editable=False)
    place = models.CharField(max_length=255, null=True, blank=True)
    parentid = models.IntegerField(null=True, db_column='parentID', blank=True, editable=False) # delete
    parents = models.ManyToManyField('Content', through='ContentContent', related_name= "children")

    def __unicode__(self):
        return self.title

    @property
    def formatted_header(self):
        return mark_safe(markdownify(self.header))

    @property
    def formatted_body(self):
        return mark_safe(markdownify(self.body))

    @property
    def formatted_teaser(self):
        if self.teaser:
            value = self.teaser
        elif self.header:
            value = ox.strip_tags(ox.decode_html(self.header))[:100]
        else:
            value = ''
        return mark_safe(value)

    @property
    def typefilter(self):
        return self.type

    @property
    def image_url(self):
        if self.image:
            return settings.IMAGE_PREFIX + self.image

    def get_absolute_url(self):
        if self.shortname:
            parts = []
            section = self.type.name
            if section == 'news':
                section = 'events'
            if section == 'page':
                parts = [self.shortname]
            else:
                parts = [section, self.shortname]
            return '/' + '/'.join(parts)

    class Meta:
        managed = True
        db_table = 'content'


class ContentContent(models.Model):
    contentid1 = models.ForeignKey("content", db_column='contentID1', related_name="child")  # Field name made lowercase.
    contentid2 = models.ForeignKey("content", db_column='contentID2', related_name="parent")  # Field name made lowercase.

    def __unicode__(self):
        return self.contentid1.title

    class Meta:
        # managed = False
        db_table = 'content_content'

    def reverse(self):
        r, created = ContentContent.objects.get_or_create(contentid1=self.contentid2, contentid2=self.contentid1)
        return r

    def save(self, *args, **kwargs):
        super(ContentContent, self).save(*args, **kwargs)
        self.reverse()

class ContentKeyword(models.Model):
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    keywordid = models.IntegerField(db_column='keywordID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'content_keyword'


class ContentResource(models.Model):
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    resourceid = models.IntegerField(db_column='resourceID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'content_resource'


class ContentTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name             

    class Meta:
        # managed = False
        db_table = 'content_types'


class Keywords(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'keywords'


class People(models.Model): #not used
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'people'


class PersonContent(models.Model):
    personid = models.IntegerField(db_column='personID')  # Field name made lowercase.
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    level = models.IntegerField()

    class Meta:
        # managed = False
        db_table = 'person_content'


class PersonResource(models.Model):
    personid = models.IntegerField(db_column='personID')  # Field name made lowercase.
    resourceid = models.IntegerField(db_column='resourceID')  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'person_resource'


class Resources(models.Model):
    type = models.IntegerField()
    href = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mime = models.CharField(max_length=10, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    istech = models.IntegerField(db_column='isTech')  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='dateAdded', null=True, blank=True)  # Field name made lowercase.
    orderno = models.IntegerField(db_column='orderNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'resources'

class File(models.Model):
    content = models.ForeignKey('Content')
    fil = models.FileField(upload_to='files')
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(blank=True, null=True)

class Image(models.Model):
    content = models.ForeignKey('Content', related_name='images')
    image = models.ImageField(upload_to='camp/static/images')
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(blank=True, null=True)

class Link(models.Model):
    content = models.ForeignKey('Content')
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(blank=True, null=True)

class Videos(models.Model): # not used
    sha1 = models.CharField(max_length=50)
    href = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    thumbno = models.IntegerField(db_column='thumbNo')  # Field name made lowercase.
    image = models.CharField(max_length=255, blank=True, null=True)
    contentid = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'videos'


class Views(models.Model):
    name = models.CharField(max_length=255)
    href = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        # managed = False
        db_table = 'views'


class MyModel(models.Model):
    myfield = MarkdownxField()



