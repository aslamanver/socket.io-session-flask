from flask import Flask, render_template, session, request, copy_current_request_context
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect, send

async_mode = None
namespace = '/netm_realtime'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace=namespace)
def on_connect():
   
    print('-----------------------')
    print('Client connected - %s' + request.sid)
    print('-----------------------')


@socketio.on('disconnect', namespace=namespace)
def on_disconnect():

    print('-----------------------')
    print('Client disconnect - %s' + request.sid)
    print('-----------------------')


@socketio.on('server_event_global', namespace=namespace)
def on_server_event_global(message):

    print('-----------------------')
    print('on_server_event_global called from client => ' + message)
    print('-----------------------')

    emit('server_response', 'on_server_event_global => response from server sid : ' + request.sid, broadcast=True)


@socketio.on('server_event_room', namespace=namespace)
def on_server_event_room(message):

    print('-----------------------')
    print('on_server_event_room called from client => ' + message['room_id'])
    print('-----------------------')

    emit('server_response', 'on_server_event_room => response from server sid : ' + request.sid, room=message['room_id'])


@socketio.on('join', namespace=namespace)
def on_join(room_id):

    join_room(room_id)

    print('-----------------------')
    print('on_join called from client => ' + room_id)
    print('-----------------------')

    emit('server_response', 'on_join => room => ' + room_id, room=room_id)


@socketio.on('leave', namespace=namespace)
def on_leave(room_id):

    print('-----------------------')
    print('on_leave called from client => ' + room_id)
    print('-----------------------')

    emit('server_response', 'on_leave => room => ' + room_id, room=room_id)

    leave_room(room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5555)
