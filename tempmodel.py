# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Acrolike(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'acrolike'


class Acronym(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    c = models.CharField(max_length=50, blank=True, null=True)
    a = models.CharField(max_length=50, blank=True, null=True)
    m = models.CharField(max_length=50, blank=True, null=True)
    p = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'acronym'


class Audios(models.Model):
    filename = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audios'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=50)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    password = models.CharField(max_length=128)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    is_superuser = models.IntegerField()
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Comments(models.Model):
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
        managed = False
        db_table = 'comments'


class Content(models.Model):
    shortname = models.CharField(db_column='shortName', max_length=255)  # Field name made lowercase.
    title = models.CharField(max_length=255)
    header = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)
    schedulebutton = models.CharField(db_column='scheduleButton', max_length=255, blank=True, null=True)  # Field name made lowercase.
    optbtn2 = models.CharField(db_column='optBtn2', max_length=127, blank=True, null=True)  # Field name made lowercase.
    opttext2 = models.TextField(db_column='optText2', blank=True, null=True)  # Field name made lowercase.
    optbtn3 = models.CharField(db_column='optBtn3', max_length=127, blank=True, null=True)  # Field name made lowercase.
    opttext3 = models.TextField(db_column='optText3', blank=True, null=True)  # Field name made lowercase.
    technotes = models.TextField()
    image = models.CharField(max_length=150, blank=True, null=True)
    postedby = models.CharField(db_column='postedBy', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datestart = models.DateField(db_column='dateStart', blank=True, null=True)  # Field name made lowercase.
    dateend = models.DateField(db_column='dateEnd', blank=True, null=True)  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='dateAdded')  # Field name made lowercase.
    datemodified = models.DateTimeField(db_column='dateModified', blank=True, null=True)  # Field name made lowercase.
    type = models.IntegerField()
    published = models.IntegerField()
    view = models.IntegerField(blank=True, null=True)
    parentid = models.IntegerField(db_column='parentId')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'content'


class ContentContent(models.Model):
    contentid1 = models.IntegerField(db_column='contentID1')  # Field name made lowercase.
    contentid2 = models.IntegerField(db_column='contentID2')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'content_content'


class ContentKeyword(models.Model):
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    keywordid = models.IntegerField(db_column='keywordID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'content_keyword'


class ContentResource(models.Model):
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    resourceid = models.IntegerField(db_column='resourceID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'content_resource'


class ContentTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_types'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    user_id = models.IntegerField()
    content_type_id = models.IntegerField(blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Keywords(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


class People(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=16, blank=True, null=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'people'


class PersonContent(models.Model):
    personid = models.IntegerField(db_column='personID')  # Field name made lowercase.
    contentid = models.IntegerField(db_column='contentID')  # Field name made lowercase.
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'person_content'


class PersonResource(models.Model):
    personid = models.IntegerField(db_column='personID')  # Field name made lowercase.
    resourceid = models.IntegerField(db_column='resourceID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'person_resource'


class Resources(models.Model):
    type = models.IntegerField()
    href = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mime = models.CharField(max_length=10, blank=True, null=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    istech = models.IntegerField(db_column='isTech')  # Field name made lowercase.
    dateadded = models.DateTimeField(db_column='dateAdded')  # Field name made lowercase.
    orderno = models.IntegerField(db_column='orderNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'resources'


class Videos(models.Model):
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
        managed = False
        db_table = 'videos'


class Views(models.Model):
    name = models.CharField(max_length=255)
    href = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'views'
