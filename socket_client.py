import os
from socketIO_client import SocketIO, LoggingNamespace

io = SocketIO(os.getenv("HOST_API_SOCKETIO"), os.getenv("PORT_API_SOCKETIO"), LoggingNamespace)