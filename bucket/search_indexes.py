import datetime

from haystack import indexes

from .models import Bucket, BucketFile, BucketFileComment


class BucketFileIndex(indexes.SearchIndex, indexes.Indexable):
    
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='uploaded_by', null=True)
    pub_date = indexes.DateTimeField(model_attr='uploaded_on')
    tags = indexes.MultiValueField(null=True)
    
    
    def get_model(self):
        return BucketFile

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(uploaded_on__lte=datetime.datetime.now())
    
    def prepare_tags(self, obj):
	return [tag.name for tag in obj.tags.all()]

    
