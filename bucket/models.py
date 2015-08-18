import os
import time
from hashlib import sha1

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import get_valid_filename
from django.utils.translation import ugettext as _

from guardian.shortcuts import assign_perm

from taggit.managers import TaggableManager


class Bucket(models.Model):
    """
    A bucket is a collection of files
    """
    class Meta:
        permissions = (
            ('view_bucket', _("View Bucket")),
        )

    created_by = models.ForeignKey(User, related_name='buckets_created')
    name = models.CharField(max_length=200, verbose_name=_("name"))

    def __unicode__(self):
        return u"Bucket %s with %d objects" % (self.name, len(self.files.all()))


class BucketFile(models.Model):
    """
    A file contained in a bucket
    """
    bucket = models.ForeignKey(Bucket, related_name='files')
    tags = TaggableManager(blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    filename = models.CharField(max_length=2048, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, related_name='uploader_of')
    being_edited_by = models.ForeignKey(User, null=True,
                                        related_name='editor_of')
    license = models.CharField(max_length=128, null=True, blank=True)
    author = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return u"File  %s from bucket %s" % (self.filename, self.bucket.name)

    def _upload_to(instance, filename):
        upload_path = getattr(settings, 'BUCKET_FILES_FOLDER')

        if upload_path[-1] != '/':
            upload_path += '/'

        filename = get_valid_filename(os.path.basename(filename))
        filename, ext = os.path.splitext(filename)
        hash = sha1(str(time.time())).hexdigest()
        fullname = os.path.join(upload_path, "%s%s" % (hash, ext))
        return fullname

    file = models.FileField(upload_to=_upload_to, max_length=255)
    thumbnail_url = models.CharField(max_length=2048)


class BucketFileComment(models.Model):
    """
    A comment on a file
    """
    bucket_file = models.ForeignKey(BucketFile, related_name='comments')
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


    def __unicode__(self):
        return "%s on %s (%s)" % (self.text,
                                  self.bucket_file,
                                  self.submitter)

@receiver(post_save, sender=Bucket)
def allow_user_to_edit_buckets(sender, instance, created, *args, **kwargs):
    assign_perm("view_bucket", user_or_group=instance.created_by, obj=instance)
    assign_perm("change_bucket", user_or_group=instance.created_by, obj=instance)
    assign_perm("delete_bucket", user_or_group=instance.created_by, obj=instance)


@receiver(post_save, sender=User)
def allow_user_to_create_bucket_via_api(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("bucket.add_bucket", instance)
