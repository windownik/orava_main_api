import datetime
import os
import time

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@data_b.on_init
async def initialization(connect):
    # you can run your db initialization code here
    await connect.execute("SELECT 1")


@app.post(path='/user', tags=['User'], responses=create_user_res)
async def new_user(name: str, surname: str, phone: int, lang: str, image_link: str,
                   image_link_little: str, midl_name: str = '0', db=Depends(data_b.connection)):
    """Create new user in server.
    name: users name\n
    midl_name:  users midl name\n
    surname: users midl surname\n
    phone: example 375294322114\n
    image_link: get from facebook API\n
    lang: users app Language can be: ru, en"""

    if lang != 'ru' and lang != 'en':
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={"ok": False,
                                     'description': 'Bad pick language', })
    now = datetime.datetime.now()
    user_data = {
        'user_id': 0,
        'name': name,
        'phone': phone,
        'middle_name': midl_name,
        'surname': surname,
        'image_link': image_link,
        'image_link_little': image_link_little,
        'lang': lang,
        'push': '0',
        'description': '0',
        'email': '0',
        'status': '0',
        'last_active': int(time.mktime(now.timetuple())),
        'create_date': int(time.mktime(now.timetuple()))
    }

    user = User.parse_obj(user_data)
    data = await conn.create_user(db=db, user=user)
    user = User.parse_obj(data[0])

    access = await conn.create_token(db=db, user_id=user.user_id, token_type='access')
    refresh = await conn.create_token(db=db, user_id=user.user_id, token_type='refresh')

    return JSONResponse(content={"ok": True,
                                 'access_token': access[0][0],
                                 'refresh_token': refresh[0][0],
                                 'user': user.dict()},
                        status_code=_status.HTTP_200_OK,

                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/user', tags=['User'], responses=get_me_res)
async def get_user_information(access_token: str, db=Depends(data_b.connection), user_id: int = 0):
    """Here you can check your username and password. Get users information.\n
    access_token: This is access auth token. You can get it when create account, login"""
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    if user_id != 0:
        user_data = await conn.read_data(db=db, name='*', table='all_users',
                                         id_name='user_id', id_data=user_id)
    else:
        user_data = await conn.read_data(db=db, name='*', table='all_users',
                                         id_name='user_id', id_data=owner_id[0][0])
    if not user_data:
        return Response(content="no user in database",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    user = User.parse_obj(user_data[0])
    return JSONResponse(content={"ok": True,
                                 'user': user.dict(),
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.put(path='/user', tags=['User'], responses=update_user_res)
async def update_user_information(access_token: str, name: str = '0', surname: str = '0', midl_name: str = '0',
                                  lang: str = '0', image_link: str = '0', image_link_little: str = '0',
                                  db=Depends(data_b.connection)):
    """Update user's information.\n

    name: users name from Facebook or name of company\n
    phone: only numbers\n
    description: users account description\n
    status: can be customer and worker\n
    lang: users app Language can be: ru, en, heb\n"""

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False,
                                     'description': "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    await conn.update_user(db=db, name=name, surname=surname, midl_name=midl_name, image_link=image_link, lang=lang,
                           user_id=user_id[0][0], image_link_little=image_link_little)
    return JSONResponse(content={"ok": True,
                                 'desc': 'all users information updated'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/user_by_phone', tags=['User'], responses=dialog_created_res)
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


@app.delete(path='/user', tags=['User'], responses=update_user_res)
async def delete_user(access_token: str, db=Depends(data_b.connection)):
    """Delete all user information.\n

    access_token: This is access auth token. You can get it when create account, login"""

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False,
                                     'description': "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    await conn.update_data(db=db, table='all_users', name='status', data='delete', id_name='user_id',
                           id_data=user_id[0][0])
    await conn.delete_all_tokens(db=db, user_id=user_id[0][0])
    return JSONResponse(content={"ok": True,
                                 'desc': 'all users information updated'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})
