import os
import re
import uuid

def calculate_image_path(instance, filename):
    """ 
    Calculate the path for image to be stored 
    """ 
    track_uuid = uuid.uuid4()
    name, extension = os.path.splitext(filename)

    dst = 'cms_news_media/%s%s' % (track_uuid,extension)
    return dst
