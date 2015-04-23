from django.conf.urls import url
from tastypie.resources import (
    ModelResource,
    ObjectDoesNotExist,
    MultipleObjectsReturned,
)
from tastypie.http import HttpGone, HttpMultipleChoices


class HistorizedModelResource(ModelResource):

    """ Allow any historized model to get an historized resource for free.

    Hint: just set ``Meta.history_resource_class`` to the right history
    resource class definition.
    """

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/history$" % (
                self._meta.resource_name, ),
                self.wrap_view('get_history'),
                name="api_project_history"),
        ]

    def get_history(self, request, **kwargs):
        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']},
                                       request=request)
            obj = self.cached_obj_get(bundle=bundle,
                                      **self.remove_api_resource_names(kwargs))

        except ObjectDoesNotExist:
            return HttpGone()

        except MultipleObjectsReturned:
            return HttpMultipleChoices(
                "More than one resource is found at this URI.")

        return self._meta.history_resource_class().get_list(request, id=obj.pk)
