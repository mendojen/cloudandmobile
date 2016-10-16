import webapp2
import base_page
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import db_defs

class Admin(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		
	def render(self, page):
		self.template_values['classes']=[{'name':x.name, 'key':x.key.urlsafe()} for x in db_defs.ChannelClass.query().fetch()]
		self.template_values['channels']=[{'name':x.name,'url':x.url,'age':x.age, 'key':x.key.urlsafe()} for x in db_defs.Channel.query().fetch()]
		base_page.BaseHandler.render(self, page, self.template_values)
		
	def get(self):
		self.render('admin.html')
	
	def post(self):
		action=self.request.get('action')
		if action=='add_channel':
			k=ndb.Key(db_defs.Channel,self.app.config.get('default-group'))
			chan=db_defs.Channel(parent=k)
			chan.name=self.request.get('channel-name')
			chan.url=self.request.get('url_name')
			chan.age=self.request.get('age_num')
			chan.check=self.request.get('check')
			chan.classes=[ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
			chan.active=True
			chan.put()
			self.template_values['message']='Added ' + chan.name + ' to the database.'
		elif action=='add_class':
			k=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))
			c=db_defs.ChannelClass(parent=k)
			c.name=self.request.get('class-name')
			c.put()
			self.template_values['message']='Added genre' + c.name + ' to the database.'
		
		else:
			self.template_values['message']='Action ' + action + ' is unknown'
		
		self.template_values['classes'] = db_defs.ChannelClass.query(
			ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))).fetch()
		self.render('admin.html')

class view(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		

	def get(self):
		if self.request.get('type')=='channel':
			channel_key=ndb.Key(urlsafe=self.request.get('key'))
			channel=channel_key.get()
			self.template_values['channel']=channel
			classes=db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group')))

		self.render('view.html', self.template_values)
		
class edit(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		self.template_values['edit_url']=blobstore.create_upload_url('/edit/channel')

	def get(self):
		if self.request.get('type')=='channel':
			channel_key=ndb.Key(urlsafe=self.request.get('key'))
			channel=channel_key.get()
			self.template_values['channel']=channel
			classes=db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group')))
			class_boxes=[]
			for c in classes:
				if c.key in channel.classes:
					class_boxes.append({'name':c.name, 'key':c.key.urlsafe(), 'checked':True})
				else:
					class_boxes.append({'name':c.name, 'key':c.key.urlsafe(), 'checked':False})
			self.template_values['classes']=class_boxes
		self.render('edit.html', self.template_values)

class editChannel(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		channel_key=ndb.Key(urlsafe=self.request.get('key'))
		channel=channel_key.get()
		channel.classes=[ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
		channel.put()
		self.redirect('/edit?key=' + channel_key.urlsafe() + '&type=channel')