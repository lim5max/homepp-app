import socketio
sio = socketio.Client(logger=True,engineio_logger=True )
@sio.event
def connect():
    print("I'm connected!")
    
    sio.send({'data': 'rasberry'})

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def get_data(sid, data):
    print(data['data'])
    return 'rbpi-connected'

@sio.event
def disconnect():
    print("I'm disconnected!")
sio.connect('http://localhost:5000')
try:

    sio.wait()
except KeyboardInterrupt:
    sio.disconnect()
    sio.eio.disconnect(True)
    exit()