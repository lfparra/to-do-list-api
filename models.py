from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ToDoList(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    tasks = db.Column(db.String(250), nullable=False)
    

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "tasks": self.tasks,
        }
