from tastypie.resources import Resource
from tastypie import fields
from tastypie.cache import SimpleCache

from vlille import Vlille

class VlilleResource(Resource):
    """
    Vlille Lille Bike Service
    """
    class Meta:
        resource_name = 'transport/vlille'
        cache = SimpleCache(timeout=60)

    id = fields.IntegerField(attribute='id')
    status = fields.CharField(attribute='status', use_in='detail')
    free_attachs = fields.IntegerField(attribute='free_attachs', use_in='detail')
    payment = fields.BooleanField(attribute='payment', use_in='detail')
    attachs = fields.IntegerField(attribute='attachs', use_in='detail')
    bikes = fields.IntegerField(attribute='bikes', use_in='detail')
    address = fields.CharField(attribute='address', use_in='detail')
    name = fields.CharField(attribute='name')
    longitude = fields.FloatField(attribute='longitude')
    latitude = fields.FloatField(attribute='latitude')
    last_update = fields.DateTimeField(attribute='last_update', use_in='detail')

    def obj_get(self, request=None, **kwargs):
        v = Vlille()
        v.load_stations()
        for station in v.stations:
            if station.id == int(kwargs['pk']):
                station.refresh()
                return station

        return None

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle)
        
    def get_object_list(self, bundle):
        v = Vlille()

        v.load_stations()
        
        return v.stations







