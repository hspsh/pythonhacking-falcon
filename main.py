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
<input type="text" name="title">
<input type="text" name="description">
<input type="submit" name="button" value="create">
</form>
</body>
</html>
'''

    def on_post(self, req, resp):
        req_args = parse.parse_qs(req.stream.read().decode('utf-8'))  # get the message and parse it to dictionary

        task_item = fdb.Task(title=req_args['title'][0],
                             description=req_args['description'][0])
        task_item.save()  # bob is now stored in the database
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = 'application/json'
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

        tasks = fdb.Task.select()

        tasks_list = []

        for p in tasks:
            d = {
                'title': p.title,
                'completion': p.completion,
                'creation_time': str(p.creation_time)
            }
            tasks_list.append(d)

        content = {'tasks': tasks_list}
        resp.body = json.dumps(content)



app = falcon.API()

things = ThingsResource()
json_resource = JsonResource()
db_resource = DBResource()

app.add_route('/todo', things)
app.add_route('/other', json_resource)
app.add_route('/db', db_resource)

httpd = make_server('', 8000, app)
print("Serving on port 8000...")

httpd.serve_forever()
