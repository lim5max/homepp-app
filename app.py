import os 
from app import create_app, db
from flask import Flask, render_template, redirect, request, url_for, session
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import pprint
from flask_session import Session
from app.models import User
from app.forms import LoginForm
from flask_login import login_required, current_user
app = create_app()
Session(app)
socketio = SocketIO(app, async_mode='threading', debug=False, manage_sessio=False)



# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id) # fetch the user id from db

@app.route("/hello")
@login_required
def hello():
    return render_template('hello.html')

@app.route('/enter', methods=['POST', 'GET'])
@login_required
def enter():
    client_id = 0
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        if client_id == 0:
            return render_template('enter.html', message='Введите коректный id')
        else:
            print(client_id)
            return redirect(url_for('client', client_id = str(client_id)))

    return render_template('enter.html')


@app.route('/client/<string:client_id>')
@login_required
def client(client_id):
   return render_template('index.html', message = client_id)


#Работа с сокетами

@socketio.on('connect')
def test_connect():
    sid = request.sid

    if current_user.is_anonymous or :
        return False
    print('current sid is: ', request.sid)
    print('current ip adderess is: ', request.remote_addr)
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('rbpi')
def message_from_rasberry(data):
    print(pprint.pprint(data))


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data['data'] )
    print(data)
    send(data['data'])

#работа с комнатой
@socketio.on('join')
def on_join(data):
    print(data)
    username = data['username']
    room = data['room']
    join_room(room)
    message = '%s joined %s' % (username, room)
    emit('broadcast message', {'data': message}, room=room)
    print('joined')


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(f'{username} leave room ({room})')



@socketio.on('room message')
def get_room_mesage(message):
    #from_who(message)
    emit('broadcast message', {'data': message['data']}, room=message['room'])


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

if __name__ == '__main__':
    socketio.run(app, port=5000)
    print(app.config.get('SQLALCHEMY_DATABASE_URI'))

