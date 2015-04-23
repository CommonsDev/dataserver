# -*- encoding: utf-8 -*-
import json

from django.conf.urls import url
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, logout
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from tastypie import fields
from tastypie import http
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.authentication import Authentication, BasicAuthentication, ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.models import ApiKey, create_api_key
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from dataserver.authentication import AnonymousApiKeyAuthentication
from .models import Profile, ObjectProfileLink

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.exclude(pk=-1) # Exclude anonymous user
        detail_uri_name = 'username'
        allowed_methods = ['get', 'post']
        resource_name = 'account/user'
        authentication = Authentication()
        authorization = Authorization()
        fields = ['id', 'username', 'first_name', 'last_name', 'groups', 'email']
        filtering = {
            "id" : ['exact',],
            "username": ALL_WITH_RELATIONS,
        }

    groups = fields.ToManyField('accounts.api.GroupResource', 'groups', null=True, full=False)

    def dehydrate(self, bundle):
        try:
            bundle.data['mugshot'] = bundle.obj.profile.mugshot
        except Profile.DoesNotExist:
            pass
        bundle.data['groups'] = [{"id" : group.id, "name":group.name} for group in bundle.obj.groups.all()]
        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        try:
            bundle = super(UserResource, self).obj_create(bundle, **kwargs)
            bundle.obj.set_password(bundle.data.get('password'))
            bundle.obj.save()
        except IntegrityError:
            raise BadRequest('That username already exists')
        return bundle

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/login%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
            url(r"^(?P<resource_name>%s)/login/google%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login_google'), name="api_login_google"),
            url(r'^(?P<resource_name>%s)/logout%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name='api_logout'),
        ]

    def login_google(self, request, **kwargs):
        """
        Given an oauth2 google token, check it and if ok, return or
        create a user.
        """
        import httplib, urllib
        import simplejson

        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        oauth_token = data.get('access_token', '')
        conn = httplib.HTTPSConnection("www.googleapis.com")
        conn.request("GET", "/oauth2/v1/userinfo?access_token=%s" % oauth_token)
        response = conn.getresponse()

        user = None
        if response.reason == "OK":
            data = simplejson.loads(response.read())
            if data['verified_email']:
                user, created = User.objects.get_or_create(username=data['email'],
                                                           email=data['email'],
                                                           first_name=data['given_name'],
                                                           last_name=data['family_name'])

        return self.login_to_apikey(request, user)

    def login(self, request, **kwargs):
        """
        Login a user against a username/password.
        Return an API Key that's going to be used for the following requests
        """
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        return self.login_to_apikey(request, user)


    def login_to_apikey(self, request, user):
        if user:
            if user.is_active:
                # login(request, user)

                try:
                    key = ApiKey.objects.get(user=user)
                except ApiKey.DoesNotExist:
                    return self.create_response(
                        request, {
                            'success': False,
                            'reason': 'missing key',
                        },
                        HttpForbidden,
                    )

                ret = self.create_response(request, {
                    'success': True,
                    'username': user.username,
                    'key': key.key,
                })

                return ret
            else:
                return self.create_response(
                    request, {
                        'success': False,
                        'reason': 'disabled',
                    },
                    HttpForbidden,
                )
        else:
            return self.create_response(
                request, {
                    'success': False,
                    'reason': 'invalid login',
                    'skip_login_redir': True,
                },
                HttpUnauthorized,
            )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)


class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'account/group'
        authentication = Authentication()
        authorization = Authorization()

    users = fields.ToManyField(UserResource, 'user_set', full=True)


# Create API key for every new user
models.signals.post_save.connect(create_api_key, sender=User)

class ProfileResource(ModelResource):
    user = fields.OneToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset = Profile.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = 'account/profile'
        authentication = Authentication()
        authorization = Authorization()
        filtering = {
            "id" : ['exact',],
            "user" : ALL_WITH_RELATIONS,
        }

    def dehydrate(self, bundle):
        bundle.data["username"] = bundle.obj.username
        return bundle

class ObjectProfileLinkResource(ModelResource):
    """
    Resource for linking profile with objects s.a a Project, a Category, etc.
    """
    content_type = fields.CharField(attribute='content_type__model')
    profile = fields.OneToOneField(ProfileResource, 'profile', full=True)
    level = fields.IntegerField(attribute='level')
    detail = fields.CharField(attribute='detail')
    isValidated = fields.BooleanField(attribute='isValidated')

    class Meta:
        queryset = ObjectProfileLink.objects.all()
        resource_name = 'objectprofilelink'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        default_format = "application/json"
        filtering = {
            "object_id" : ['exact', ],
            "content_type" : ['exact', ],
            "profile" : ALL_WITH_RELATIONS,

        }
        always_return_data = True

    def prepend_urls(self):
        return [
           url(r"^(?P<resource_name>%s)/(?P<content_type>\w+?)/(?P<object_id>\d+?)%s$" % (self._meta.resource_name, trailing_slash()),
               self.wrap_view('dispatch_list'),
               name="api_dispatch_list"),
            ]

    def dispatch_list(self, request, **kwargs):
        self.method_check(request, allowed=['get', 'post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if 'content_type' in kwargs and 'object_id' in kwargs and request.method=="POST":
            data = json.loads(request.body)
            if 'profile_id' in data:
                profile = get_object_or_404(Profile, pk=data['profile_id'])
            else:
                profile=request.user.profile
            objectprofilelink_item, created = ObjectProfileLink.objects.get_or_create(profile=profile,
                                            content_type=ContentType.objects.get(model=kwargs['content_type']),
                                            object_id=kwargs['object_id'],
                                            level=data['level'],
                                            detail=data['detail'],
                                            isValidated=data['isValidated'])
            bundle = self.build_bundle(obj=objectprofilelink_item, request=request)
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)

            return self.create_response(request,
                                        bundle,
                                        response_class=http.HttpCreated,
                                        location=self.get_resource_uri(bundle))

        return ModelResource.dispatch_list(self, request, **kwargs)
