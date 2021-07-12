import sys
sys.path.insert(0, r'/home/alexandr/work_test/Todo/TodosGarpix')

import datetime
from flask import abort
from sqlalchemy.dialects.postgresql import JSON
from ap.base import db


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
