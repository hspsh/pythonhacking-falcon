from superweb import database

database.db.connect()

tables = [database.Task]
database.db.drop_tables(tables)
database.db.create_tables(tables)
