import socketio
sio = socketio.Client(logger=True,engineio_logger=True )
@sio.event
def connect():
    print("I'm connected!")
    
    #sio.send({'data': 'rasberry'})
    sio.emit('join', {'room': '123', 'username': 'web-client'})
@sio.event
def connect_error():
    print("The connection failed!")

@sio.on('broadcast message')
def broadcast_get_message(message):
    print(message['data'])

@sio.event
def disconnect():
    print("I'm disconnected!")

sio.connect('http://localhost:5000')
#sio.connect('http://5.187.2.162:5000')
try:

    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()
    sio.eio.disconnect(True)
    exit()