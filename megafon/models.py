from django.db import models
from autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager
from accounts.models import Profile
from mptt.models import MPTTModel, TreeForeignKey

import random, string

class Post(MPTTModel):

    """ A post """

    def populate_slug(instance):
        if instance.title:
            return instance.title
        else:
            return "answer-%s" % ''.join(random.choice(string.lowercase) for i in range(20))

    title = models.CharField(max_length="200", blank=True, null=False)
    posted_on = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Profile)
    text = models.TextField()
    slug = AutoSlugField(populate_from=populate_slug, unique_with='id')
    tags = TaggableManager(blank=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='answers', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['posted_on']
