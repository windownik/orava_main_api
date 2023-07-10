import datetime
from typing import Dict
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from lib.app_init import app

'127.0.0.1:8000'
"45.82.68.203:10020"

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8000/ws/1");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/ws_chat")
async def get():
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self):
        self.connections: Dict = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.connections[user_id] = websocket
        print(len(self.connections))

    async def disconnect(self, user_id: int):
        self.connections.pop(user_id)

    async def broadcast(self, data: str, user_id: int):
        for key in self.connections.keys():
            if user_id == key:
                continue
            await self.connections[key].send_json(data)


manager = ConnectionManager()


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id=user_id)
    try:
        while True:
            data = await websocket.receive_text()
            print('qdfwedf')
            # if 'user_id' not in data:
            #     await websocket.send_json({'desc': 'No user_id in message'})
            #     continue
            now = datetime.datetime.now()
            await manager.broadcast(data, user_id=user_id)
            await manager.connections[user_id].send_json(str(datetime.datetime.now() - now))

    except Exception as ex:
        print(ex)
