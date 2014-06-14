from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from guardian.shortcuts import get_users_with_perms, assign_perm

class Label(models.Model):
    label = models.CharField(max_length=100)

    def __unicode__(self):
        return self.label
    
class Board(models.Model):
    class Meta:
        permissions = (
            ('view_board', _("View Board")),
        )

    created_by = models.ForeignKey(User, related_name='kanban_created')

    
    title = models.CharField(_('title'), max_length=100)

    labels = models.ManyToManyField(Label, null=True, blank=True, related_name='boards')
    
    @property
    def members(self):
        return get_users_with_perms(self)

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
    labels = models.ManyToManyField(Label, null=True, blank=True)

    @property
    def completion(self):
        tasks = self.tasks.all()
        if len(tasks) == 0:
            return -1
        done_tasks = [t for t in tasks if t.done]
        return float(len(done_tasks)) / len(tasks)

    @property
    def tasks_done_count(self):
        return len(self.tasks.filter(done=True))
    
    @property
    def comment_count(self):
        return len(self.comments.all())

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

class CardComment(models.Model):
    """
    A comment about a card for eg.
    """
    user = models.ForeignKey(User)
    card = models.ForeignKey(Card, related_name='comments')

    posted_at = models.DateTimeField(auto_now_add=True)    
    text = models.TextField()
    
@receiver(post_save, sender=Board)
def allow_user_to_edit_boards(sender, instance, created, *args, **kwargs):
    assign_perm("view_board", user_or_group=instance.created_by, obj=instance)
    assign_perm("change_board", user_or_group=instance.created_by, obj=instance)
    assign_perm("delete_board", user_or_group=instance.created_by, obj=instance)

    
@receiver(post_save, sender=User)
def allow_user_to_create_boards_via_api(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("flipflop.add_board", instance)
    

