import datetime
import json
import urllib
import webapp2

from datamodel import Event, Friendship, Likes, Page, Place, RSVP, Swipe, User
from exceptions import MissingProperty

from google.appengine.ext import ndb

class RestAPI(webapp2.RequestHandler):
    
    def create_envelope(self, api):    
        envelope = dict()
        envelope['API']= api
        return envelope            
    
    def jsonify(self, data):
        return json.dumps(data)
    
    def parse_request(self):
        json_string = urllib.unquote(self.request.body)
        return json.loads(json_string)

    def get_property(self, data, prop, required=False):
        if prop not in data:
            if required is False:
                return None
            else:
                raise MissingProperty(prop)
        else:
            return data[prop]
    
    def write_response(self, response):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(response)        

    def print_error(self, error):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.error(500)
        self.response.out.write(error)

class EventAPI(RestAPI):
    
    def get_all_events(self):
                    
        envelope = self.create_envelope('get_all_events')
        envelope['results'] = [ event.to_dict() for event in Event.query().fetch() ]
        self.write_response(self.jsonify(envelope)) 
        
    def get_single_event(self, fid):

        envelope = self.create_envelope('get_single_event')
        event = Event.query(Event.fid == fid).get()        
        if event is None:
            self.print_error("event does not exist")
            return
        
        envelope['event'] = event.to_dict()
        envelope['rsvps'] = [ rsvp.to_dict() for rsvp in RSVP.query(RSVP.event == fid).fetch() ]
        self.write_response(self.jsonify(envelope))
    
    def post_single_event(self):
        
        request = self.parse_request()        
        try:
            fid = self.get_property(request, 'fid', required=True) 
            name = self.get_property(request, 'name', required=True)
            place = self.get_property(request, 'place', required=True)
            description = self.get_property(request, 'description', required=True)
            cover = self.get_property(request, 'cover')
            start_time_s = self.get_property(request, 'start_time')
            # XXX fix this code
            start_time = datetime.datetime(start_time_s)
            end_time_s = self.get_property(request, 'end_time')
            end_time = datetime.datetime(end_time_s)
        except MissingProperty, e:
            self.print_error(e.printable_error())
            return
        except ValueError, e:
            self.print_error(e.printable_error())
            return
        
        ancor = ndb.Key("Place", place)
        event = Event(ancor=ancor, id=fid, fid=fid, name=name, description=description, place=place, cover=cover, start_time=start_time, end_time=end_time)
        event.put()

class PageAPI(RestAPI):
    
    def get_all_pages(self):
        
        envelope = self.create_envelope('get_all_pages')
        envelope['results'] = [ page.to_dict() for page in Page.query().fetch() ]
        self.write_response(self.jsonify(envelope))
        
    def get_single_page(self, fid):

        envelope = self.create_envelope('get_single_page')
        page = ndb.Key("Page", fid).get()
        if page is None:
            self.print_error("page does not exist")
            return
    
        envelope['page'] = page.to_dict()
        envelope['likes'] = [ like.to_dict() for like in Likes.query(Likes.page == fid).fetch() ]
        self.write_response(self.jsonify(envelope))

    def post_single_page(self):
        
        request = self.parse_request()
        try:
            fid = self.get_property(request, 'fid', required=True) 
            name = self.get_property(request, 'name', required=True)
            icon = self.get_property(request, 'icon')
        except MissingProperty, e:
            self.print_error(e.printable_error())
            return
        
        page = Page(id=fid, fid=fid, name=name, icon=icon)
        page.put()

class PlaceAPI(RestAPI):
    
    def get_all_places(self):
        
        envelope = self.create_envelope('get_all_places')
        envelope['results'] = [ place.to_dict() for place in Place.query().fetch() ]
        self.write_response(self.jsonify(envelope))
        
    def get_single_place(self, fid):
        
        envelope = self.create_envelope('get_single_place')
        place = ndb.Key("Place", fid).get()
        if place is None:
            self.print_error("place does not exist")
            return

        envelope['place'] = place.to_dict()
        envelope['events'] = [ event.to_dict() for event in Event.query(ancestor=place).fetch() ]
        envelope['likes'] = [ like.to_dict() for like in Likes.query(Likes.page == fid).fetch() ]
        self.write_response(self.jsonify(envelope))

    def post_single_place(self):
        
        request = self.parse_request()
        try:
            fid = self.get_property(request, 'fid', required=True) 
            name = self.get_property(request, 'name', required=True)
            description = self.get_property(request, 'description', required=True)
            icon = self.get_property(request, 'icon')
            place_type = self.get_property(request, 'place_type', required=True)
            location_data = self.get_property(request, 'location', required=True)
            latitude = self.get_property(location_data, 'latitude', required=True)
        except MissingProperty, e:
            self.print_error(e.printable_error())
            return
        
        place = Place(id=fid, fid=fid, name=name, description=description, icon=icon, place_type=place_type)
        place.put()

class UserAPI(RestAPI):
    
    def get_all_users(self):
        
        envelope = self.create_envelope('get_all_users')
        envelope['results'] = [ user.to_dict() for user in User.query().fetch() ]
        self.write_response(self.jsonify(envelope))
        
    def get_single_user(self, fid):
                
        envelope = self.create_envelope('get_single_user')                
        user = ndb.Key("User", fid).get()
        if user is None:
            self.print_error("user does not exist")
            return
        
        envelope['friends'] = [ friend.to_dict() for friend in Friendship.query(ancestor=user).fetch() ]
        envelope['likes'] = [ like.to_dict() for like in Likes.query(ancestor=user).fetch() ]
        envelope['rsvps'] = [ rsvp.to_dict() for rsvp in RSVP.query(ancestor=user).fetch() ]
        envelope['swiped'] = [ swipe.to_dict() for swipe in Swipe.query(ancestor=user).fetch() ]
        envelope['swiped_by'] = [ swiped.to_dict() for swiped in Swipe.query(Swipe.destination == fid).fetch() ]
        self.write_response(self.jsonify(envelope))
