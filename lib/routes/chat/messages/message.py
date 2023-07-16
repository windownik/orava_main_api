import json

from starlette.websockets import WebSocketDisconnect
from fastapi import WebSocket, Depends
from fastapi.responses import HTMLResponse

from lib.app_init import app
from lib.routes.chat.messages.check_message import msg_manager
from lib.routes.chat.messages.connection_manager import manager
from lib.sql_connect import data_b

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
            var ws = new WebSocket("ws://45.82.68.203:10020/ws/1");
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


@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, db=Depends(data_b.connection)):
    await manager.connect(websocket, user_id=user_id)
    print('Connect', manager.connections.keys())
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            if 'echo' in data.keys():
                await websocket.send_text(str(data))
                continue
            check = await msg_manager(data, db=db, user_id=user_id, websocket=websocket, manager=manager)

            if not check:
                continue
    except WebSocketDisconnect:
        await manager.disconnect(user_id=user_id)
    except Exception as ex:
        print('Exception', ex)
    finally:
        print('finally')
        await manager.disconnect(user_id)
