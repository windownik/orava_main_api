import os

from fastapi import Depends
import starlette.status as _status
from lib import sql_connect as conn
from starlette.responses import Response, JSONResponse

from lib.response_examples import *
from lib.routes.push.push_func import send_push
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@data_b.on_init
async def initialization(connect):
    # you can run your db initialization code here
    await connect.execute("SELECT 1")


@app.get(path='/send_push', tags=['Push'], responses=send_push_res)
async def send_push_notification(access_token: str, user_id: int, title: str, push_body: str, push_type: str,
                                 data: str = '0', msg_id: int = 0, db=Depends(data_b.connection)):
    """
    Send push notifications
    user_id - id of user for sending push\n
    title - Title of push\n
    push_body - Text body of push message\n
    data - This is simple str with main data.\n
    push_type - can be: 'text_msg', 'connect_community' and other,
    """
    owner_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not owner_id:
        return Response(content="not enough rights", status_code=_status.HTTP_401_UNAUTHORIZED)

    push_token = await conn.read_data(db=db, table='all_users', name='push', id_name='user_id', id_data=user_id)
    if not push_token:
        return Response(content="no user in database", status_code=_status.HTTP_400_BAD_REQUEST)
    send_push(fcm_token=push_token[0][0], title=title, body=push_body, data=data, push_type=push_type,
              msg_id=msg_id)
    return JSONResponse(content={'ok': True, 'desc': 'successful send push'},
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.put(path='/update_push', tags=['Push'], responses=update_push_res)
async def user_update_push_token(access_token: str, push_token: str, db=Depends(data_b.connection)):
    """Update users push token in database"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="not enough rights", status_code=_status.HTTP_401_UNAUTHORIZED)

    user_id = user_id[0][0]
    await conn.update_data(db=db, table='all_users', name='push', data=push_token, id_name='user_id', id_data=user_id)

    return JSONResponse(content={'ok': True, 'desc': 'successfully updated'},
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.post(path='/sending_push', tags=['Push'], responses=update_push_res)
async def start_sending_push_msg(access_token: str, lang: str, content_type: int, users_account_type: str,
                                 title: str, short_text: str, main_text: str = None, url: str = None,
                                 db=Depends(data_b.connection)):
    """
    Use it route for create massive sending message for users with filter\n\n
    access_token: users token\n
    lang: users language filter can be: ru, en, he, all\n
    content_type: can be: 0 for text and 1 for img\n
    users_account_type: can be: worker, customer, all\n
    title: Tittle of message\n
    short_text: short text of push message\n
    main_text: main text of message for content type 0\n
    url: url to img in internet for content type 0\n
    """

    if lang not in ('ru', 'en', 'he', 'he', 'all'):
        return JSONResponse(content={"ok": False,
                                     'description': "Bad language"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    if content_type not in (0, 1):
        return JSONResponse(content={"ok": False,
                                     'description': "Content type not valid"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    if users_account_type not in ('worker', 'customer', 'all'):
        return JSONResponse(content={"ok": False,
                                     'description': "Bad users account type"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    admin_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not admin_id:
        return JSONResponse(content={"ok": False,
                                     'description': "bad access token or not enough rights"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    users_id = await conn.get_users_for_push(db=db, lang=lang, users_account_type=users_account_type)
    if content_type == 0:
        push_type = 'text'
    else:
        push_type = 'img'

    description = '0'
    if main_text is not None:
        description = main_text
    elif url is not None:
        description = url

    for user in users_id:
        msg_id = await conn.msg_to_user(db=db, user_id=user[0], title=title, short_text=short_text,
                                        description=description, from_id=1, msg_type=push_type)

        await conn.save_push_to_sending(db=db, user_id=user[0], title=title, short_text=short_text,
                                        main_text=main_text if main_text is not None else '0',
                                        push_type=push_type, msg_id=msg_id[0][0],
                                        img_url=url if url is not None else '0')

    return JSONResponse(content={'ok': True, 'desc': 'successfully created'},
                        headers={'content-type': 'application/json; charset=utf-8'})
