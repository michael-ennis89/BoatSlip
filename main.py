from google.appengine.ext import ndb
from datetime import datetime
import webapp2
import json

# [START Boat Definition]
class Boat(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty(required=True)
	length = ndb.IntegerProperty(required=True)
	at_sea = ndb.BooleanProperty()
# [END Boat Definition]

# [START Slip Definition]
class Slip(ndb.Model):
	id = ndb.StringProperty()
	number = ndb.IntegerProperty(required=True)
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
# [END Slip Definition]

# [START BoatHandler]
class BoatHandler(webapp2.RequestHandler):
	def post(self):
		boat_data = json.loads(self.request.body)
		new_boat = Boat()
		new_boat.name = boat_data['name']
		new_boat.type = boat_data['type']
		new_boat.length = int(boat_data['length'])
		new_boat.at_sea = True
		new_boat.put()
		new_boat.id = new_boat.key.urlsafe()
		new_boat.put()
		boat_dict = new_boat.to_dict()
		boat_dict['self'] = '/boat/' + new_boat.key.urlsafe()
		self.response.write(json.dumps(boat_dict))
		
	def get(self, id=None):
		if id:
			boat = ndb.Key(urlsafe=id).get()
			boat_dict = boat.to_dict()
			boat_dict['self'] = "/boat/" + boat.key.urlsafe()
			self.response.write(json.dumps(boat_dict))
		else:
			boats = Boat.query()
			boat_list = list()
			for boat in boats:
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boat/' + boat.key.urlsafe()
				boat_list.append(boat_dict)
			self.response.write(json.dumps(boat_list))	
			
	def put(self, id=None):
		if id:
			try:
				boat = ndb.Key(urlsafe=id).get()
			except Exception:
				boat = None
			if boat is None:
				self.response.set_status(400)
			else:		
				put_data = json.loads(self.request.body)
				boat.name = put_data['name']
				boat.type = put_data['type']
				boat.length = put_data['length']
				boat.put()
				if 'at_sea' in put_data:
					if put_data['at_sea'] is True and boat.at_sea is False:
						try:
							current_slip = Slip.query(Slip.current_boat == boat.key.urlsafe()).get()
						except Exception:
							boat = None
						if current_slip is None:
							self.response.set_status(400)
						else:
							current_slip.current_boat = None
							current_slip.arrival_date = None
							current_slip.put()
							boat.at_sea = True
							boat.put()
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boat/' + boat.id
				self.response.write(json.dumps(boat_dict))			
		else:
			self.response.set_status(400)
			
	def patch(self, id=None):
		if id:
			try:
				boat_data = ndb.Key(urlsafe=id).get()
			except Exception:
				boat_data = None
			if boat_data is None:
				self.response.set_status(400)
			else:
				patch_data = json.loads(self.request.body)
				if 'name' in patch_data:
					boat_data.name = patch_data['name']
					boat_data.put()
				if 'type' in patch_data:
					boat_data.type = patch_data['type']
					boat_data.put()
				if 'length' in patch_data:
					boat_data.length = patch_data['length']
					boat_data.put()
				if 'at_sea' in patch_data:
					if patch_data['at_sea'] is True and boat_data.at_sea is False:
						try:
							current_slip = Slip.query(Slip.current_boat == boat_data.key.urlsafe()).get()
						except Exception:
							boat = None
						if current_slip is None:
							self.response.set_status(400)
						else:
							current_slip.current_boat = None
							current_slip.arrival_date = None
							current_slip.put()
							boat.at_sea = True
							boat.put()
				boat_dict = boat_data.to_dict()
				boat_dict['self'] = '/boat/' + boat_data.id
				self.response.write(json.dumps(boat_dict))
		else:
			self.response.set_status(400)
			
	def delete(self, id=None):
		if id:
			try:
				boat_to_delete = ndb.Key(urlsafe=id).get()
			except Exception:
				boat_to_delete = None
			if boat_to_delete is None:
				self.response.set_status(400)
			else:
				if boat_to_delete.at_sea == True:
					boat_to_delete.key.delete()
					self.response.set_status(204)
				else:
					current_slip = Slip.query(Slip.current_boat == boat_to_delete.key.urlsafe()).get()
					current_slip.current_boat = None
					current_slip.arrival_date = None
					current_slip.put()
					boat_to_delete.key.delete()
					self.response.set_status(204)		
		else:
			self.response.set_status(400)
# [END BoatHandler]

# [START SlipHandler]
class SlipHandler(webapp2.RequestHandler):
	def post(self):
		slip_data = json.loads(self.request.body)
		new_slip_numcheck = slip_data['number']
		numcheck = Slip.query(Slip.number == new_slip_numcheck).get()
		if numcheck is None:
			new_slip = Slip()
			new_slip.number = slip_data['number']
			new_slip.put()
			new_slip.id = new_slip.key.urlsafe()
			new_slip.put()
			slip_dict = new_slip.to_dict()
			slip_dict['self'] = '/slip/' + new_slip.key.urlsafe()
			self.response.write(json.dumps(slip_dict))
		else:
			self.response.set_status(403)
		
	def get(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			slip_dict = slip.to_dict()
			slip_dict['self'] = '/slip/' + slip.key.urlsafe()
			self.response.write(json.dumps(slip_dict))
		else:
			slips = Slip.query()
			slip_list = list()
			for slip in slips:
				slip_dict = slip.to_dict()
				slip_dict['self'] = '/slip/' + slip.key.urlsafe()
				slip_list.append(slip_dict)
			self.response.write(json.dumps(slip_list))
			
	def put(self, id=None):
		if id:
			try:
				slip = ndb.key(urlsafe=id).get()
			except Exception:
				slip = None
			if Slip is none:
				self.response.set_status(400)
			else:
				put_data = json.loads(self.request.body)
				if 'number' in put_data:
					new_slip_numcheck = put_data['number']
					numcheck = Slip.query(Slip.number == new_slip_numcheck).get()
					if numcheck is None:
						slip_data.number = put_data['number']
						slip_data.put()
				if 'current_boat' in put_data:
					if put_data['current_boat'] is None and slip_data.current_boat is not None:
						try:
							boat = ndb.Key(urlsafe=(slip_data.current_boat)).get()
						except Exception:
							boat = None
						if boat is None:
							self.response.set_status(400)
						else:
							boat.at_sea = True
							boat.put()
							slip_data.current_boat = put_data['current_boat']
							slip_data.arrival_date = None
							slip_data.put()
					if put_data['current_boat'] is not None and slip_data.current_boat is None:
						try:
							boat = ndb.Key(urlsafe=(put_data['current_boat'])).get()
						except Exception:
							boat = None
						if boat is None:
							self.response.set_status(400)
						else:
							boat.at_sea = False
							boat.put()
							slip_data.current_boat = put_data['current_boat']
							slip_data.arrival_date = datetime.strftime(datetime.utcnow().date(), "%d/%m/%y")
							slip_data.put()
					if put_data['current_boat'] is not None and slip_data.current_boat is not None:
						self.response.set_status(403)
						# already boat inside, cant put another. 
				slip_dict = slip_data.to_dict()
				slip_dict['self'] = '/slip/' + slip_data.id
				self.response.write(json.dumps(slip_dict))
				
		else:
			self.response.set_status(400)
			
	def patch(self, id=None):
		if id:
			try:
				slip_data = ndb.Key(urlsafe=id).get()
			except Exception:
				slip_data = None
			if slip_data is None:
				self.response.set_status(400)
			else:
				patch_data = json.loads(self.request.body)
				if 'number' in patch_data:
					new_slip_numcheck = patch_data['number']
					numcheck = Slip.query(Slip.number == new_slip_numcheck).get()
					if numcheck is None:
						slip_data.number = patch_data['number']
						slip_data.put()
				if 'current_boat' in patch_data:
					if patch_data['current_boat'] is None and slip_data.current_boat is not None:
						try:
							boat = ndb.Key(urlsafe=(slip_data.current_boat)).get()
						except Exception:
							boat = None
						if boat is None:
							self.response.set_status(400)
						else:
							boat.at_sea = True
							boat.put()
							slip_data.current_boat = patch_data['current_boat']
							slip_data.arrival_date = None
							slip_data.put()
					if patch_data['current_boat'] is not None and slip_data.current_boat is None:
						try:
							boat = ndb.Key(urlsafe=(patch_data['current_boat'])).get()
						except Exception:
							boat = None
						if boat is None:
							self.response.set_status(400)
						else:
							boat.at_sea = False
							boat.put()
							slip_data.current_boat = patch_data['current_boat']
							slip_data.arrival_date = datetime.strftime(datetime.utcnow().date(), "%d/%m/%y")
							slip_data.put()
					if patch_data['current_boat'] is not None and slip_data.current_boat is not None:
						self.response.set_status(403)
						# already boat inside, cant put another. 
				slip_dict = slip_data.to_dict()
				slip_dict['self'] = '/slip/' + slip_data.id
				self.response.write(json.dumps(slip_dict))
		else:
			self.response.set_status(400)	
	
	def delete(self, id=None):
		if id:
			try:
				slip_to_delete = ndb.Key(urlsafe=id).get()
			except Exception:
				slip_to_delete = None
			if slip_to_delete is None:
				self.response.set_status(400)
			else:
				if slip_to_delete.current_boat == None:
					slip_to_delete.key.delete()
				else:
					boattosea = ndb.Key(urlsafe=(slip_to_delete.current_boat)).get()
					boattosea.at_sea = True
					boattosea.put()
					slip_to_delete.key.delete()
		else:
			self.response.set_status(400)
# [END SlipHandler]

# [START MainPage]
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write('Hello')
# [END MainPage]

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/boat', BoatHandler),
	('/boat/(.*)', BoatHandler),
	('/slip', SlipHandler),
	('/slip/(.*)', SlipHandler)
], debug=True)
# [END app}