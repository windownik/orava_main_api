import json
import os

import starlette.status as _status
from fastapi import Depends
from starlette.responses import Response, JSONResponse

from lib import sql_connect as conn
from lib.db_objects import User, Community, Quiz
from lib.response_examples import *
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.post(path='/quiz', tags=['Quiz'], responses=create_event_res)
async def create_new_quiz(access_token: str, community_id: int, title: str, text: str, question_list: str,
                          death_date: int = 0, death_time: int = 0, db=Depends(data_b.connection)):
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
    data = json.loads(question_list)
    quiz_data = await conn.create_quiz(db=db, community_id=community.community_id, creator_id=user.user_id,
                                       title=title, description=text, death_date=death_date, death_time=death_time)
    quiz: Quiz = Quiz.parse_obj(quiz_data[0])
    # создаем пуш для всех пользователей

    for i in data:
        await conn.create_quiz_question(db=db, quiz_id=quiz.quiz_id, text=i['text'])

    resp = await build_quiz_json(db=db, quiz_data=quiz_data[0])

    community_users = await conn.read_community_users_with_lang(db=db, community_id=community.community_id)
    for user in community_users:
        if user[1] == 'ru':
            push_title = 'Новый опрос'
            push_text = f'В сообществе {community.name} создан новый опрос'
        else:
            push_title = 'New quiz'
            push_text = f'A new quiz has been created in the {community.name} community.'
        await conn.save_push_to_sending(db=db, user_id=user[0], title=push_title, short_text=push_text,
                                        main_text=json.dumps(resp),
                                        push_type='new_quiz', msg_id=quiz.quiz_id)

    return JSONResponse(content={"ok": True,
                                 'quiz': resp},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})

