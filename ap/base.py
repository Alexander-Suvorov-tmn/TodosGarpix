#!/usr/bin/python3
import sys


sys.path.insert(0, r'/home/alexandr/work_test/Todo/TodosGarpix')
# from ap.model import Todo
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_migrate import Migrate
from flask_restx import Api, Namespace, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

import datetime
from flask import abort

load_dotenv(".env")

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS"))
db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate()
if not (os.environ.get("APP_SETTINGS")) == "config. TestingConfig":
    migrate.init_app(app, db)
else:
    with app.app_context():
        db.create_all()

ns = Namespace("api/task", description="операции")
api = Api(app, version="1.0", title="Task", description="Планировщик задач")
api.add_namespace(ns)

task = ns.model(
    "Task",
    {
        "id": fields.Integer(readonly=True, description="The task unique identifier"),
        "title": fields.String(required=True, description="The title task"),
        "content": fields.String(required=True, description="The content task"),
        "create_at": fields.DateTime(required=True, description="Create date"),
    },
)

task_create = ns.model(
    "Task_create",
    {
        "title": fields.String(required=True, description="The title task"),
        "content": fields.String(required=True, description="Create date"),
    },
)

task_list = ns.model(
    "Task_list",
    {
        "id": fields.Integer(readonly=True, description="The task unique identifier"),
        "title": fields.String(required=True, description="The title task"),
        "create_at": fields.DateTime(required=True, description="Create date"),
    },
)

task_detail = ns.model(
    "Task_detail",
    {
        "title": fields.String(required=True, description="The title task"),
        "content": fields.String(required=True, description="Create date"),
        "create_at": fields.DateTime(required=True, description="Create date"),
    },
)



class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String())
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.title}>"

    def get_all_task(self):
        tasks = Task.query.all()
        results = [
            {"id": task.id, "title": task.title, "content": task.content, "create_at": task.create_at} for task in tasks
        ]
        return results

    def create_task(self, data):
        task = Task(title=data["title"], content=data["content"])
        db.session.add(task)
        db.session.commit()
        return task

    def get_task(self, id):
        task = Task.query.get_or_404(id)
        return task

    def update_task(self, id, data):
        task = Task.query.get_or_404(id)
        if not "title" in data:
            abort(400)
        if not "content" in data:
            abort(400)
        task.title = data["title"]
        task.content = data["content"]
        db.session.add(task)
        db.session.commit()
        return task

    def delete_task(self, id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        
DAO = Task()


@ns.route("/")
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @ns.doc("list_todos")
    @ns.marshal_list_with(task_list)
    def get(self):
        """List all tasks"""
        return DAO.get_all_task()

    @ns.doc("create_todo")
    @ns.expect(task_create)
    @ns.marshal_with(task, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create_task(request.json), 201


@ns.route("/<int:id>")
@ns.response(404, "Todo not found")
@ns.param("id", "The task identifier")
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @ns.doc("get_todo")
    @ns.marshal_with(task_detail)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get_task(id)

    @ns.doc("delete_todo")
    @ns.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete_task(id)
        return "", 204

    @ns.expect(task_create)
    @ns.marshal_with(task)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update_task(id, request.json)


if __name__ == "__main__":
    app.run(debug=True)
