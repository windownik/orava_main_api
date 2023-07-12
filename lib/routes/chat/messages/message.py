import json

from fastapi import WebSocket, Depends
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from lib.app_init import app
from lib.db_objects import ReceiveMessage
from lib.routes.chat.messages.check_message import check_message, save_msg_in_dialog
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
    print('Connect')
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            check = await check_message(data, db=db, user_id=user_id)
            if not check:
                continue
            if check == 'bad access':
                await websocket.send_json({
                    "ok": False,
                    'status_code': 401,
                    'desc': 'bad access',
                    "msg_chat_id": data["msg_chat_id"],
                    "to_id": data["to_id"],
                    "chat_id": data["to_id"],
                })
                continue

            msg = ReceiveMessage.model_validate(data)
            print(msg.print_msg())

            if data['msg_type'] == 'dialog':
                msg_id = await save_msg_in_dialog(data, db=db)
            else:
                continue

            await websocket.send_json({
                "ok": True,
                'status_code': 200,
                'desc': 'save and send to user',
                "msg_chat_id": data["msg_chat_id"],
                "to_id": data["to_id"],
                "chat_id": data["to_id"],
                "new_msg_id": msg_id
            })

    except Exception as ex:
        print(ex)
