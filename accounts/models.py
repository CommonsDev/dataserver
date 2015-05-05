from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from guardian.shortcuts import assign_perm

from userena.models import UserenaBaseProfile
from userena.utils import get_profile_model



class Profile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')

    @property
    def username(self):
        return self.user.username

class ObjectProfileLink(models.Model):
    """
    Generic class to record a link between a user profile and an object (Project e.g.)
    with different levels of implication (Project Team Member, Project follower, Project Resource member e.g)
    and a free field for detail (as role e.g). Validation process is covered by an aditional boolean field.
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.TextField(_('object_id'))
    content_object = generic.GenericForeignKey('content_type', 'object_id', _("Linked object"))
    profile = models.ForeignKey(Profile, verbose_name = _("Linked user profile"))
    level = models.IntegerField(_("Implication level of the link"))
    detail = models.CharField(max_length=200, blank=True)
    isValidated = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_profile_on_user_signup(sender, created, instance, **kwargs):
    if created:
        profile_model = get_profile_model()
        profile_model.objects.create(user=instance)

@receiver(post_save, sender=User)
def assign_to_authenticated_users_group(sender, instance, created, *args, **kwargs):
    """
    Here we assign all newly created users to the group 'authenticated_users'
    If this group does not exists we create it and give permissions from settings 
    variable AUTHENTICATED_USERS_PERMISSIONS
    """
    # Check if authenticated_user group exists, if not create it and add following perms
    group, created = Group.objects.get_or_create(name='authenticated_users')
    
    # assign perms to group
    permissions = getattr(settings, 'AUTHENTICATED_USERS_PERMISSIONS')
    print "assigning permisions %s" % (permissions.__str__())
    for permission in permissions:
        assign_perm(permission, group)
    # assign user to group
    instance.groups.add(group)