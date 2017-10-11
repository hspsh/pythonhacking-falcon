from wsgiref.simple_server import make_server
from . import app
httpd = make_server('', 8000, app)
print("Serving on port 8000...")
httpd.serve_forever()
