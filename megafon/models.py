from django.db import models
from autoslug.fields import AutoSlugField
from taggit.managers import TaggableManager
from accounts.models import Profile
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save

import random, string

class Post(MPTTModel):

    """
    A post
    Author is defined with accounts.ObjectProfileLink
    """

    def populate_slug(instance):
        if instance.title:
            return instance.title
        else:
            return "answer-%s" % ''.join(random.choice(string.lowercase) for i in range(20))

    title = models.CharField(max_length="200", blank=True, null=False)
    posted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True, auto_now=True)
    text = models.TextField()
    slug = AutoSlugField(populate_from=populate_slug, unique_with='id')
    tags = TaggableManager(blank=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='answers', db_index=True)
    answers_count = models.PositiveIntegerField(default=0)

    class MPTTMeta:
        order_insertion_by = ['posted_on']


def update_answers_count(sender, instance, created, **kwargs):
    if not instance.is_root_node():
        instance.parent.answers_count = instance.parent.get_descendant_count()
        instance.parent.save()

# register the signal
post_save.connect(update_answers_count, sender=Post, dispatch_uid="update_answers_count")
