from http.server import HTTPServer, SimpleHTTPRequestHandler
import pgmeta
import dbexec

page ="""
<html>
 <body>
    TODO: create a canvas tag, and call nomnoml.draw to fill in the canvas
          See https://github.com/skanaar/nomnoml for sample code.
 </body>
</html>
"""

class PGMetaHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/meta":
            TODO:  Same code as pyweb.py. Only page needs a change
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        SimpleHTTPRequestHandler.do_GET(self)        

httpd = HTTPServer( ('', 8000), PGMetaHandler)
httpd.serve_forever()
