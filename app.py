from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, emit, send, join_room, leave_room
import pprint
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager


app = Flask(__name__)
login_manager = LoginManager()
csrf = CSRFProtect(app)
CORS(app)
cors = CORS(app,
    resources={
        r"/*": {
            "origins": "*" # localhost:5000, 0.0.0.0:5000
        }
})


app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = False
app.config['USE_RELOADER'] = True
csrf.init_app(app)
login_manager.init_app(app)
socketio = SocketIO(app, async_mode='threading', debug=False)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id) # fetch the user id from db


@app.route('/enter', methods=['POST', 'GET'])
def enter():
    client_id = 0
    if request.method == 'POST':
        client_id = request.form.get('client_id')
        if client_id == 0:
            return render_template('enter.html', message='Введите коректный id')
        else:
            return redirect(url_for('client', client_id = client_id))

    return render_template('enter.html')


@app.route('/client/<int:client_id>')
def client(client_id):
   return render_template('index.html', message = client_id)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@socketio.on('connect')
def test_connect():
    print('Corent sid is:', request.sid)
    print('Ip', request.remote_addr)
    emit('my response', {'data': 'Connected'})

@socketio.on('rbpi')
def message_from_rasberry(data):
    print(pprint.pprint(data))

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

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data['data'] )
    print(data)
    send(data['data'])

@socketio.on('room message')
def get_room_mesage(message):
    emit('broadcast message', {'data': message['data']}, room=message['room'])
@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, port=5000)

