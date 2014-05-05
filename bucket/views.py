import mimetypes
import os.path
import subprocess

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
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

from .api import BucketFileResource

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
    preprocess_uno = ('application/vnd.oasis.opendocument.text', 'application/msword', 'application/vnd.ms-excel', 'application/vnd.ms-powerpoint')
    
    def get(self, request, *args, **kwargs):
        file_id = self.kwargs['pk']
        preview_width = self.request.GET.get('width', "150")

        # Lookup bucket file first
        bfile = get_object_or_404(BucketFile, pk=file_id)
        # FIXME1: BUG in Tastypie causes file/image fields to be reconstructed with absolute path when PATCHing a file (see https://gist.github.com/ratpik/6308307)
        # so we strip off the /media/ if present
        if bfile.file.name[0:6] == "/media":
            bfile.file.name = bfile.file.name[7:]
        target = bfile.file.name
        # Guess mimetype
        mimetype, encoding = mimetypes.guess_type(bfile.file.url)

        # Convert document to PDF first, if needed
        # FIXME2: bug when several files are loaded => clashes 
        if mimetype in ThumbnailView.preprocess_uno:
            target = '%s.pdf' % bfile.file.name
            if  os.path.isfile(os.path.join(settings.MEDIA_ROOT, target)):
                print "___ file exist %s " % os.path.join(settings.MEDIA_ROOT, target)
            else:
                print "converting file %s " % bfile.file.name
                conversion_cmd = "unoconv -f pdf -o %s %s" % (os.path.join(settings.MEDIA_ROOT, target),
                                                              os.path.join(settings.MEDIA_ROOT, bfile.file.name))
                subprocess.check_output(conversion_cmd.split())

        # Generate thumbnail
        try:
            thumbnail = get_thumbnail(target, preview_width, quality=80, format='JPEG')
        except Exception:
            thumbnail = None

        if thumbnail:
            # Issue a X-Sendfile to the server
            fp = os.path.join(settings.MEDIA_ROOT, thumbnail.name)
        else:
            fp = os.path.join(settings.STATIC_ROOT, 'images/defaultfilepreview.jpg')
        return sendfile(request, fp)
                
class UploadView(JSONResponseMixin, FormMixin, View):
    """
    A generic HTML5 Upload view
    
    FIXME : deal with permissions !!
    """
    form_class = BucketUploadForm
    template_name = 'multiuploader/form.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(UploadView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.api_res = BucketFileResource()
        try:
            self.api_res.is_authenticated(request)
        except:
            raise PermissionDenied()

        form_class = self.get_form_class()

        qdict = request.POST.copy()
        print "Request user : %s" % (request.user.pk)
        qdict['uploaded_by'] = request.user.pk
        form = form_class(qdict, request.FILES)
        print form

        if form.is_valid():
            file = request.FILES[u'file']
            wrapped_file = UploadedFile(file)
            
            # writing file manually into model
            # because we don't need form of any type.
            # 
            # check if we update a file by giving an 'id' param 
            if 'id' in request.POST:
                file_id = qdict['id']
                self.bf = get_object_or_404(BucketFile, pk=file_id)
                self.bf.file = file
                self.bf.being_edited_by = None 
                self.bf.uploaded_by = form.cleaned_data['uploaded_by'] # FIXME : security hole !! should
                self.bf.save()
                self.bf.thumbnail_url = reverse('bucket-thumbnail', args=[self.bf.pk])
                self.bf.save()
            # new file
            else:
                self.bf = BucketFile()
                self.bf.filename = wrapped_file.file.name
                self.bf.file_size = wrapped_file.file.size
                self.bf.file = file
                self.bf.uploaded_by = form.cleaned_data['uploaded_by'] # FIXME : security hole !!
                self.bf.bucket = form.cleaned_data['bucket']
                self.bf.save()
                self.bf.thumbnail_url = reverse('bucket-thumbnail', args=[self.bf.pk])
                self.bf.save()

            return self.form_valid(form)            
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_json_response({'error': 'error not implemented'})
            
    def form_valid(self, form):
        """
        Once saved, return the object as if we were reading the API (json, ...)
        """
        return self.api_res.get_detail(self.request, pk=self.bf.pk)


