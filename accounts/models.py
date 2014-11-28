from django.contrib.auth.models import User
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

@receiver(post_save, sender=User)
def create_profile_on_user_signup(sender, created, instance, **kwargs):
    if created:
        profile_model = get_profile_model()
        profile_model.objects.create(user=instance)
