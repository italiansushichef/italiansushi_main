from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# Login User Profiles
class LoginProfile(models.Model):

    # Linking LoginProfile to User model instance
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.username

class ItemSet(models.Model):

    users = models.ManyToManyField(LoginProfile)
    json = JSONField()

