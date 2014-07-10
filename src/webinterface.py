import webapp2

from datamodel import Event, Friendship, Likes, Page, Place, RSVP, Swipe, User

from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

class WebView(webapp2.RequestHandler):

    def print_error(self, error):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(error)        

class EventWebView(WebView):
            
    def get_all_events(self):
        
        events = Event.query().fetch()
        self.response.write(template.render("templates/events.html", 
                                            {'events': events}))
        
    def get_single_event(self, fid):
        
        event = Event.query(Event.fid == fid).get()        
        if event is None:
            self.print_error("event does not exist")
            return
        
        rsvps = RSVP.query(RSVP.event == fid).fetch()
        
        self.response.write(template.render("templates/event.html", 
                                            {'event': event,
                                             'rsvps': rsvps}))

class PageWebView(WebView):

    def get_all_pages(self):
                
        pages = Page.query().fetch()
        self.response.write(template.render("templates/pages.html", 
                                            {'pages': pages}))

    def get_single_page(self, fid):
        
        page = ndb.Key("Page", fid).get()
        if page is None:
            self.print_error("page does not exist")
            return
        
        likes = Likes.query(Likes.page == fid).fetch()
        
        self.response.write(template.render("templates/page.html", 
                                            {'page': page,
                                             'likes': likes}))

class PlaceWebView(WebView):
    
    def get_all_places(self):
        
        places = Place.query().fetch()
        self.response.write(template.render("templates/places.html", 
                                            {'places': places}))        
        
    def get_single_place(self, fid):

        place = ndb.Key("Place", fid).get()
        if place is None:
            self.print_error("place does not exist")
            return

        events = Event.query(ancestor=place).fetch()
        likes = Likes.query(Likes.page == fid).fetch()
        
        self.response.write(template.render("templates/place.html", 
                                            {'place': place,
                                             'events': events,
                                             'likes': likes}))

class UserWebView(WebView):
    
    def get_all_users(self):
        
        users = User.query().fetch()
        self.response.write(template.render("templates/users.html", 
                                            {'users': users}))               
    
    def get_single_user(self, fid):
                
        user = ndb.Key("User", fid).get()
        if user is None:
            self.print_error("user does not exist")
            return
        
        friends = Friendship.query(ancestor=user).fetch()
        likes = Likes.query(ancestor=user).fetch()
        rsvps = RSVP.query(ancestor=user).fetch()
        swiped = Swipe.query(ancestor=user).fetch()
        swiped_by = Swipe.query(Swipe.destination == fid).fetch()

        self.response.out.write(template.render("templates/user.html", 
                                                {'user': user, 
                                                 'friends': friends,
                                                 'likes': likes,
                                                 'rsvps': rsvps, 
                                                 'swiped': swiped, 
                                                 'swiped_by': swiped_by}))

class Home(WebView):
    
    def get(self):
        self.print_error("no homepage set!")
        return
