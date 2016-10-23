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
class patientHandler(webapp2.RequestHandler):
	def post(self):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports application/json MIME type"
			return
		new_patient=db_def.Patient()
		name=self.request.get('name', default_value=None)
		age=self.request.get('age', default_value=None)
		illness=self.request.get_all('illness[]', default_value=None)
		if name:
			new_patient.name=name
		else:
			self.response.status=400
			self.response.status_message="Invalid Request, Illness name is required."
		if age:
			new_patient.age=age
		if illness:
			for ill in illness:
				new_patient.illness.append(ndb.Key(db_def.Illness,int(ill)))
		key = new_patient.put()
		out = new_patient.to_dict()
		self.response.write(json.dumps(out))
		return
		
class patientIllness(webapp2.RequestHandler):
	def put(self, **kwargs):
		if 'application/json' not in self.request.accept:
			self.response.status=406
			self.response.status_message="Not Acceptable, API only supports application/json MIME type"
		if 'cid' in kwargs:
			patient=ndb.Key(db_def.Patient, int(kwargs['cid'])).get()
			if not patient:
				self.response.status=404
				self.response.status_message="Patient not found"
				return
		if 'mid' in kwargs:
			ill=ndb.Key(db_def.Illness, int(kwargs['mid']))
			if not patient:
				self.response.status=404
				self.response.status_message="Illness not found"
				return
		if ill not in patient.illness:
			patient.illness.append(ill)
			patient.put()
		self.response.write(json.dumps(patient.to_dict()))
		return
