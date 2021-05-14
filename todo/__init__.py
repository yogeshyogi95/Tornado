from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.options import define, options
from tornado_sqlalchemy import SQLAlchemy

database_url = "postgresql://postgres:password@localhost:5432/database"

from todo.views import TaskListView, HomePage

define('port', default=9999, help='port to listen to')


def main():
    """ Construct and serve the tornado application"""
    app = Application([
        ('/', HomePage),
        ('/tasks', TaskListView)
    ],
        db = SQLAlchemy(database_url)
    )
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print("Listening on http://localhost:{}".format(options.port))
    IOLoop.current().start()