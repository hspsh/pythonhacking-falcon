import json
from urllib import parse
from wsgiref.simple_server import make_server
import fdb
import falcon


class ThingsResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h2>Body</h2>
<form method="post">
<input type="text" name="input">
<input type="submit" name="button" value="submit">
</form>
</body>
</html>
'''

    def on_post(self, req, resp):
        req_args = parse.parse_qs(req.stream.read().decode('utf-8'))  # get the message and parse it to dictionary
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = 'text/json'
        resp.body = json.dumps(req_args)


class JsonResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        content = {'message': 'Hello World!'}
        resp.body = json.dumps(content)




class DBResource:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'

        peoples = fdb.Person.select()

        people_list = []

        for p in peoples:
            d = {
                'name': p.name,
                'birth': str(p.birthday)
            }
            people_list.append(d)

        content = {'people': people_list}
        resp.body = json.dumps(content)



app = falcon.API()

things = ThingsResource()
json_resource = JsonResource()
db_resource = DBResource()

app.add_route('/things', things)
app.add_route('/other', json_resource)
app.add_route('/db', db_resource)

httpd = make_server('', 8000, app)
print("Serving on port 8000...")

httpd.serve_forever()
