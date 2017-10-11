from superweb import database

database.backend.connect()

tables = [database.Task]
database.backend.drop_tables(tables)
database.backend.create_tables(tables)
