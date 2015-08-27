from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# Login User Profiles
class LoginProfile(models.Model):

    # Linking LoginProfile to User model instance
    user = models.OneToOneField(User)
    def __unicode__(self):
        return self.user.username

# ItemSets
class ItemSet(models.Model):

    owner = models.ForeignKey(LoginProfile, null=True)
    json = JSONField()
    name = models.CharField(max_length=32, default='noname.json')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
    	return self.name + " owner: " + self.owner.user.username

