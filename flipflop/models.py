from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

class Board(models.Model):
    title = models.CharField(_('title'), max_length=100)

    def __unicode__(self):
        return self.title

class List(models.Model):
    """
    In a board, a column, or list, where you store cards
    """
    title = models.CharField(_('title'), max_length=100)
    board = models.ForeignKey(Board, related_name='lists')

    def __unicode__(self):
        return self.title


class Card(models.Model):
    """
    A card, describing something, such as a User Story.
    """
    class Meta:
        ordering = ('submitted_date', 'title')
    
    title = models.CharField(_('title'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    archived = models.BooleanField(default=False)
    
    submitted_date = models.DateTimeField(_('date submitted'), auto_now_add=True)
    modified_date = models.DateTimeField(_('date modified'), auto_now=True)

    due_date = models.DateTimeField(_('due date'), null=True, blank=True)
    
    submitter = models.ForeignKey(User, verbose_name=_('submitter'), related_name="submitted_cards")
    assigned_to = models.ManyToManyField(User, verbose_name=_('assigned to'), blank=True)

    list = models.ForeignKey(List, related_name='cards')
    tags = TaggableManager(blank=True)

    @property
    def completion(self):
        tasks = self.tasks.all()
        if len(tasks) == 0:
            return -1
        done_tasks = [t for t in tasks if t.done]
        return float(len(done_tasks)) / len(tasks)

    @property
    def comment_count(self):
        return 0

    @property
    def attachment_count(self):
        return 0

    def __unicode__(self):
        return self.title
        

class Task(models.Model):
    """
    Something to do, linked to a card
    """
    title = models.CharField(_('title'), max_length=255)
    card = models.ForeignKey(Card, related_name='tasks')
    done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title
    