from datetime import datetime

from peewee import *

# Tworzymy obiekt bazy danych
db = SqliteDatabase('todo.db')


class Task(Model):
    title = CharField()
    description = CharField(null=True)
    completion = BooleanField(default=False)
    creation_time = DateTimeField(default=datetime.now)

    # Tutaj łączymy nasz model z bazą danych "db" zdefiniowaną wyżej.
    class Meta:
        database = db
