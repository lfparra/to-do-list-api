from flask import Flask, jsonify, request
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, ToDoList
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/database' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:leoparra@localhost:3306/todolist' 
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)

@app.route('/todos/user/<username>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def todolist(username):
    if request.method == 'GET':
        todolist = ToDoList.query.filter_by(username=username).first()
        if not todolist:
            return jsonify({"msg": "User not found"}), 404
        else:
            return jsonify(json.loads(todolist.tasks)), 200

    if request.method == 'POST':

        body = request.get_json()
        todolist = ToDoList.query.filter_by(username=username).first()
        if todolist:
            return jsonify({"msg": "Username is registered"})
            
        todolist = ToDoList()
        todolist.username = username
        todolist.tasks = json.dumps(body)

        db.session.add(todolist)
        db.session.commit()

        return jsonify({"result": "ok"}), 201
    
    if request.method == 'PUT':

        body = request.get_json()
        todolist = ToDoList.query.filter_by(username=username).first()
        if not todolist:
            return jsonify({"msg": "Username not found"})
            
        todolist.tasks = json.dumps(body)

        db.session.commit()

        return jsonify({"result": "A list with " + str(len(body))  +" todos was succesfully saved"}), 201

    if request.method == 'DELETE':
        todolist = ToDoList.query.filter_by(username=username).first()
        if not todolist:
            return jsonify({"msg": "Username not found"})

        db.session.delete(todolist)
        db.session.commit()

        return jsonify({"result": "ok"}), 201

if __name__ == '__main__':
    manager.run()