from django.core.urlresolvers import reverse
from django.conf.urls import url  # , patterns, include

from haystack.query import SearchQuerySet
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization  # , Authorization,
from tastypie import fields
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.paginator import Paginator
from tastypie.utils import trailing_slash

from dataserver.authentication import AnonymousApiKeyAuthentication
from base.api import HistorizedModelResource
from bucket.api import BucketResource, BucketFileResource
from projects.api import ProjectResource
from projects.models import Project

from .models import ProjectSheet, ProjectSheetTemplate, ProjectSheetQuestion, ProjectSheetQuestionAnswer, QuestionChoice


class QuestionChoiceResource(ModelResource):
    class Meta:
        queryset = QuestionChoice.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/sheet/question_choice'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True

class ProjectSheetQuestionResource(ModelResource):
    choices = fields.ForeignKey(QuestionChoiceResource, 'choices', full=True, null=True)
    class Meta:
        queryset = ProjectSheetQuestion.objects.all()
        allowed_methods = ['post', 'get']
        resource_name = 'project/sheet/question'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()

    def hydrate(self, bundle):
        bundle.obj.template = ProjectSheetTemplate.objects.get(
            id=bundle.data["template_id"])
        return bundle


class ProjectSheetTemplateResource(ModelResource):
    questions = fields.ToManyField(ProjectSheetQuestionResource,
                                   'questions', full=True, null=True)

    class Meta:
        queryset = ProjectSheetTemplate.objects.all()
        allowed_methods = ['get']
        resource_name = 'project/sheet/template'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'slug': ('exact', )
        }


class ProjectSheetQuestionAnswerResource(ModelResource):
    question = fields.ToOneField(ProjectSheetQuestionResource, 'question', full=True)
    projectsheet = fields.ToOneField("projectsheet.api.ProjectSheetResource", 'projectsheet')
    selected_choices_id = fields.ListField(attribute='selected_choices_id', null=True)

    class Meta:
        queryset = ProjectSheetQuestionAnswer.objects.all()
        allowed_methods = ['get', 'patch', 'post']
        resource_name = 'project/sheet/question_answer'
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True


class ProjectSheetHistoryResource(ModelResource):

    class Meta:
        queryset = ProjectSheet.history.all()
        filtering = {'id': ALL_WITH_RELATIONS}


class ProjectSheetResource(HistorizedModelResource):
    project = fields.ToOneField(ProjectResource, 'project', full=True)
    template = fields.ToOneField(ProjectSheetTemplateResource, 'template')
    bucket = fields.ToOneField(BucketResource, 'bucket', null=True, full=True)
    cover = fields.ToOneField(BucketFileResource, 'cover', null=True, full=True)
    question_answers = fields.ToManyField(ProjectSheetQuestionAnswerResource,
                                          'question_answers', null=True,
                                          full=True)
    videos = fields.DictField(attribute='videos', null=True)

    class Meta:
        object_class = ProjectSheet
        queryset = ProjectSheet.objects.all()
        allowed_methods = ['get', 'post', 'put', 'patch']
        default_format = "application/json"
        resource_name = 'project/sheet/projectsheet'
        history_resource_class = ProjectSheetHistoryResource
        authentication = AnonymousApiKeyAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        filtering = {
            'project': ALL_WITH_RELATIONS,
            'template': ALL_WITH_RELATIONS,
        }

    def hydrate(self, bundle):
        if "project_id" in bundle.data:  # XXX: ???
            bundle.obj.project = Project.objects.get(
                id=bundle.data["project_id"])

        if "template_id" in bundle.data:
            bundle.obj.template = ProjectSheetTemplate.objects.get(
                id=bundle.data["template_id"])

        return bundle

    def prepend_urls(self):
        """ URL override for permissions and search specials. """

        # get the one from HistorizedModelResource
        urls = super(ProjectSheetResource, self).prepend_urls()

        return urls + [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name,
                trailing_slash()), self.wrap_view('projectsheet_search'),
                name="api_projectsheet_search"),
        ]

    def projectsheet_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        self.is_authenticated(request)

        # Query params
        query = request.GET.get('q', '')
        autocomplete = request.GET.get('auto', None)
        selected_facets = request.GET.getlist('facet', None)

        sqs = SearchQuerySet().models(self.Meta.object_class).facet('tags')

        # narrow down QS with facets
        if selected_facets:
            for facet in selected_facets:
                sqs = sqs.narrow('tags:%s' % (facet))

        # A: if autocomplete, we return only a list of tags starting with "auto" along with their count
        if autocomplete != None:
            tags = sqs.facet_counts()
            tags = tags['fields']['tags']
            if len(autocomplete) > 0:
                tags = [ t for t in tags if t[0].startswith(autocomplete) ]
            tags = [ {'name':t[0], 'count':t[1]} for t in tags ]
            object_list = {
                'objects': tags,
            }
        # B: else, we return a list of projectsheets
        else:
            # launch query
            if query != "":
                sqs = sqs.auto_query(query)

            uri = reverse('api_projectsheet_search',
                          kwargs={'api_name': self.api_name,
                                  'resource_name': self._meta.resource_name})
            paginator = Paginator(request.GET, sqs, resource_uri=uri)

            objects = []
            for result in paginator.page()['objects']:
                if result:
                    bundle = self.build_bundle(obj=result.object, request=request)
                    bundle = self.full_dehydrate(bundle)
                    objects.append(bundle)
            object_list = {
                'meta': paginator.page()['meta'],
                'objects': objects,
            }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
