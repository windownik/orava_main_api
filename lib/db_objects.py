import datetime

from fastapi import Depends
from pydantic import BaseModel

from lib import sql_connect as conn
from lib.routes.files.files_scripts import create_file_json


class User(BaseModel):
    user_id: int
    name: str
    middle_name: str
    surname: str
    phone: int
    email: str
    image_link: str
    image_link_little: str
    description: str
    lang: str
    status: str
    last_active: int
    create_date: int


class File(BaseModel):
    file_id: int = 0
    file_type: str = '0'


class Message(BaseModel):
    """
    msg_type: Может принимать значения 'new_message', 'system',
    """
    msg_id: int = 0
    client_msg_id: int = 0
    msg_type: str = 'new_message'
    text: str = '0'

    from_id: int = 0
    reply_id: int = 0
    chat_id: int = 0
    to_id: int = 0
    file_id: int = 0

    status: str = '0'
    read_date: int = 0
    deleted_date: int = 0
    create_date: int = 0

    sender: User = None

    def update_msg_id(self, msg_id: int):
        self.msg_id = msg_id

    def update_user_sender(self, sender: User):
        self.sender = sender

    async def add_user_to_msg(self, db: Depends, reqwest_user: User):
        if self.from_id == reqwest_user.user_id:
            self.update_user_sender(reqwest_user)
        else:
            user_data = await conn.read_data(db=db, name='*', table='all_users', id_name='user_id',
                                             id_data=self.from_id)
            msg_send_user: User = User.parse_obj(user_data[0])
            self.update_user_sender(msg_send_user)


class Chat(BaseModel):
    chat_id: int = 0
    owner_id: int = 0
    owner_user: User = None
    all_users_count: int = 0
    all_users: list = []
    community_id: int = 0
    name: str = '0'
    img_url: str = '0'
    little_img_url: str = '0'
    chat_type: str = 'dialog'
    status: str = '0'
    open_profile: bool = True
    send_media: bool = True
    send_voice: bool = True
    deleted_date: int = None
    create_date: int = None

    async def to_json(self, db: Depends, reqwest_user: User):
        users_data = await conn.get_users_in_chat(db=db, chat_id=self.chat_id)
        for one in users_data:
            user = User.parse_obj(one)
            self.all_users.append(user)
        users_count = (await conn.get_count_users_in_chat(db=db, chat_id=self.chat_id))[0][0]

        self.all_users_count = users_count

        user_data = await conn.read_data(table='all_users', id_name='user_id', id_data=self.owner_id, db=db)
        self.owner_user = User.parse_obj(user_data[0])

        resp = self.dict()
        unread_message = []
        unread_count = 0
        if self.status == 'delete':
            pass
        else:
            msg_data = await conn.get_users_unread_messages(db=db, chat_id=self.chat_id)
            unread_count = (await conn.get_users_unread_messages_count(db=db, chat_id=self.chat_id))[0][0]
            for one in msg_data:
                msg: Message = Message.parse_obj(one)
                msg_dict = await add_user_and_reply_to_msg(db=db, msg=msg, reqwest_user=reqwest_user)
                unread_message.append(msg_dict)

        resp.pop('owner_id')
        resp['unread_message'] = unread_message
        resp['unread_count'] = unread_count
        return resp


async def add_user_and_reply_to_msg(db: Depends, msg: Message, reqwest_user: User) -> dict:
    await msg.add_user_to_msg(reqwest_user=reqwest_user, db=db)

    msg_dict = msg.dict()
    msg_dict = await add_file_to_dict(msg_dict=msg_dict, msg=msg, db=db)
    if msg.reply_id != 0:
        reply_msg_data = await conn.read_data(db=db, table='messages', id_name='msg_id', id_data=msg.reply_id)
        reply_msg: Message = Message.parse_obj(reply_msg_data[0])
        await reply_msg.add_user_to_msg(reqwest_user=reqwest_user, db=db)

        msg_dict['reply'] = reply_msg.dict()
    return msg_dict


async def add_file_to_dict(msg_dict: dict, msg: Message, db: Depends,) -> dict:
    if msg.file_id == 0:
        return msg_dict
    file = await conn.read_data(db=db, table='files', id_name='id', id_data=msg.file_id, name='*')
    resp = create_file_json(file[0])
    msg_dict['file'] = resp
    return msg_dict


class Community(BaseModel):
    community_id: int = 0
    owner_id: int = 0
    name: str = '0'
    main_chat_id: int = 0
    total_users_count: int = 0
    join_code: str = '0'
    img_url: str = '0'
    little_img_url: str = '0'
    status: str = '0'
    open_profile: bool = True
    send_media: bool = True
    send_voice: bool = True
    moder_create_chat: bool = True
    deleted_date: int = 0
    create_date: int = 0


class ReceiveMessage(BaseModel):
    access_token: str = 0
    msg_client_id: int = 0
    msg_type: str = '0'
    body: Message = None


class Event(BaseModel):
    event_id: int = 0
    community_id: int = 0
    creator_id: int = 0
    creator_name: str = '0'
    creator_surname: str = '0'
    creator_middlename: str = '0'
    title: str = '0'
    text: str = '0'
    event_type: str = 'event'
    status: str = '0'
    repeat_days: int = 0
    start_time: int = 0
    end_time: int = 0
    death_date: int = 0
    read_date: int = 0
    deleted_date: int = 0
    create_date: int = 0


class Quiz(BaseModel):
    quiz_id: int = 0
    community_id: int = 0
    creator_id: int = 0
    title: str = '0'
    description: str = '0'
    death_time: int = 0
    death_date: int = 0
    deleted_date: int = 0
    create_date: int = 0


class QAndA(BaseModel):
    q_id: int = 0
    event_id: int = 0
    answer_id: int = 0
    creator_id: int = 0
    text: str = '0'
    create_date: int = 0


