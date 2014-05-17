from django.db import models

class GroupBuyItem(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s" % self.name
    

class GroupBuy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    start_on = models.DateTimeField()
    end_on = models.DateTimeField()
    
    items = models.ManyToManyField(GroupBuyItem, related_name='groupbuys')

    def __unicode__(self):
        return u"Group Buy:%s" % self.title
