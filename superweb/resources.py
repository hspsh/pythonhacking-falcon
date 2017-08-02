import datetime
import json
from urllib import parse

import falcon
from playhouse.shortcuts import model_to_dict

from superweb import database


def dt_handler(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    else:
        return None


class ToDoList:
    def on_get(self, req, resp):
        tasks = database.Task.select()
        tasks_list = []
        for t in tasks:
            tasks_list.append(model_to_dict(t))
        tasks_json = json.dumps(tasks_list, default=dt_handler)
        resp.content_type = 'application/json'
        resp.body = tasks_json


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

        task_item = database.Task(title=req_args['title'][0],
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

        tasks = database.Task.select()

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
