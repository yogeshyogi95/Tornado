import datetime
import json
from todo.models import User, Task
from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin

class BaseView(RequestHandler, SessionMixin):
    """Base view for this application"""

    def prepare(self):
        self.form_data = {
            key: [val.decode('utf-8') for val in val_list]
            for key, val_list in self.request.arguments.items()
        }

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

class HomePage(BaseView):
    """Home Page"""
    SUPPORTED_METHODS = ("GET", "POST",)

    def get(self):
        self.write("Hello World!")


class TaskListView(BaseView):
    """View for reading and adding new tasks."""
    SUPPORTED_METHODS = ("GET", "POST",)

    async def get(self, username):
        """Get all tasks for an existing user."""
        with self.make_session() as session:
            user = await (session.query(User).filter(User.username == username))
            if user:
                tasks = [task.to_dict() for task in user.tasks]
                self.send_response({
                    'username': user.username,
                    'tasks': tasks
                })
            else:
                self.send_response({
                    'message': 'user does not exist'
                })

    async def post(self, username):
        """Create a task"""
        with self.make_session() as session:
            user = await (session.query(User).filter(User.username == username))
            if user:
                due_date = self.form_data['due_data'][0]
                task = Task(
                    name = self.form_data['name'][0],
                    note = self.form_data['note'][0],
                    creation_date = datetime.now(),
                    due_date = datetime.strptime(due_date, '%d/%m/%Y %H:%M:%s'),
                    completed = self.form_data['completed'][0],
                    user_id = user.id,
                    user = user
                )
                session.add(task)
                self.send_response({'msg': 'posted'}, status=201)