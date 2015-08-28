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
    champ_for = models.CharField(max_length=32, default='')
    champ_against = models.CharField(max_length=32, default='')
    LANE_CHOICES = (
    	('M', 'mid'),
    	('T', 'top'),
    	('B', 'bot'),
    	('J', 'jungle'),
    	('', 'any')
    )
    lane = models.CharField(max_length=1, choices=LANE_CHOICES, default='')

    def __unicode__(self):
    	if self.owner:
    		ownername = self.owner.user.username
    	else:
    		ownername = "tmp"
    	return self.name + " owner: " + ownername + " for: " + self.champ_for + \
    			" against: " + self.champ_against + " lane: " + self.lane 

