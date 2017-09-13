import json
from urllib import parse

import falcon
from playhouse.shortcuts import model_to_dict

from superweb import database
from superweb.base import render_template, json_serializer_handler

import datetime


class ToDoJsonList:
    def on_get(self, req, resp):
        tasks = database.Task.select()

        tasks_list = []
        for t in tasks:
            tasks_list.append(model_to_dict(t))

        tasks_json = json.dumps(tasks_list, default=json_serializer_handler)

        resp.content_type = 'application/json'
        resp.body = tasks_json


class ToDoList:
    def on_get(self, req, resp):
        tasks = database.Task.select().where(database.Task.is_completed == False)

        tasks_list = []
        for t in tasks:
            tasks_list.append(model_to_dict(t))

        resp.content_type = 'text/html'
        resp.body = render_template('todo_list.jinja2', {'tasks': tasks_list})


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
        resp.body = render_template('todo_list.jinja2', {'tasks': tasks_list})


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
