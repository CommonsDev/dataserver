# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic.edit import FormMixin
from django.views.generic import TemplateView, View
from django.core import serializers

from multiuploader.forms import MultiUploadForm
from django.utils import simplejson as json

from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import UploadedFile

from .models import BucketFile
from .forms import BucketUploadForm

from sorl.thumbnail import get_thumbnail

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

class UploadView(JSONResponseMixin, FormMixin, View):
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
            
            try:
                #TODO: gerer + types de fichiers / parametrer les thumbnails
                im = get_thumbnail(self.bf.file, "150x100", quality=80)
                self.bf.thumbnail_url = im.url
            except Exception as e:
                print(e)

            self.bf.save()              

            return self.form_valid(form)            
        else:
            print(form.errors)
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # generating json response array
        result = [{"id": self.bf.id,
                   "name": self.bf.filename,
                   "size": self.bf.file_size,
                   "url": reverse('multiuploader_file_link', args=[self.bf.pk]),
                   "thumbnail_url": self.bf.thumbnail_url,
                   "delete_url": reverse('multiuploader_delete', args=[self.bf.pk]),
                   "delete_type": "POST", }]
        
        response_data = json.dumps(result)
        mimetype = 'application/json'
        return HttpResponse(response_data, mimetype=mimetype)            


