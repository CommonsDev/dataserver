from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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
