from google.appengine.ext import ndb

class Message(ndb.Model):
	channel=ndb.StringProperty(required=True)
	date_time=ndb.DateTimeProperty(required=True)
	count=ndb.IntegerProperty(required=True)

class Channel(ndb.Model):
	name=ndb.StringProperty(required=True)
	url=ndb.StringProperty(required=True)
	age=ndb.StringProperty(required=True)
	check=ndb.StringProperty(required=True)
	classes=ndb.KeyProperty(repeated=True)
	active=ndb.BooleanProperty(required=True)

class ChannelClass(ndb.Model):
	name=ndb.StringProperty(required=True)
	url=ndb.StringProperty(required=True)
	age=ndb.StringProperty(required=True)
	check=ndb.StringProperty(required=True)
