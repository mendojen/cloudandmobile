import webapp2
from google.appengine.api import oauth
import json
from google.appengine.ext import ndb
import db_def

class IllnessHandler(webapp2.RequestHandler):
	def post(self):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports application/json MIME type"
			return
		new_illness=db_def.Illness()
		name=self.request.get('name', default_value=None)
		mSymptom=self.request.get('mSymptom', default_value=None)
		mExercise=self.request.get('mExercise', default_value=None)
		if name:
			new_illness.name=name
		else:
			self.response.status=400
			self.response.status_message="Invalid Request, Illness name is required."
		if mSymptom:
			new_illness.mSymptom=mSymptom
		if mExercise:
			new_illness.mExercise=mExercise
		key = new_illness.put()
		out = new_illness.to_dict()
		self.response.write(json.dumps(out))
		return
		
	def get(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable"
			return
		if 'id' in kwargs:
			out=ndb.Key(db_def.Illness, int(kwargs['id'])).get().to_dict()
			self.response.write(json.dumps(out))
		else:
			q = db_def.Illness.query()
			keys = q.fetch(keys_only=True)
			results = { 'keys' :[x.id() for x in keys]}
			self.response.write(json.dumps(results))



