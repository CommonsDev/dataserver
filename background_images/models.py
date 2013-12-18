import uuid
import os

from django.db import models
from cms.models import CMSPlugin

def get_picture_path(aPicture, filename):
    """
    Generate a random UUID for a picture,
    use the uuid as the track name
    """
    track_uuid = uuid.uuid4()
    name, extension = os.path.splitext(filename)

    dst = 'cms_background_images_media/%s%s' % (track_uuid,extension)
    return dst

class BackgroundImagesPlugin(CMSPlugin):
    image1 = models.ImageField(upload_to=get_picture_path, blank=True, null=True)
    image2 = models.ImageField(upload_to=get_picture_path, blank=True, null=True)
    image3 = models.ImageField(upload_to=get_picture_path, blank=True, null=True)
