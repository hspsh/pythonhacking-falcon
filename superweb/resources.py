import json
from urllib import parse

import falcon
from playhouse.shortcuts import model_to_dict

from superweb import database
from superweb.base import render_template, json_serializer_handler

import datetime

APPLICATION_JSON = 'application/json'


def json_dumps(obj):
    return json.dumps(obj, default=json_serializer_handler)


class ToDoJsonList:
    def on_get(self, req, resp):
        tasks = database.Task.select()

        tasks_list = []
        for t in tasks:
            tasks_list.append(model_to_dict(t))

        tasks_json = json_dumps(tasks_list)

        resp.content_type = 'application/json'
        resp.body = tasks_json


class ToDoList:
    def on_get(self, req, resp):
        tasks = database.Task.select().where(database.Task.is_completed == False)

        tasks_list = []
        for t in tasks:
            tasks_list.append(model_to_dict(t))

        resp.content_type = 'text/html'
        resp.body = render_template('todo_list.jinja2', {'tasks': tasks_list, 'now': datetime.datetime.now()})


class ToDo:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = render_template('todo_add.jinja2')

    def on_post(self, req, resp):
        # Odkodowanie danych
        data = req.stream.read().decode('utf-8')

        # parsowanie danych
        req_args = parse.parse_qs(data)

        title = req_args['title'][0]
        description = req_args['description'][0]
        deadline_at = req_args['deadline_at'][0] if 'deadline_at' in req_args else None

        if deadline_at is not None:
            deadline_at = datetime.datetime.strptime(deadline_at, "%Y-%m-%S")  # this will raise ValueError on format mismatch

        database.Task.insert(title=title, description=description,
                             deadline_at=deadline_at).execute()

        raise falcon.HTTPSeeOther('/todo/')


class ToDoComplete:
    def on_put(self, req, resp, task_id):
        task_id = int(task_id)

        query = database.Task.update(is_completed=True, completed_at=datetime.datetime.now()).where(database.Task.id == task_id)
        query.execute()

        raise falcon.HTTPSeeOther('/todo/')


class ToDoTaskCompleted:
    def on_get(self, req, resp):
        completed_task = database.Task.select().where(database.Task.is_completed == True)
        tasks_list = []
        for t in completed_task:
            tasks_list.append(model_to_dict(t))

        resp.content_type = 'text/html'
        resp.body = render_template('todo_list.jinja2', {'tasks': tasks_list, 'now': datetime.datetime.now()})


class JsonHello:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        content = {'message': 'Hello World!'}
        resp.body = json.dumps(content)


class Index:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        resp.body = render_template('index.jinja2')


class TodoTaskResource:
    # Rules for implementing respective verbs:
    # http://www.restapitutorial.com/lessons/httpmethods.html
    def on_post(self, req, resp, task_id):
        try:
            database.Task.get(database.Task.id == task_id)
        except database.DoesNotExist:
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            resp.status = falcon.HTTP_CONFLICT

    def on_get(self, req, resp, task_id):
        try:
            item_to_get = database.Task.get(database.Task.id == task_id)
        except database.DoesNotExist:
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            resp.body = json_dumps(model_to_dict(item_to_get))
            resp.status = falcon.HTTP_OK
            resp.content_type = APPLICATION_JSON

    def on_delete(self, req, resp, task_id):
        try:
            item_to_delete = database.Task.get(database.Task.id == task_id)
        except database.DoesNotExist:
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            item_to_delete.delete_instance()
            resp.status = falcon.HTTP_OK

    def on_put(self, req, resp, task_id):
        try:
            item_to_update = database.Task.get(database.Task.id == task_id)
        except database.DoesNotExist:
            resp.status = falcon.HTTP_NOT_FOUND
        else:
            data = json.loads(req.stream.read().decode('utf-8'))
            item_to_update.update(**data).execute()
            resp.status = falcon.HTTP_OK

    def on_patch(self, req, resp, task_id):
        # TBD: do we need it?
        resp.status = falcon.HTTP_METHOD_NOT_ALLOWED


class TodoTasksResource:
    # Rules for implementing respective verbs:
    # http://www.restapitutorial.com/lessons/httpmethods.html
    def on_post(self, req, resp):
        data = json.loads(req.stream.read().decode('utf-8'))
        title = data['title']
        description = data['description']
        deadline_at = data.get('deadline_at')
        created_id = database.Task.insert(title=title,
                                          description=description,
                                          deadline_at=deadline_at).execute()
        resp.set_headers({'Location': '/api/todo_tasks/{}'.format(created_id)})
        resp.status = falcon.HTTP_CREATED

    def on_get(self, req, resp):
        # TODO: pagination, filtering
        database.Task.select()
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        resp.body = json_dumps([model_to_dict(t) for t in database.Task.select()])

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_METHOD_NOT_ALLOWED

    def on_put(self, req, resp):
        resp.status = falcon.HTTP_METHOD_NOT_ALLOWED

    def on_patch(self, req, resp, task_id):
        resp.status = falcon.HTTP_METHOD_NOT_ALLOWED
