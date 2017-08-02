from wsgiref.simple_server import make_server

import falcon

from superweb.resources import ThingsResource, JsonResource, DBResource, ToDoList

app = falcon.API()

things = ThingsResource()
json_resource = JsonResource()
db_resource = DBResource()
todo_list = ToDoList()

app.add_route('/todo', things)
app.add_route('/todo/list', todo_list)
app.add_route('/other', json_resource)
app.add_route('/db', db_resource)

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    print("Serving on port 8000...")
    httpd.serve_forever()
