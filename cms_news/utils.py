import os
import re

def calculate_image_path(instance, filename):
    ''' Calculate the path for image to be stored '''
    
    def normalizePath(path):
        return re.compile('[ ]').sub('-', re.compile('[/:.()<>|?*]|(\\\)').sub('', path))

    extension = os.path.splitext(filename)[1]
    filename = os.path.join(str(instance.id) + '-' + normalizePath(instance.title) + extension)
    full_path = os.path.join('news_pictures', filename)
    
    return full_path
