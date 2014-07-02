from tastypie.resources import ModelResource
from tastypie import fields
from .models import Place, Thing, PeopleThing
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from accounts.api import UserResource

class ThingResource(ModelResource):
	class Meta:
			queryset = Thing.objects.all()
			resource_name = "thing/thing"
			authentication = Authentication()
			authorization = Authorization()


class PlaceResource(ModelResource):
	class Meta:
			queryset = Place.objects.all()
			resource_name = 'thing/place'
			authentication = Authentication()
			authorization = Authorization()
			always_return_data=True

	things_available = fields.ToManyField(ThingResource,'things', full=True, full_list=False, full_detail=True, blank=True)

class PeopleThingResource(ModelResource):
	class Meta:
			queryset = PeopleThing.objects.all()
			resource_name = "thing/peoplething"
			authentication = Authentication()
			authorization = Authorization()

  	assigned_to = fields.ToManyField(UserResource, 'assigned_to', blank=True, full=True)