from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField

# ItemSets
class ItemSet(models.Model):

    owner = models.ForeignKey(User, null=True, default=None, related_name="owner_of_itemset")
    json = JSONField()
    name = models.CharField(max_length=32, default='noname.json')
    created_at = models.DateTimeField(auto_now_add=True)
    champ_for = models.PositiveSmallIntegerField(default=0)     # champid
    champ_against = models.PositiveSmallIntegerField(default=0) # champid
    LANE_CHOICES = (
    	('M', 'mid'),
    	('T', 'top'),
    	('B', 'bot'),
    	('J', 'jungle'),
    	('', 'any')
    )
    lane = models.CharField(max_length=1, choices=LANE_CHOICES, default='')
    users_upvotes = models.ManyToManyField(User,blank=True, default=None, related_name="users_who_upvoted")
    users_upvotes_count = models.IntegerField(default=0)

    def __unicode__(self):
    	if self.owner:
    		ownername = self.owner.username
    	else:
    		ownername = "tmp"
    	return self.name + "| owner: " + ownername + "| for: " + str(self.champ_for) + \
    			"| against: " + str(self.champ_against) + "| lane: " + self.lane + "| upvotes count: " + str(self.users_upvotes_count)

