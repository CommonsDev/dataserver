import mimetypes
import os.path
import subprocess

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import FormMixin
from django.views.generic import View
from django.utils import simplejson as json
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

from sendfile import sendfile
from sorl.thumbnail import get_thumbnail

from .models import BucketFile
from .forms import BucketUploadForm

class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class ThumbnailView(View):
    """
    A view for generating thumbnails of documents, pictures and any
    other file supported.
    FIXME: THIS VIEW IS TERRIBLE: NO CACHE AND NOTHING!
    """
    preprocess_uno = ('application/vnd.oasis.opendocument.text',)
    
    def get(self, request, *args, **kwargs):
        file_id = self.kwargs['pk']
        preview_width = self.request.GET.get('width', "150")

        # Lookup bucket file first
        bfile = get_object_or_404(BucketFile, pk=file_id)
        target = bfile.file.name

        # Guess mimetype
        mimetype, encoding = mimetypes.guess_type(bfile.file.url)        
        
        # Convert document to PDF first, if needed
        if mimetype in ThumbnailView.preprocess_uno:
            target = '%s.pdf' % bfile.file.name
            conversion_cmd = "unoconv -f pdf -o %s %s" % (os.path.join(settings.MEDIA_ROOT, target),
                                                          os.path.join(settings.MEDIA_ROOT, bfile.file.name))
            subprocess.check_output(conversion_cmd.split())

        # Generate thumbnail
        try:
            thumbnail = get_thumbnail(target, preview_width, quality=80, format='JPEG')
        except Exception as e:
            raise e

        # Issue a X-Sendfile to the server
        fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
        return sendfile(request, fp)
                
class UploadView(JSONResponseMixin, FormMixin, View):
    """
    A generic HTML5 Upload view
    """
    form_class = BucketUploadForm
    template_name = 'multiuploader/form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES[u'file']
            wrapped_file = UploadedFile(file)
            
            # writing file manually into model
            # because we don't need form of any type.
            self.bf = BucketFile()
            self.bf.filename = wrapped_file.file.name
            self.bf.file_size = wrapped_file.file.size
            self.bf.file = file
            self.bf.bucket = form.cleaned_data['bucket']
            self.bf.save()
            
            return self.form_valid(form)            
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # generating json response array
        result = [{"id": self.bf.id,
                   "name": self.bf.filename,
                   "size": self.bf.file_size,
                   "url": reverse('multiuploader_file_link', args=[self.bf.pk]),
                   "thumbnail_url": reverse('bucket-thumbnail', args=[self.bf.pk]),
                   "delete_url": reverse('multiuploader_delete', args=[self.bf.pk]),
                   "delete_type": "POST", }]
        
        response_data = json.dumps(result)
        mimetype = 'application/json'
        return HttpResponse(response_data, mimetype=mimetype)            


