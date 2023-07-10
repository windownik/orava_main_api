import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import Dialog, User
from lib.response_examples import *
from lib.routes.chat.dialog_funcs import check_dialog_in_db
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.get(path='/user_by_phone', tags=['Chat'], responses=dialog_created_res)
async def user_by_phone(access_token: str, phone: int, db=Depends(data_b.connection)):
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    user_data = await conn.read_data(db=db, table='all_users', id_name='phone', id_data=phone)
    if not user_data:
        return JSONResponse(status_code=_status.HTTP_200_OK,
                            content={"ok": False,
                                     "description": "no user with this phone"})
    else:
        user = User.parse_obj(user_data[0])
        return JSONResponse(status_code=_status.HTTP_200_OK,
                            content={"ok": True,
                                     "user": user.dict()},
                            headers={'content-type': 'application/json; charset=utf-8'})


@app.post(path='/dialog', tags=['Chat'], responses=dialog_created_res)
async def new_dialog(access_token: str, to_id: int, db=Depends(data_b.connection)):
    """Create new dialog with user with to_id.
    access_token: This is access auth token. You can get it when create account or login\n
    to_id: Second user in dialog"""

    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id', id_data=to_id)
    if not user_data:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': "Haven't user with to_id", })

    dialog = await check_dialog_in_db(from_id=owner_id[0][0], to_id=user_data[0][0], db=db)
    if dialog is None:
        chat_id = await conn.create_in_all_chats(db=db, owner_id=owner_id[0][0])
        await conn.create_msg_line_table(db=db, chat_id=chat_id[0][0])
        dialog_data = await conn.create_dialog(owner_id=owner_id[0][0], to_id=user_data[0][0], db=db,
                                               msg_chat_id=chat_id[0][0])
        dialog = Dialog.parse_obj(dialog_data[0])
        await conn.update_data(table='dialog', name='owner_status', data='active', db=db, id_name='msg_chat_id',
                               id_data=dialog.msg_chat_id)
    else:
        if dialog.owner_id == owner_id[0][0]:
            await conn.update_data(table='dialog', name='owner_status', data='active', db=db, id_name='msg_chat_id',
                                   id_data=dialog.msg_chat_id)
        else:
            await conn.update_data(table='dialog', name='to_status', data='active', db=db, id_name='msg_chat_id',
                                   id_data=dialog.msg_chat_id)
    return JSONResponse(status_code=_status.HTTP_200_OK,
                        content={"ok": True,
                                 "dialog": await dialog.to_json(db=db, user_id=owner_id[0][0])
                                 },
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.delete(path='/dialog', tags=['Chat'], responses=dialog_created_res)
async def delete_dialog(access_token: str, msg_chat_id: int, db=Depends(data_b.connection)):
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    dialog_data = await conn.read_data(table='dialog', id_name='msg_chat_id', id_data=msg_chat_id, db=db)
    if not dialog_data:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': "Haven't dialog with msg_chat_id", })
    if dialog_data[0]['owner_id'] == owner_id[0][0]:
        await conn.update_data(table='dialog', name='owner_status', data='delete', db=db, id_name='msg_chat_id',
                               id_data=msg_chat_id)
    elif dialog_data[0]['to_id'] == owner_id[0][0]:
        await conn.update_data(table='dialog', name='to_status', data='delete', db=db, id_name='msg_chat_id',
                               id_data=msg_chat_id)
    else:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': "not enough rights", })

    await conn.delete_from_table(db=db, table=f'messages_{msg_chat_id}')
    return JSONResponse(status_code=_status.HTTP_200_OK,
                        content={"ok": True,
                                 "description": 'dialog and all messages was deleted'
                                 })
