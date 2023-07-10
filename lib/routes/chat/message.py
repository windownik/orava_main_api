import datetime
from typing import List
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from lib.app_init import app

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
            var ws = new WebSocket("ws://45.82.68.203:8000/ws");
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
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
        print(len(self.connections))

    async def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_json(data)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    print('connect')
    print(len(manager.connections))
    try:

        while True:
            data = await websocket.receive_text()
            print('message')
            now = datetime.datetime.now()
            await manager.broadcast(data)
            await manager.connections[0].send_json(str(datetime.datetime.now() - now))

    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except:
        pass