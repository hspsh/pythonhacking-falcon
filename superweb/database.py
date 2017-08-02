from peewee import *
from datetime import datetime


db = SqliteDatabase('todo.db')

class Task(Model):
    title = CharField()
    description = CharField(null=True)
    completion = BooleanField(default=False)
    creation_time = DateTimeField(default=datetime.now)

    class Meta:
        database = db # This model uses the "people.db" database.
