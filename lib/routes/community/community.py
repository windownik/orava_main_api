import os
import random
import string

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User, Chat, Community
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.post(path='/community', tags=['Community'], responses=create_user_res)
async def create_new_community(access_token: str, com_name: str, chat_name: str, open_profile: bool = True,
                               send_media: bool = True, moder_create_chat: bool = True, send_voice: bool = True,
                               db=Depends(data_b.connection)):
    """Create community in server.
    com_name: it is community name\n
    chat_name:  this is name of main chat\n
    open_profile: can users open other users profiles\n
    send_media: can users send media\n
    moder_create_chat: Moder can create chats\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id', id_data=user_id[0][0])
    user = User.parse_obj(user_data[0])

    chat_data = await conn.create_chat(db=db, owner_id=user_id[0][0], name=chat_name, chat_type='main_chat')
    chat: Chat = Chat.parse_obj(chat_data[0])

    com_data = await conn.create_community(db=db, owner_id=user_id[0][0], name=com_name, main_chat_id=chat.chat_id,
                                           join_code=await create_code(db), moder_create_chat=moder_create_chat,
                                           open_profile=open_profile, send_media=send_media, send_voice=send_voice)
    community: Community = Community.parse_obj(com_data[0])

    await conn.update_data(db=db, table='all_chats', name='community_id', data=community.community_id,
                           id_name='chat_id', id_data=chat.chat_id)
    await conn.save_user_to_chat(db=db, chat_id=chat.chat_id, user_id=user.user_id)

    return JSONResponse(content={"ok": True,
                                 'main_chat': await chat.to_json(db=db, reqwest_user=user),
                                 'community': community.dict()},
                        status_code=_status.HTTP_200_OK,

                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/community', tags=['Community'], responses=get_me_res)
async def get_community_by_id(access_token: str, community_id: int, db=Depends(data_b.connection), ):
    """Here you can get community by id\n
    access_token: This is access auth token. You can get it when create account, login"""
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    user_data = await conn.read_data(db=db, table='all_users', id_name='user_id', id_data=owner_id[0][0])
    user = User.parse_obj(user_data[0])
    com_data = await conn.read_data(db=db, table='community', id_name='community_id', id_data=community_id)
    if not com_data:
        return Response(content="bad community_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)
    community: Community = Community.parse_obj(com_data[0])
    chat_data = await conn.read_data(db=db, table='all_chats', id_name='chat_id', id_data=community.main_chat_id)
    chat: Chat = Chat.parse_obj(chat_data[0])

    res = {"ok": True,
           'main_chat': await chat.to_json(db=db, reqwest_user=user),
           'community': community.dict()
           }
    return JSONResponse(content=res,
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.put(path='/community', tags=['Community'], responses=create_user_res)
async def create_new_community(access_token: str, community_id: int, chat_name: str, com_name: str,
                               open_profile: bool = True, send_media: bool = True, moder_create_chat: bool = True,
                               send_voice: bool = True, db=Depends(data_b.connection)):
    """Create community in server.
    com_name: it is community name\n
    chat_name:  this is name of main chat\n
    open_profile: can users open other users profiles\n
    send_media: can users send media\n
    moder_create_chat: Moder can create chats\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, table='all_users', id_name='user_id', id_data=user_id[0][0])
    user = User.parse_obj(user_data[0])
    com_data = await conn.read_data(db=db, table='community', id_name='community_id', id_data=community_id)
    if not com_data:
        return Response(content="bad community_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.update_community(db=db, name=com_name, moder_create_chat=moder_create_chat, open_profile=open_profile,
                                send_media=send_media, send_voice=send_voice, community_id=community_id)

    com_data = await conn.read_data(db=db, table='community', id_name='community_id', id_data=community_id)
    community: Community = Community.parse_obj(com_data[0])

    await conn.update_data(db=db, table='all_chats', name='name', data=chat_name,
                           id_name='chat_id', id_data=community.main_chat_id)

    chat_data = await conn.read_data(db=db, table='all_chats', id_name='chat_id', id_data=community.main_chat_id)
    chat: Chat = Chat.parse_obj(chat_data[0])

    return JSONResponse(content={"ok": True,
                                 'main_chat': await chat.to_json(db=db, reqwest_user=user),
                                 'community': community.dict()},
                        status_code=_status.HTTP_200_OK,

                        headers={'content-type': 'application/json; charset=utf-8'})


async def create_code(db: Depends):
    """Create and check in db random string code"""
    while True:
        letters = string.ascii_lowercase + '1234567890'
        rand_string = ''.join(random.choice(letters) for _ in range(6))
        res = await conn.read_data(db=db, table='community', id_name='join_code', id_data=rand_string)
        if not res:
            return rand_string
