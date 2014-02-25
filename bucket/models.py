import os
import time
from hashlib import sha1

from django.conf import settings
from django.db import models
from django.utils.text import get_valid_filename

from userena.utils import get_profile_model

from taggit.managers import TaggableManager

class Bucket(models.Model):
    pass

    def __unicode__(self):
        return u"Bucket with %d objects" % len(self.files.all())


        
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
    uploaded_by = models.ForeignKey(get_profile_model())

    def _upload_to(instance, filename):
        upload_path = getattr(settings, 'BUCKET_FILES_FOLDER')

        if upload_path[-1] != '/':
            upload_path += '/'

        filename = get_valid_filename(os.path.basename(filename))
        filename, ext = os.path.splitext(filename)
        hash = sha1(str(time.time())).hexdigest()
        fullname = os.path.join(upload_path, "%s.%s%s" % (filename, hash, ext))
        return fullname
    
    file = models.FileField(upload_to=_upload_to, max_length=255)
    thumbnail_url = models.CharField(max_length=2048)


class BucketFileComment(models.Model):
    """
    A comment on a file
    """
    bucket_file = models.ForeignKey(BucketFile, related_name='comments')
    submitter = models.ForeignKey(get_profile_model())
    submitted_on = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


    def __unicode__(self):
        return "%s on %s (%s)" % (self.text,
                                  self.bucket_file,
                                  self.submitter)
    
