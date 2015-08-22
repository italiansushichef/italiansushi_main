from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# Login User Profiles
class LoginProfile(models.Model):

    # Linking LoginProfile to User model instance
    user = models.OneToOneField(User)
    saved_count = models.PositiveSmallIntegerField(default=0)
    def __unicode__(self):
        return self.user.username + " count: " + str(self.saved_count)

class ItemSet(models.Model):

    owner = models.ForeignKey(LoginProfile)
    json = JSONField()
    name = models.CharField(max_length=32, default='noname.json')

    def __unicode__(self):
    	return self.name + " owner: " + self.owner.user.username

