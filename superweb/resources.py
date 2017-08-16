import json
from urllib import parse

import falcon
from playhouse.shortcuts import model_to_dict

from superweb import database
from superweb.base import render_template, json_serializer_handler


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
        tasks = database.Task.select()

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

        task_item = database.Task(title=req_args['title'][0],
                                  description=req_args['description'][0])

        # Zapisujemy obiekt task do bazy danych.
        task_item.save()

        raise falcon.HTTPSeeOther('/todo/')


class JsonHello:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'application/json'
        content = {'message': 'Hello World!'}
        resp.body = json.dumps(content)
