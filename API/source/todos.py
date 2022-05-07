from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity


todos=Blueprint("todos", __name__, url_prefix='/api/v1/todos')

@todos.route('/add', methods=['POST'])
@jwt_required()
def add():
    user_obj_id = get_jwt_identity()
    header = request.json['header']
    detail = request.json['detail']
    todo=jsonify({
        'header': header,
        'detail': detail,
        'iscompleted': False,
        'userid': user_obj_id
    })
    current_app.db.todos.insert_one({
        'header': header,
        'detail': detail,
        'iscompleted': False,
        'userid': user_obj_id
    })
    return jsonify({'message': "Todo is added"}), 200

@todos.route('/update/<oid>', methods=['PUT'])
def update():
    return 'update selected todo'    

@todos.route('/delete/<oid>', methods=['DELETE'])
def delete():
    return 'delete selected todo'

@todos.route('/delete_completed', methods=['DELETE'])
def delete_completed():
    return 'delete completed todos'


@todos.route('/', methods=['GET'])
@jwt_required()
def get_all():
    user_obj_id = get_jwt_identity()
    
    todos = current_app.db.todos.find({'userid': user_obj_id})
    
    todo_list=[]
    
    for todo in todos:
        
        new_todo = {
            '_id': str(todo['_id']),
            'header': todo['header'],
            'detail': todo['detail'],
            'iscompleted': todo['iscompleted'],
            'userid': todo['userid']
        }
        
        todo_list.append(new_todo)
    
    return jsonify({'todo_list':todo_list}), 200

@todos.route('/<oid>', methods=['GET'])
@jwt_required()
def get(oid):
    todo = current_app.db.todos.find_one({'_id': ObjectId(oid)})
    return jsonify({
            '_id': str(todo['_id']),
            'header': todo['header'],
            'detail': todo['detail'],
            'iscompleted': todo['iscompleted'],
            'userid': todo['userid']
        }), 200
    