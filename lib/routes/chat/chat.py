import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User, Message, add_user_and_reply_to_msg, Chat
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.post(path='/chat', tags=['Chat'], responses=create_chat_res)
async def create_new_chat(access_token: str, chat_type: str = 'dialog', owner_id: int = 0, name: str = '0',
                          community_id: int = 0, image_link: str = '0',
                          image_link_little: str = '0', db=Depends(data_b.connection)):
    """Create new chat in server.
    name: you can add name only for chat type\n
    midl_name:  users midl name\n
    surname: users midl surname\n
    phone: example 375294322114\n
    image_link: get from facebook API\n
    chat_type: status can be: dialog, chat"""

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)
    if owner_id == 0:
        owner_id = user_id[0][0]

    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id', id_data=owner_id)
    user = User.parse_obj(user_data[0])
    if chat_type != 'dialog' and chat_type != 'chat' and chat_type != 'community_main_chat':
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': 'Bad status', })

    chat_data = await conn.create_chat(db=db, owner_id=owner_id, name=name, img_url=image_link, chat_type=chat_type,
                                       little_img_url=image_link_little, community_id=community_id)
    chat: Chat = Chat.parse_obj(chat_data[0])

    return JSONResponse(content={"ok": True,
                                 'chat': await chat.to_json(reqwest_user=user, db=db)},
                        status_code=_status.HTTP_200_OK,

                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/chat_msg', tags=['Chat'], responses=get_me_res)
async def get_chat_msg_by_scroll(access_token: str, chat_id: int, lust_msg_id: int, old_msg_scroll: bool,
                                 db=Depends(data_b.connection), ):
    """Here you can check your username and password. Get users information.\n
    access_token: This is access auth token. You can get it when create account, login"""
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)
    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id', id_data=owner_id[0][0])
    user = User.parse_obj(user_data[0])

    msg_data = await conn.get_chat_messages_by_last_msg(db=db, chat_id=chat_id, old_msg_scroll=old_msg_scroll,
                                                        lust_msg_id=lust_msg_id)
    messages = []
    for one in msg_data:
        msg: Message = Message.parse_obj(one)
        msg_dict = await add_user_and_reply_to_msg(db=db, msg=msg, reqwest_user=user)
        messages.append(msg_dict)

    return JSONResponse(content={"ok": True,
                                 'messages': messages
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})
