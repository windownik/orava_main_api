import datetime
import os
import time

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User
from lib.response_examples import *
from lib.routes.chat.dialog_funcs import check_dialog_in_db
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.post(path='/dialog', tags=['Chat'], responses=create_dialog_res)
async def new_dialog(access_token: str, to_id: int, db=Depends(data_b.connection)):
    """Create new dialog with user with to_id. This is default chat for 2 persons.\n
    access_token: This is access auth token. You can get it when create account or login\n
    to_id: Second user in dialog"""

    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id', id_data=to_id)
    if not user_data:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': "Haven't user with to_id", })
    user: User = User.parse_obj(user_data[0])
    dialog = await check_dialog_in_db(from_id=owner_id[0][0], to_id=user_data[0][0], db=db)
    return JSONResponse(status_code=_status.HTTP_200_OK,
                        content={"ok": True,
                                 "dialog": await dialog.to_json(db=db, reqwest_user=user)
                                 },
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.delete(path='/chat', tags=['Chat'], responses=delete_dialog_res)
async def delete_chat(access_token: str, chat_id: int, db=Depends(data_b.connection)):
    """
    Here owner can delete chat with all messages\n
    chat_id: this is id of chat, get it when create chat\n
    access_token: This is access auth token. You can get it when create account or login\n
    """
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return JSONResponse(content={"ok": False,
                                     'description': "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    chat_data = await conn.read_data(table='all_chats', id_name='chat_id', id_data=chat_id, db=db)
    if not chat_data:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': "Haven't chat with chat_id", })
    if owner_id[0][0] != chat_data[0]['owner_id']:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': "not enough rights", })

    await conn.update_data(table='all_chats', name='status', data='delete', db=db, id_name='chat_id',
                           id_data=chat_data[0][0])
    now = datetime.datetime.now()
    await conn.update_data(table='all_chats', name='deleted_date', data=int(time.mktime(now.timetuple())), db=db,
                           id_name='chat_id',
                           id_data=chat_data[0][0])

    await conn.delete_all_messages(db=db, chat_id=chat_data[0][0])
    return JSONResponse(status_code=_status.HTTP_200_OK,
                        content={"ok": True,
                                 "description": 'dialog and all messages was deleted'
                                 })
