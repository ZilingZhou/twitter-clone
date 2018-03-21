from django.db import models
from mongoengine import *

connect('twitterdb')
# Create your models here.
class User(Document):
	username = StringField(primary_key=True)
	password = StringField()
	email = StringField()
	verified = BooleanField()
	key = StringField()

class Item(Document):
	#itemId = StringField(primary_key=True)
	username = StringField()
	likes = IntField(default = 0)
	retweeted = IntField(default = 0)
	content = StringField()
	timestamp = DateTimeField()
	childType = StringField()


# item: {
# id: item id
# username: username who sent item
# property: {
# likes: number
# }
# retweeted: number
# content: body of item, (original content if this item is a retweet)
# timestamp: timestamp, represented as Unix time
# }
