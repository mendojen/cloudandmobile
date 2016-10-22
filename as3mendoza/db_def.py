import webapp2
from google.appengine.api import oauth
import json
from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d=super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Illness(Model):
	name=ndb.StringProperty(required=True)
	mSymptom=ndb.StringProperty()
	mExercise=ndb.StringProperty()

class Patient(Model):
	name=ndb.StringProperty(required=True)
	age=ndb.StringProperty()
	currentExercise=ndb.StringProperty()
	illness=ndb.KeyProperty(required=True)
	def to_dict(self):
		d=super(Illness,self).to_dict()
		d['illness']=[m.id() for m in d['illness']]
		return d