from flask import Flask, render_template, redirect, request, url_for
from flask_socketio import SocketIO, emit, send
import pprint
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading')



@app.route('/enter', methods=['POST', 'GET'])
def enter():
    client_id = 0
    if request.method == 'POST':
        client_id = int(request.form.get('client_id'))
        if client_id == 0:
            return render_template('enter.html', message='Введите коректный id')
        else:
            return redirect(url_for('client', client_id = client_id))

    return render_template('enter.html')


@app.route('/client/<int:client_id>')
def client(client_id):
   return render_template('index.html', message = client_id)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('rbpi')
def message_from_rasberry(data):
    print(pprint.pprint(data))


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data['data'] )
    print(data)

    send(data['data'])


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)