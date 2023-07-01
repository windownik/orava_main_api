import datetime
import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import Message
from lib.response_examples import *
from lib.routes.push.push import send_push_notification
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@data_b.on_init
async def initialization(connect):
    # you can run your db initialization code here
    await connect.execute("SELECT 1")


# Create new msg
@app.post(path='/message', tags=['Message'], responses=new_msg_created_res)
async def create_new_messages(access_token: str, to_user_id: int, title: str, text: str, description: str,
                              user_type: str = 'user', lang: str = 'en',
                              msg_type: str = 'text', msg_id: int = 0, push: bool = False,
                              db=Depends(data_b.connection)):
    """
    Use this route for creating new message\n\n

    description: short text\n
    text: main text of message\n
    title: title of message\n
    msg_id: id of new document or another main document. Send 0 if only text message\n
    access_token: user's access token in our service\n
    to_user_id: user_id for personal msg sending for all users send value 0\n
    user_type: can be 'user', 'admin', 'all'\n
    push: Send True for sending push notification\n
    lang: Can be 'en', 'ru', 'he'\n
    msg_type: Can be 'text', 'img', 'new_user', 'new_order'\n
    _____________\n
    'text' - Просто текстовое сообщение отправляемое от одного пользователя другому или в рассылке\n
    'img' - Просто графическое сообщение отправляемое от одного пользователя другому или в рассылке\n
    'new_user' - Автоматически созданное сообщение при регистрации нового пользователя msg_id в таком сообщении
    равен user_id нового пользователя, to_id равен 0, user_type - admin\n
    'new_order' - Автоматически созданное сообщение при создании нового заказа msg_id в таком сообщении
    равен order_id нового заказа, to_id равен 0, user_type - admin\n
    'new_order_admin_comment' - Комментарий отправленный админом пользователю при модерации ордера\n
    """
    from_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not from_id:
        return JSONResponse(content={"ok": False, "desc": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, name='status', table='all_users', id_name='user_id',
                                     id_data=to_user_id)
    if not user_data and to_user_id != 0:
        return JSONResponse(content={"ok": False, "desc": "Bad to_user_id"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    if user_type not in ('user', 'admin', 'all'):
        return JSONResponse(content={"ok": False, "desc": "Bad user_type"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    if lang not in ('en', 'ru', 'he'):
        return JSONResponse(content={"ok": False, "desc": "Bad lang"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    msg_id = await conn.create_msg(msg_id=msg_id, msg_type=msg_type, title=title, text=text, description=description,
                                   lang=lang, from_id=from_id[0][0], to_id=to_user_id, user_type=user_type, db=db)
    if msg_id is None:
        return JSONResponse(content={"ok": False, "desc": "I can't create this message"},
                            status_code=_status.HTTP_400_BAD_REQUEST)
    if push:
        await send_push_notification(access_token=access_token, user_id=to_user_id, title=title, push_body=text,
                                     push_type='text_msg', msg_id=msg_id[0][0], db=db)

    return JSONResponse(content={"ok": True, 'desc': 'New message was created successfully.'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


# Admin get all messages
@app.get(path='/admin_get_msg', tags=['Message'], responses=get_me_res)
async def admin_get_all_messages(access_token: str, offset: int = 0, limit: int = 0, db=Depends(data_b.connection)):
    """Here you can get new message list. It's command only for admins.\n
    access_token: This is access auth token. You can get it when create account or login"""
    user_id = await conn.get_token_admin(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    msg_data = await conn.read_all_msg(db=db, user_id=user_id[0][0], offset=offset,
                                       limit=limit)
    count = await conn.count_admin_msg(db=db, user_id=user_id[0][0])
    msg_list = []

    for _msg_data in msg_data:
        msg = Message(data=_msg_data)
        msg_list.append(
            msg.get_msg_json()
        )
    return JSONResponse(content={"ok": True,
                                 'count': count[0][0],
                                 'msg_list': msg_list},

                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


# User get all app jobs
@app.get(path='/app_jobs', tags=['Message'], responses=get_me_res)
async def user_get_orders_app_jobs(access_token: str, order_id: int, db=Depends(data_b.connection)):
    """Here you can get new message list. It's command only for admins.\n
    access_token: This is access auth token. You can get it when create account or login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    msg_data = await conn.read_job_app_msg(db=db, order_id=order_id)
    msg_list = []

    for _msg_data in msg_data:
        user_data = await conn.read_data(db=db, table='all_users', id_name="user_id", id_data=_msg_data['from_id'])
        msg = Message(data=_msg_data, user_from=user_data[0])
        msg_list.append(
            msg.get_msg_json()
        )
    return JSONResponse(content={"ok": True,
                                 'count': len(msg_data),
                                 'msg_list': msg_list,
                                 },

                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


# Admin get all messages
@app.get(path='/user_get_msg', tags=['Message'], responses=get_me_res)
async def user_get_all_messages(access_token: str, offset: int = 0, limit: int = 0, db=Depends(data_b.connection)):
    """Here user can get new message list.\n
    access_token: This is access auth token. You can get it when create account or login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    msg_data = await conn.read_all_msg_user(db=db, user_id=user_id[0][0], offset=offset, limit=limit)
    count = await conn.count_users_msg(db=db, user_id=user_id[0][0])
    msg_list = []

    for _msg_data in msg_data:
        msg = Message(data=_msg_data)
        msg_list.append(
            msg.get_msg_json()
        )
    return JSONResponse(content={"ok": True,
                                 'count': count[0][0],
                                 'msg_list': msg_list},

                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/message', tags=['Message'], responses=get_msg_by_id_res)
async def get_messages_by_id(access_token: str, msg_id: int, db=Depends(data_b.connection)):
    """Here you can get message by message id.\n
    access_token: This is access auth token. You can get it when create account or login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    msg_data = await conn.read_data(db=db, table='message_line', id_name='id', id_data=msg_id)
    if not msg_data:
        return JSONResponse(content={"ok": True,
                                     'message': 'No msg in database'},
                            status_code=_status.HTTP_400_BAD_REQUEST)
    user_id = user_id[0][0]
    user_status = await conn.read_data(db=db, table='all_users', id_name='user_id', name='status', id_data=user_id)

    user_from = await conn.read_data(db=db, table='all_users', id_name='user_id',
                                     id_data=msg_data[0]['from_id'])
    user_to = await conn.read_data(db=db, table='all_users', id_name='user_id',
                                   id_data=msg_data[0]['to_id'])

    if (msg_data[0]['to_id'] == user_id or msg_data[0]['from_id'] == user_id) or (msg_data[0]['user_type'] == 'all') \
            or user_status[0][0] == 'admin':
        pass
    else:
        return JSONResponse(content={"ok": True,
                                     'message': "You haven't rights"},
                            status_code=_status.HTTP_400_BAD_REQUEST)
    msg = Message(
        data=msg_data[0],
        user_from=user_from[0] if user_from else None,
        user_to=user_to[0] if user_to else None)

    return JSONResponse(content={"ok": True,
                                 'message': msg.get_msg_json()},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.put(path='/message', tags=['Message'], responses=get_msg_by_id_res)
async def read_message(access_token: str, msg_id: int, db=Depends(data_b.connection)):
    """Use it if user open message and read.\n
    access_token: This is access auth token. You can get it when create account or login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    user_id = user_id[0][0]

    msg_data = await conn.read_data(db=db, table='message_line', id_name='id', id_data=msg_id)
    if not msg_data:
        return JSONResponse(content={"ok": True,
                                     'message': 'No msg in database'},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    if user_id != msg_data[0]['to_id']:
        user_id = await conn.get_token_admin(db=db, token_type='access', token=access_token)
        if not user_id:
            return JSONResponse(content={"ok": True,
                                         'message': "You haven't rights"},
                                status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.update_data(table='message_line', id_name='id', name='read_date', data=datetime.datetime.now(),
                           id_data=msg_id, db=db)
    await conn.update_data(table='message_line', id_name='id', name='status', data='read', id_data=msg_id, db=db)

    return JSONResponse(content={"ok": True,
                                 'desc': 'Status and read inform of msg was updated'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.delete(path='/message', tags=['Message'], responses=get_msg_by_id_res)
async def read_message(access_token: str, msg_id: int, db=Depends(data_b.connection)):
    """Use it if user open want to delete msg.\n
    access_token: This is access auth token. You can get it when create account or login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    user_id = user_id[0][0]

    msg_data = await conn.read_data(db=db, table='message_line', id_name='id', id_data=msg_id)
    if not msg_data:
        return JSONResponse(content={"ok": True,
                                     'message': 'No msg in database'},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    if user_id != msg_data[0]['to_id']:
        admin = await conn.get_token_admin(db=db, token_type='access', token=access_token)
        if not admin or msg_data[0]['to_id'] != 0:
            return JSONResponse(content={"ok": True,
                                         'message': "You haven't rights"},
                                status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.update_data(table='message_line', id_name='id', name='deleted_date', data=datetime.datetime.now(),
                           id_data=msg_id, db=db)
    await conn.update_data(table='message_line', id_name='id', name='status', data='delete', id_data=msg_id, db=db)

    return JSONResponse(content={"ok": True,
                                 'desc': 'Status and read inform of msg was updated'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})