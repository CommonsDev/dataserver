from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _


from userena.models import UserenaBaseProfile

# Create your models here.

class GUPProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    favourite_snack = models.CharField(_('favourite snack'),
                                       max_length=5)

