from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sdsdsdssss'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data['data'])

    send(data['data'])

    
if __name__ == '__main__': 
    socketio.run(app)