# @app.put(path='/event', tags=['Event'], responses=create_event_res)
# async def update_event(access_token: str, event_id: int, title: str, text: str, repeat_days: int = 0,
#                        death_date: int = 0, event_type: str = 'event', start_time: int = 0, end_time: int = 0,
#                        db=Depends(data_b.connection)):
#     """Create event in community.\n
#     community_id: it is community id\n
#     title: it is community name\n
#     text:  main text of event\n
#     event_type: type of event can be event or announcement\n
#     """
#
#     user_id = await conn.get_token(db=db, token_type='access', token=access_token)
#     if not user_id:
#         return JSONResponse(content={"ok": False, "description": "bad access token"},
#                             status_code=_status.HTTP_401_UNAUTHORIZED)
#
#     event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
#     if not event_data:
#         return Response(content="bad event_id",
#                         status_code=_status.HTTP_400_BAD_REQUEST)
#
#     if event_type not in ('event', 'announcement'):
#         return JSONResponse(content={"ok": False,
#                                      'description': 'Bad event_type'},
#                             status_code=_status.HTTP_400_BAD_REQUEST, )
#
#     await conn.update_event(db=db, event_id=event_id, title=title, text=text, death_date=death_date,
#                             repeat_days=repeat_days, event_type=event_type, end_time=end_time, start_time=start_time)
#
#     event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
#     event: Event = Event.parse_obj(event_data[0])
#     return JSONResponse(content={"ok": True,
#                                  'event': event.dict()},
#                         status_code=_status.HTTP_200_OK,
#                         headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/quiz', tags=['Quiz'], responses=create_event_res)
async def get_quiz_by_id(access_token: str, quiz_id: int, db=Depends(data_b.connection), ):
    """Here you can get community by id\n
    access_token: This is access auth token. You can get it when create account, login"""
    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return Response(content="bad access token",
                        status_code=_status.HTTP_401_UNAUTHORIZED)
    quiz_data = await conn.read_data(db=db, table='quiz', id_name='quiz_id', id_data=quiz_id)
    if not quiz_data:
        return JSONResponse(content={"ok": False, 'description': "bad quiz_id"},
                            status_code=_status.HTTP_400_BAD_REQUEST)
    resp = await build_quiz_json(db=db, quiz_data=quiz_data[0])

    return JSONResponse(content={"ok": True,
                                 'quiz': resp},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/all_quiz', tags=['Quiz'], responses=create_event_res)
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

    quiz_data = await conn.read_quiz(db=db, community_id=community_id)
    quiz_list = []
    for one in quiz_data:
        resp = await build_quiz_json(db=db, quiz_data=one)
        quiz_list.append(resp)

    dead_quiz_data = await conn.read_dead_quiz(db=db, community_id=community_id)
    dead_quiz_list = []
    for one in dead_quiz_data:
        resp = await build_quiz_json(db=db, quiz_data=one)
        dead_quiz_list.append(resp)

    return JSONResponse(content={"ok": True,
                                 'actual_quiz': quiz_list,
                                 'dead_quiz': dead_quiz_list,
                                 },
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


# @app.delete(path='/event', tags=['Event'], responses=delete_event_res)
# async def delete_event_by_id(access_token: str, event_id: int, db=Depends(data_b.connection), ):
#     """Here you can delete event by id\n
#     access_token: This is access auth token. You can get it when create account, login"""
#     user_id = await conn.get_token(db=db, token_type='access', token=access_token)
#     if not user_id:
#         return Response(content="bad access token",
#                         status_code=_status.HTTP_401_UNAUTHORIZED)
#     event_data = await conn.read_data(db=db, table='event', id_name='event_id', id_data=event_id)
#     if not event_data:
#         return Response(content="bad event_id",
#                         status_code=_status.HTTP_400_BAD_REQUEST)
#     if event_data[0]['creator_id'] != user_id[0][0]:
#         return JSONResponse(content={"ok": False, 'description': "not enough rights"},
#                             status_code=_status.HTTP_400_BAD_REQUEST)
#
#     await conn.delete_where(db=db, table='event', id_name='event_id', data=event_id)
#     return JSONResponse(content={"ok": True,
#                                  "description": "Event successful deleted"},
#                         status_code=_status.HTTP_200_OK,
#                         headers={'content-type': 'application/json; charset=utf-8'})


@app.post(path='/quiz_answer', tags=['Quiz'], responses=create_event_res)
async def create_new_quiz(access_token: str, quiz_id: int, question_id: int, db=Depends(data_b.connection)):
    """Create quiz_answer in quiz.\n
    quiz_id: it is quiz id\n
    answer_id: it is answer id\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    quiz_data = await conn.read_data(db=db, table='quiz', id_name='quiz_id', id_data=quiz_id)
    if not quiz_data:
        return Response(content="bad quiz_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.user_vote_in_quiz(db=db, quiz_id=quiz_id, question_id=question_id, user_id=user_id[0][0])

    resp = await build_quiz_json(db=db, quiz_data=quiz_data[0])

    return JSONResponse(content={"ok": True,
                                 'description': 'user vote successful',
                                 'quiz':  resp},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.delete(path='/quiz_answer', tags=['Quiz'], responses=create_event_res)
async def create_new_quiz(access_token: str, quiz_answer_id: int, db=Depends(data_b.connection)):
    """Delete quiz_answer by quiz_answer_id.\n
    quiz_answer_id: it is quiz id\n
    """

    user_id = await conn.get_token(db=db, token_type='access', token=access_token)
    if not user_id:
        return JSONResponse(content={"ok": False, "description": "bad access token"},
                            status_code=_status.HTTP_401_UNAUTHORIZED)

    quiz_data = await conn.read_data(db=db, table='quiz_answer', id_name='q_id', id_data=quiz_answer_id)

    if not quiz_data:
        return Response(content="bad quiz_answer_id",
                        status_code=_status.HTTP_400_BAD_REQUEST)

    await conn.delete_where(db=db, table='quiz_answer', id_name='q_id', data=quiz_answer_id)

    return JSONResponse(content={"ok": True,
                                 'description': 'quiz answer deleted'},
                        status_code=_status.HTTP_200_OK,
                        headers={'content-type': 'application/json; charset=utf-8'})


async def build_quiz_json(db: Depends, quiz_data: tuple) -> json:
    quiz: Quiz = Quiz.parse_obj(quiz_data)
    quiz_questions = await conn.read_data(db=db, table='quiz_question', id_name='quiz_id', id_data=quiz.quiz_id)

    user_data = await conn.read_data(table='all_users', id_name='user_id', id_data=quiz.creator_id, db=db,
                                     name='name, middle_name, surname')
    quiz.creator_name = user_data[0][0]
    quiz.creator_middlename = user_data[0][1]
    quiz.creator_surname = user_data[0][2]

    # Add questions list
    questions = []
    for one in quiz_questions:
        questions.append({"question_id": one[0], "text": one[2]})
    resp = quiz.dict()
    resp["questions"] = questions

    # Add questions list
    quiz_answer = await conn.read_data(db=db, table='quiz_answer', id_name='quiz_id', id_data=quiz.quiz_id)
    answers = []
    for one in quiz_answer:
        answers.append({"answer_id": one['answer_id'],
                        "question_id": one['q_id'],
                        "user_id": one['creator_id'],
                        "quiz_id": one['quiz_id'],
                        "create_date": one['create_date'],
                        })
    resp["answers"] = answers
    return resp
