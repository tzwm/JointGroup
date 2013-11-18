import xmpp

import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp.util import run_wsgi_app

import webapp2


class GroupUser(ndb.Model):
    user_email = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write('<html><body>')

        greetings_query = GroupUser.query().order(-GroupUser.date)
        greetings = greetings_query.fetch(10)

        for greeting in greetings:
            self.response.write('<blockquote>%s</blockquote>' %
                                cgi.escape(greeting.user_email))


        self.response.write('</html></body>')


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/_ah/xmpp/message/chat/', xmpp.XMPPHandler),
], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

