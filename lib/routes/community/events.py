import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User, Community, Event
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.post(path='/event', tags=['Event'], responses=create_event_res)
async def create_new_event(access_token: str, community_id: int, title: str, text: str, repeat_days: int = 0,
                           death_date: int = 0, event_type: str = 'event', start_time: int = 0, end_time: int = 0,
                           db=Depends(data_b.connection)):
    """Create event in community.\n
    community_id: it is community id\n
    title: it is community name\n
    text:  main text of event\n
    event_type: type of event can be event or announcement\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    user_data = await conn.read_data(db=db, table='all_users', id_name='user_id', id_data=user_id[0][0])
    user = User.parse_obj(user_data[0])
    com_data = await conn.read_data(db=db, table='community', id_name='community_id', id_data=community_id)
    if not com_data:
        return Response(content="bad community_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)
    community: Community = Community.parse_obj(com_data[0])
    if community.owner_id != user.user_id:
        return JSONResponse(content={"ok": False,
                                     'description': 'Not enough rights'},
                            status_code=_status.HTTP_400_BAD_REQUEST, )

    if event_type not in ('event', 'announcement'):
        return JSONResponse(content={"ok": False,
                                     'description': 'Bad event_type'},
                            status_code=_status.HTTP_400_BAD_REQUEST, )

    event_data = await conn.create_event(db=db, community_id=community.community_id, creator_id=user.user_id,
                                         title=title, text=text, death_date=death_date, repeat_days=repeat_days,
                                         event_type=event_type, end_time=end_time, start_time=start_time)
    event: Event = Event.parse_obj(event_data[0])
    return JSONResponse(content={"ok": True,
                                 'event': event.dict()},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.put(path='/event', tags=['Event'], responses=create_event_res)
async def update_event(access_token: str, event_id: int, title: str, text: str, repeat_days: int = 0,
                       death_date: int = 0, event_type: str = 'event', start_time: int = 0, end_time: int = 0,
                       db=Depends(data_b.connection)):
    """Create event in community.\n
    community_id: it is community id\n
    title: it is community name\n
    text:  main text of event\n
    event_type: type of event can be event or announcement\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
    if not event_data:
        return Response(content="bad event_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    if event_type not in ('event', 'announcement'):
        return JSONResponse(content={"ok": False,
                                     'description': 'Bad event_type'},
                            status_code=_status.HTTP_400_BAD_REQUEST, )

    await conn.update_event(db=db, event_id=event_id, title=title, text=text, death_date=death_date,
                            repeat_days=repeat_days, event_type=event_type, end_time=end_time, start_time=start_time)

    event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
    event: Event = Event.parse_obj(event_data[0])
    return JSONResponse(content={"ok": True,
                                 'event': event.dict()},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/event', tags=['Event'], responses=create_event_res)
async def get_event_by_id(access_token: str, event_id: int, db=Depends(data_b.connection), ):
    """Here you can get community by id\n
    access_token: This is access auth token. You can get it when create account, login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
    if not event_data:
        return JSONResponse(content={"ok": False, 'description': "bad event_id"},
                            status_code=_status.HTTP_400_BAD_REQUEST)
    event: Event = Event.parse_obj(event_data[0])

    return JSONResponse(content={"ok": True,
                                 'event': event.dict()},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/all_events', tags=['Event'], responses=create_event_res)
async def get_event_by_id(access_token: str, community_id: int, db=Depends(data_b.connection), ):
    """Here you can get all_events in community\n
    access_token: This is access auth token. You can get it when create account, login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    com_data = await conn.read_data(db=db, table='community', id_name='community_id', id_data=community_id)
    if not com_data:
        return Response(content="bad community_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    event_data = await conn.read_events(db=db, community_id=community_id)
    event_list = []
    for one in event_data:
        event: Event = Event.parse_obj(one)
        event_list.append(event.dict())

    dead_event_data = await conn.read_dead_events(db=db, community_id=community_id)
    dead_event_list = []
    for one in dead_event_data:
        event: Event = Event.parse_obj(one)
        dead_event_list.append(event.dict())

    return JSONResponse(content={"ok": True,
                                 'actual_events': event_list,
                                 'dead_events': dead_event_list,
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.delete(path='/event', tags=['Event'], responses=delete_event_res)
async def delete_event_by_id(access_token: str, event_id: int, db=Depends(data_b.connection), ):
    """Here you can delete event by id\n
    access_token: This is access auth token. You can get it when create account, login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
    if not event_data:
        return Response(content="bad event_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)
    if event_data[0]['creator_id'] != user_id[0][0]:
        return JSONResponse(content={"ok": False, 'description': "not enough rights"},
                            status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.delete_where(db=db, table='event', id_name='event_id', data=event_id)
    return JSONResponse(content={"ok": True,
                                 "description": "Event successful deleted"},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.post(path='/read_event', tags=['Event'], responses=create_event_res)
async def create_read_event_note(access_token: str, event_id: int, db=Depends(data_b.connection)):
    """Use it route when user open event.\n
    event_id: it is event id\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
    if not event_data:
        return Response(content="bad event_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)
    user_read_event = await conn.read_data_2_were(db=db, table='read_event', id_name1='event_id', id_data1=event_id,
                                             id_name2='user_id', id_data2=user_id[0][0])
    if not user_read_event:
        await conn.create_read_event(db=db, user_id=user_id[0][0], event_id=event_id)
    read_event_count = await conn.read_event_count_were(db=db, event_id=event_id)
    if not read_event_count:
        read_event_count = 0
    else:
        read_event_count = read_event_count[0][0]
    return JSONResponse(content={"ok": True,
                                 'read_event_count': read_event_count,
                                 'description': "Successful read event"},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/read_event', tags=['Event'], responses=create_event_res)
async def get_read_event_count(access_token: str, event_id: int, db=Depends(data_b.connection)):
    """Create event in community.\n
    event_id: it is event id\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
    if not event_data:
        return Response(content="bad event_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    read_event_count = await conn.read_event_count_were(db=db, event_id=event_id)
    if not read_event_count:
        read_event_count = 0
    else:
        read_event_count = read_event_count[0][0]
    return JSONResponse(content={"ok": True,
                                 'read_event_count': read_event_count},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})
