import json
import datetime

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.core import urlresolvers
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from django_comments.models import Comment, CommentFlag
from django_comments.views.moderation import perform_flag
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie import fields
from tastypie.utils import dict_strip_unicode_keys, trailing_slash
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie import http

from dataserver.authentication import AnonymousApiKeyAuthentication
from accounts.api import ProfileResource, UserResource
from accounts.models import Profile

class CommentFlagResource(ModelResource):
    flag=fields.CharField(attribute='flag')
    
    class Meta:
        queryset = CommentFlag.objects.all()


class CommentResource(ModelResource):
    comment = fields.CharField(attribute='comment')
    user = fields.ToOneField(UserResource, 'user', full='true')
    flags = fields.ToManyField(CommentFlagResource, 'flags', full='false', null='true')
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        filtering = {
            "comment": ALL_WITH_RELATIONS,
            "content_type": "exact",
            "object_pk": "exact"
        }
        allowed_methods = ['get', 'post', 'delete']
        always_return_data = True
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        default_format = "application/json"

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_pk>\d+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
           url(r"^(?P<resource_name>%s)/(?P<comment_id>\d+?)/flag%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('flag_ucomment'),
               name="api_flag")
            ]

    def flag_ucomment(self, request, **kwargs):
        """
        Flags a comment on POST request only using method from django_comments view (to bypass csrf protection)
        
        """
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Flag on POST
        if request.method == 'POST':
            comment = get_object_or_404(Comment, pk=kwargs['comment_id'], site__pk=settings.SITE_ID)
            perform_flag(request, comment)
            
            # FIXME : basic email sending
            change_url = urlresolvers.reverse('admin:django_comments_comment_change', args=(comment.id,))
            host = request.get_host()
            recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
            subject = '[%s] Un commentaire abusif signale ' % (get_current_site(request).name)
            message = "Un commentaire abusif a ete signale. Vous pouvez le moderer et le supprimer si besoin a cette adresse %s%s" % (host, change_url)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)

            return HttpResponse("Comment flaged")



    def dispatch_list(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if 'content_type' in kwargs and 'object_pk' in kwargs and request.method=="POST":
            data = json.loads(request.body)
            commented_item, created = Comment.objects.get_or_create(comment=data['comment_text'],
                                            user=request.user,
                                            user_name=request.user.username,
                                            content_type=ContentType.objects.get(model=kwargs['content_type']),
                                            object_pk=kwargs['object_pk'],
                                            site_id=settings.SITE_ID,
                                            submit_date=datetime.datetime.now())
            bundle = self.build_bundle(obj=commented_item, request=request)
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)

            return self.create_response(request,
                                        bundle,
                                        response_class=http.HttpCreated,
                                        location=self.get_resource_uri(bundle))

        return ModelResource.dispatch_list(self, request, **kwargs)
