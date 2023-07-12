from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import socketio

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=["Origin, X-Requested-With, Content-Type, Accept"],
)

# sio = socketio.AsyncServer(
#     async_mode='asgi',
#     cors_allowed_origins='*'
# )
# fast_app = socketio.ASGIApp(
#     socketio_server=sio,
#     other_asgi_app=app,
#     socketio_path='/api/notifications/socket.io/'
# )