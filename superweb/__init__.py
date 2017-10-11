import falcon

from superweb import resources

app = falcon.API()

app.add_route('/', resources.Index())
app.add_route('/todo/add', resources.ToDo())
app.add_route('/todo/complete/{task_id}', resources.ToDoComplete())
app.add_route('/todo/completed', resources.ToDoTaskCompleted())
app.add_route('/todo/', resources.ToDoList())
app.add_route('/json_hello', resources.JsonHello())
app.add_route('/api/todo_tasks/{task_id}', resources.TodoTaskResource())
app.add_route('/api/todo_tasks', resources.TodoTasksResource())
