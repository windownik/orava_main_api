import datetime
import os
import random
import time

import starlette.status as _status
from fastapi import Depends
from starlette.responses import JSONResponse

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


@app.get(path='/access_token', tags=['Auth'], responses=access_token_res)
async def create_new_access_token(refresh_token: str, db=Depends(data_b.connection), ):
    """refresh_token: This is refresh token, use it for create new access token.
    You can get it when create account or login."""
    user_id = await conn.get_token(db=db, token_type='refresh', token=refresh_token)
    if not user_id:
        return JSONResponse(content={"ok": False,
                                     'description': "bad refresh token, please login"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)
    await conn.delete_old_tokens(db=db)
    now = datetime.datetime.now()
    less_3 = now - datetime.timedelta(days=3)
    if user_id[0][1] < int(time.mktime(less_3.timetuple())):
        refresh = await conn.create_token(db=db, user_id=user_id[0][0], token_type='refresh')
        refresh_token = refresh[0][0]
    access = await conn.create_token(db=db, user_id=user_id[0][0], token_type='access')
    await conn.update_user_active(db=db, user_id=user_id[0][0])
    return {"ok": True,
            'user_id': user_id[0][0],
            'access_token': access[0][0],
            'refresh_token': refresh_token}


@app.get(path='/login', tags=['Auth'], responses=login_get_res)
async def login_user(phone: int, db=Depends(data_b.connection)):
    """Login user in service by phone number"""
    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='phone', id_data=phone)
    if not user_data:
        return JSONResponse(content={"ok": True,
                                     'description': 'This email is not in database', },
                            status_code=_status.HTTP_200_OK,
                            headers={'content-type': 'application/json; charset=utf-8'})

    user = User.parse_obj(user_data[0])

    access = await conn.create_token(db=db, user_id=user.user_id, token_type='access')
    refresh = await conn.create_token(db=db, user_id=user.user_id, token_type='refresh')

    return JSONResponse(content={"ok": True,
                                 'user': user.dict(),
                                 'access_token': access[0][0],
                                 'refresh_token': refresh[0][0]
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/check_email', tags=['Auth'], responses=get_me_res)
async def check_email(email: str, db=Depends(data_b.connection), ):
    """Here you can check your email.
    email: string email for check it in db"""

    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='email', id_data=email)
    if not user_data:
        return JSONResponse(content={"ok": True,
                                     'description': 'This email is not in database', },
                            status_code=_status.HTTP_200_OK,
                            headers={'content-type': 'application/json; charset=utf-8'})
    return JSONResponse(content={"ok": False,
                                 'description': 'This email is in database', },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/check_phone', tags=['Auth'], responses=get_me_res)
async def check_email(phone: int, db=Depends(data_b.connection), ):
    """Here you can check your phone.
    phone: int phone for check it in db"""

    user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='phone', id_data=phone)
    if not user_data:
        return JSONResponse(content={"ok": True,
                                     'description': 'This phone is not in database', },
                            status_code=_status.HTTP_200_OK,
                            headers={'content-type': 'application/json; charset=utf-8'})
    return JSONResponse(content={"ok": False,
                                 'description': 'This phone is in database', },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/sms_to_phone', tags=['Auth'], responses=get_me_res)
async def check_email(phone: int, db=Depends(data_b.connection), ):
    """Here you can check your phone by sms.
    phone: int phone for check"""

    code = random.randrange(1000, 9999)
    await conn.save_new_sms_code(db=db, phone=phone, code="1111")
    return JSONResponse(content={"ok": True,
                                 'description': 'This phone is not in database', },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})
