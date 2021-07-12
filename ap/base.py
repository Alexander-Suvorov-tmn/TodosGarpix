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

todo = ns.model(
    "Todo",
    {
        "id": fields.Integer(readonly=True, description="The task unique identifier"),
        "title": fields.String(required=True, description="The title task"),
        "content": fields.String(required=True, description="The content task"),
        "create_at": fields.DateTime(required=True, description="Create date"),
    },
)

todo_create = ns.model(
    "Todo_create",
    {
        "title": fields.String(required=True, description="The title task"),
        "content": fields.String(required=True, description="Create date"),
    },
)

todo_list = ns.model(
    "Todo_list",
    {
        "id": fields.Integer(readonly=True, description="The task unique identifier"),
        "title": fields.String(required=True, description="The title task"),
        "create_at": fields.DateTime(required=True, description="Create date"),
    },
)

todo_details = ns.model(
    "Todo_detail",
    {
        "title": fields.String(required=True, description="The title task"),
        "content": fields.String(required=True, description="Create date"),
        "create_at": fields.DateTime(required=True, description="Create date"),
    },
)


class Todo(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.String())
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Todo title {self.title}>"

    def todo_get_all(self):
        tasks = Todo.query.all()
        results = [
            {
                "id": task.id,
                "title": task.title,
                "content": task.content,
                "create_at": task.create_at,
            }
            for task in tasks
        ]
        return results

    def todo_create(self, data):
        head = Todo(title=data["title"], content=data["content"])
        db.session.add(head)
        db.session.commit()
        return head

    def todo_update(self, id, data):
        task = Todo.query.get_or_404(id)
        if not "title" in data:
            abort(400)
        if not "content" in data:
            abort(400)
        task.title = data["title"]
        task.content = data["content"]
        db.session.add(task)
        db.session.commit()
        return task

    def todo_delete(self, id):
        task = Todo.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()

    def get_todo(self, id):
        task = Todo.query.get_or_404(id)
        return task
        
DAO = Todo()


@ns.route("/")
class TodoList(Resource):
    @ns.doc("list_todos")
    @ns.marshal_list_with(todo_list)
    def get(self):
        return DAO.todo_get_all()

    @ns.doc("create_todo")
    @ns.expect(todo_create)
    @ns.marshal_with(todo, code=201)
    def post(self):
        return DAO.todo_create(request.json), 201


@ns.route("/<int:id>")
@ns.response(404, "Todo not found")
@ns.param("id", "The task identifier")
class Todos(Resource):
    @ns.doc("get_todo")
    @ns.marshal_with(todo_details)
    def get(self, id):
        return DAO.get_todo(id)

    @ns.doc("delete_todo")
    @ns.response(204, "Todo deleted")
    def delete(self, id):
        DAO.todo_delete(id)
        return "", 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        return DAO.todo_update(id, request.json)


if __name__ == "__main__":
    app.run(debug=True)
