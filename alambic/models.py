from django.db import models

from bucket.models import Bucket
from flipflop.models import Board

class Room(models.Model):
    """
    A room holds anything related to a topic such as an xmpp room,
    a file bucket, ...
    """
    name = models.CharField(max_length=500, unique=True)
    bucket = models.OneToOneField(Bucket, related_name='room')
    issue_tracker = models.OneToOneField(Board, related_name='room', null=True, blank=True)

    def __unicode__(self):
        return self.name
    
    def save(self, **kwargs):
        """
        Automatically create a bucket if none is linked
        """
        try:
            self.bucket != None
        except Bucket.DoesNotExist:
            self.bucket = Bucket.objects.create()
            
        return super(Room, self).save(**kwargs)
