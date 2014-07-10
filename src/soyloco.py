import webapp2

from webinterface import EventWebView, Home, PageWebView, PlaceWebView, UserWebView

from google.appengine.ext.webapp.util import run_wsgi_app



application = webapp2.WSGIApplication([webapp2.Route(r'/web/events/<fid:(\d+)>', handler=EventWebView, handler_method='get_single_event', name='single_event', methods=['GET']),
                                       webapp2.Route(r'/web/events/', handler=EventWebView, handler_method='get_all_events', name='all_events', methods=['GET']),
                                       webapp2.Route(r'/web/pages/<fid:(\d+)>', handler=PageWebView, handler_method='get_single_page', name='single_page', methods=['GET']),
                                       webapp2.Route(r'/web/pages/', handler=PageWebView, handler_method='get_all_pages', name='all_pages', methods=['GET']),
                                       webapp2.Route(r'/web/places/<fid:(\d+)>', handler=PlaceWebView, handler_method='get_single_place', name='single_place', methods=['GET']),
                                       webapp2.Route(r'/web/places/', handler=PlaceWebView, handler_method='get_all_places', name='all_places', methods=['GET']),
                                       webapp2.Route(r'/web/users/<fid:(\d+)>', handler=UserWebView, handler_method='get_single_user', name='single_user', methods=['GET']),
                                       webapp2.Route(r'/web/users/', handler=UserWebView, handler_method='get_all_users', name='all_users', methods=['GET']),
                                       webapp2.Route(r'/', handler=Home, name='home', methods=['GET'])
                                       ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
