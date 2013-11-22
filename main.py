import XMPPHandler

import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app


class GetXML(webapp2.RequestHandler):

    def get(self):
        self.response.write('Hello World~')


app = webapp2.WSGIApplication([
    ('/_ah/xmpp/message/chat/', XMPPHandler.XMPPHandler),
    ('/getXML', GetXML)],
    debug=True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
