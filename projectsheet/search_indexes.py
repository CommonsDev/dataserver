import datetime

from haystack import indexes
from taggit.models import Tag
from .models import ProjectSheet


class ProjectSheetIndex(indexes.SearchIndex, indexes.Indexable):
    
  text = indexes.CharField(document=True, use_template=True)
  tags = indexes.MultiValueField(null=True, faceted=True)
  
  def get_model(self):
      return ProjectSheet
  
  def prepare_tags(self, obj):
      return [tag.name for tag in obj.project.tags.all()]
