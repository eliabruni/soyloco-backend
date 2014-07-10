from google.appengine.ext import ndb

# XXX implement to_dict() method (nested) to return also id

class GPSLocation(ndb.Model):
    longitude = ndb.FloatProperty(required=True, indexed=False)
    latitude = ndb.FloatProperty(required=True, indexed=False)

class User(ndb.Model):
    # id of the user on facebook
    fid = ndb.StringProperty(required=True)
    signup_date = ndb.DateTimeProperty(required=True, indexed=False)
    last_login = ndb.DateTimeProperty(required=True, indexed=False)
    # basic profile
    first_name = ndb.StringProperty(required=True, indexed=False)
    last_name = ndb.StringProperty(required=True, indexed=False)
    fb_key = ndb.StringProperty(required=True, indexed=False)
    gender = ndb.StringProperty(required=True, choices=["male", "female"], indexed=False)
    age = ndb.IntegerProperty(required=True, indexed=False) # have to see this
    gps_location = ndb.StructuredProperty(GPSLocation, required=True, indexed=False)
    radius = ndb.IntegerProperty(required=True, indexed=False)
    # photos: list of urls of photos
    photos = ndb.StringProperty(repeated=True, indexed=False)
    # url of the profile photo
    profile_photo = ndb.StringProperty(required=True, indexed=False)

class Likes(ndb.Model):
    # fid of the source of the like
    source = ndb.StringProperty(required=True)
    # fid of the page
    page = ndb.StringProperty(required=True)

class Friendship(ndb.Model):
    # fid of the source of the relationship
    source = ndb.StringProperty(required=True)
    # fid of the destionation of the relationship
    destination = ndb.StringProperty(required=True)

class Swipe(ndb.Model):
    # fid of the swiper
    source = ndb.StringProperty(required=True)
    # fid of the swiped
    destination = ndb.StringProperty(required=True)
    # action {0: no, 1: yes}
    swipe_type = ndb.IntegerProperty(required=True, choices=[0, 1], indexed=False)

class RSVP(ndb.Model):
    # fid of the user
    user = ndb.StringProperty(required=True)
    # fid of the event
    event = ndb.StringProperty(required=True)
    # the rsvp answer {0: no, 1: yes, 2: maybe}
    rsvp = ndb.IntegerProperty(required=True, choices=[0, 1, 2], indexed=False)

class Page(ndb.Model):
    # id of the page on facebook
    fid = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True, indexed=False)
    # the url of the page icon
    icon = ndb.StringProperty(required=True, indexed=False)

class Location(ndb.Model):
    country = ndb.StringProperty(required=True, indexed=False)
    city = ndb.StringProperty(required=True, indexed=False)
    street = ndb.StringProperty(required=True, indexed=False)
    zip = ndb.StringProperty(required=True, indexed=False)
    state = ndb.StringProperty(required=True, indexed=False)
    gps_location = ndb.StructuredProperty(GPSLocation, required=True, indexed=False)

class Place(ndb.Model):
    fid = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True, indexed=False)
    description = ndb.TextProperty(indexed=False)
    # url of the page icon
    icon = ndb.StringProperty(required=True, indexed=False)
    place_type = ndb.StringProperty(required=True, choices=["Night Club", "Restaurant"], indexed=False)
    location = ndb.StructuredProperty(Location, required=True, indexed=False)

class Event(ndb.Model):
    # id of the event on facebook
    fid = ndb.StringProperty(required=True)
    name = ndb.StringProperty(required=True, indexed=False)
    description = ndb.TextProperty(required=True, indexed=False)
    # url of the cover photo
    cover = ndb.StringProperty(indexed=False)
    place = ndb.StringProperty(required=True)
    # need to see if these are required, and what to do for multi-days events
    start_time = ndb.DateTimeProperty()
    end_time = ndb.DateTimeProperty()
