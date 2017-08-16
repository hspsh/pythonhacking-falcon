from superweb import database

database.db.connect()

database.db.create_tables([database.Task])
