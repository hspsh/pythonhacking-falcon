import pathlib

from datetime import datetime

from peewee import *

# Tworzymy obiekt bazy danych
DB_PATH = str(pathlib.Path(__file__).with_name('todo.db'))
db = SqliteDatabase(DB_PATH)


class Task(Model):
    title = CharField()
    description = CharField(null=True)
    is_completed = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    completed_at = DateTimeField(null=True)
    deadline_at = DateTimeField(null=True)



    # Tutaj łączymy nasz model z bazą danych "db" zdefiniowaną wyżej.
    class Meta:
        database = db
