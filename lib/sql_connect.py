import datetime
import os
import time
from hashlib import sha256

from fastapi_asyncpg import configure_asyncpg
from lib.app_init import app
from fastapi import Depends

from lib.db_objects import User

password = os.environ.get("DATABASE_PASS")
host = os.environ.get("DATABASE_HOST")
port = os.environ.get("DATABASE_PORT")
db_name = os.environ.get("DATABASE_NAME")

password = 102015 if password is None else password
host = '127.0.0.1' if host is None else host
port = 5432 if port is None else port
db_name = 'cleaner_api' if db_name is None else db_name

# Создаем новую таблицу
data_b = configure_asyncpg(app, f'postgres://postgres:{password}@{host}:{port}/{db_name}')


async def create_all_users_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS all_users (
 user_id SERIAL PRIMARY KEY,
 phone BIGINT UNIQUE DEFAULT 0,
 email TEXT DEFAULT '0',
 name TEXT DEFAULT '0',
 middle_name TEXT DEFAULT '0',
 surname TEXT DEFAULT '0',
 image_link TEXT DEFAULT '0',
 image_link_little TEXT DEFAULT '0',
 description TEXT DEFAULT '0',
 lang TEXT DEFAULT 'en',
 status TEXT DEFAULT 'active',
 push TEXT DEFAULT '0',
 last_active BIGINT DEFAULT 0,
 create_date BIGINT DEFAULT 0)''')


# Создаем новую таблицу
async def create_token_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS token (
 id SERIAL PRIMARY KEY,
 user_id BIGINT DEFAULT 0,
 token TEXT DEFAULT '0',
 token_type TEXT DEFAULT 'access',
 change_password INTEGER DEFAULT 0,
 create_date timestamp,
 death_date timestamp
 )''')


# Создаем новую таблицу
# Таблица для записи статей информации о файлах
async def create_files_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS files (
 id SERIAL PRIMARY KEY,
 file_name TEXT DEFAULT '0',
 file_path TEXT DEFAULT '0',
 file_type TEXT DEFAULT '0',
 owner_id INTEGER DEFAULT 0,
 little_file_id INTEGER DEFAULT 0,
 middle_file_id INTEGER DEFAULT 0,
 file_size BIGINT DEFAULT 0,
 client_file_id INTEGER DEFAULT 0,
 create_date timestamptz
 )''')


# Создаем новую таблицу
# Таблица для записи статей информации о файлах
async def create_sms_code_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS sms_code (
 id SERIAL PRIMARY KEY,
 phone BIGINT DEFAULT 0,
 code TEXT DEFAULT '0',
 create_date timestamp DEFAULT now()
 )''')


# Создаем новую таблицу
# Таблица для записи статей информации о файлах
async def create_sending_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS sending (
 id SERIAL PRIMARY KEY,
 user_id INTEGER DEFAULT 0,
 title TEXT DEFAULT '0',
 short_text TEXT DEFAULT '0',
 main_text TEXT DEFAULT '0',
 img_url TEXT DEFAULT '0',
 push_type TEXT DEFAULT 'text',
 status TEXT DEFAULT 'created',
 msg_line_id INTEGER DEFAULT 0
 )''')


# Создаем новую таблицу
# Таблица для записи всех видов сообщений для всех пользователей
async def create_msg_line_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS messages (
 msg_id BIGSERIAL PRIMARY KEY,
 text TEXT DEFAULT '0',
 from_id INTEGER DEFAULT 0,
 reply_id INTEGER DEFAULT 0,
 chat_id INTEGER DEFAULT 0,
 to_id INTEGER DEFAULT 0,
 file_id INTEGER DEFAULT 0,
 status TEXT DEFAULT 'not_read',
 read_date BIGINT DEFAULT 0,
 deleted_date BIGINT DEFAULT 0,
 create_date BIGINT DEFAULT 0
 )''')


# Создаем новую таблицу
# Таблица для записи всех видов сообщений для всех пользователей
async def create_chats_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS all_chats (
 chat_id SERIAL PRIMARY KEY,
 owner_id INTEGER DEFAULT 0,
 community_id INTEGER DEFAULT 0,
 name TEXT DEFAULT '0',
 img_url TEXT DEFAULT '0',
 little_img_url TEXT DEFAULT '0',
 chat_type TEXT DEFAULT 'dialog',
 status TEXT DEFAULT 'create',
 open_profile BOOLEAN DEFAULT true,
 send_media BOOLEAN DEFAULT true,
 send_voice BOOLEAN DEFAULT true,
 deleted_date BIGINT DEFAULT 0,
 create_date BIGINT DEFAULT 0
 )''')


# Создаем новую таблицу
# Таблица для записи всех видов сообщений для всех пользователей
async def create_community_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS community (
 community_id SERIAL PRIMARY KEY,
 owner_id INTEGER DEFAULT 0,
 name TEXT DEFAULT '0',
 main_chat_id INTEGER DEFAULT 0,
 join_code TEXT UNIQUE,
 img_url TEXT DEFAULT '0',
 little_img_url TEXT DEFAULT '0',
 status TEXT DEFAULT 'create',
 open_profile BOOLEAN DEFAULT true,
 send_media BOOLEAN DEFAULT true,
 send_voice BOOLEAN DEFAULT true,
 moder_create_chat BOOLEAN DEFAULT true,
 deleted_date BIGINT DEFAULT 0,
 create_date BIGINT DEFAULT 0
 )''')


# Создаем новую таблицу
# Таблица для записи всех видов сообщений для всех пользователей
async def create_users_comm_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS users_community (
 id SERIAL PRIMARY KEY,
 community_id INTEGER DEFAULT 0,
 user_id INTEGER DEFAULT 0,
 status TEXT DEFAULT 'user',
 ban BOOLEAN DEFAULT false,
 deleted_date BIGINT DEFAULT 0,
 create_date BIGINT DEFAULT 0
 )''')


# Создаем новую таблицу
# Таблица для записи всех видов сообщений для всех пользователей
async def create_users_chats_table(db):
    await db.execute(f'''CREATE TABLE IF NOT EXISTS users_chat (
 id SERIAL PRIMARY KEY,
 chat_id INTEGER DEFAULT 0,
 user_id INTEGER DEFAULT 0,
 status TEXT DEFAULT 'user',
 ban BOOLEAN DEFAULT false,
 send_text BOOLEAN DEFAULT true,
 send_media BOOLEAN DEFAULT true,
 send_voice BOOLEAN DEFAULT true,
 can_receive_push BOOLEAN DEFAULT true,
 push_sent BOOLEAN DEFAULT false,
 deleted_date BIGINT DEFAULT 0,
 create_date BIGINT DEFAULT 0
 )''')


# Создаем новую таблицу
async def create_user(db: Depends, user: User):
    user_id = await db.fetch(f"INSERT INTO all_users (name, middle_name, surname, phone, email, image_link, "
                             f"image_link_little, description, lang, last_active, create_date) "
                             f"VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) "
                             f"ON CONFLICT DO NOTHING RETURNING *;", user.name, user.middle_name, user.surname,
                             user.phone, user.email, user.image_link, user.image_link_little, user.description,
                             user.lang, user.last_active, user.create_date)
    return user_id


# Создаем новую таблицу
async def save_users_work(db: Depends, user_id: int, work_type: str, object_id: int, object_size: int):
    await db.fetch(f"INSERT INTO work (user_id, work_type, object_id, object_size) "
                   f"VALUES ($1, $2, $3, $4) "
                   f"ON CONFLICT DO NOTHING;", user_id, work_type, object_id, object_size)
    return user_id


# Создаем новый токен
async def create_token(db: Depends, user_id, token_type):
    create_date = datetime.datetime.now()
    if token_type == 'access':
        death_date = create_date + datetime.timedelta(minutes=30)
    else:
        death_date = create_date + datetime.timedelta(days=30)
    now = datetime.datetime.now()
    token = sha256(f"{user_id}.{now}".encode('utf-8')).hexdigest()
    token = await db.fetch(f"INSERT INTO token (user_id, token, token_type, create_date, death_date) "
                           f"VALUES ($1, $2, $3, $4, $5) "
                           f"ON CONFLICT DO NOTHING RETURNING token;", user_id, token, token_type,
                           create_date, death_date)
    return token


# Создаем новое сообщение
async def create_msg(db: Depends, msg_id: int, msg_type: str, title: str, text: str, description: str, lang: str,
                     from_id: int, to_id: int, user_type: str):
    now = datetime.datetime.now()
    new_id = await db.fetch(f"INSERT INTO message_line (msg_id, msg_type, title, text, description, lang, from_id, "
                            f"to_id, user_type, create_date) "
                            f"VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10) "
                            f"ON CONFLICT DO NOTHING RETURNING id;",
                            msg_id, msg_type, title, text, description, lang, from_id, to_id, user_type, now)
    return new_id


# Создаем новую запись в базе данных
async def save_new_file(db: Depends, file_name: str, file_path: str, file_type: str, owner_id: int, file_size: int,
                        client_file_id: int):
    now = datetime.datetime.now()
    file_id = await db.fetch(f"INSERT INTO files (file_name, file_path, file_type, owner_id, file_size, client_file_id,"
                             f" create_date) "
                             f"VALUES ($1, $2, $3, $4, $5, $6, $7) "
                             f"ON CONFLICT DO NOTHING RETURNING *;", file_name, file_path, file_type, owner_id,
                             file_size, client_file_id, now)
    return file_id


# Создаем новую запись в базе данных
async def save_new_sms_code(db: Depends, phone: int, code: str):
    file_id = await db.fetch(f"INSERT INTO sms_code (phone, code) "
                             f"VALUES ($1, $2) "
                             f"ON CONFLICT DO NOTHING RETURNING id;", phone, code)
    return file_id


# Создаем много новых записей в таблице рассылки
async def save_push_to_sending(db: Depends, msg_id: int, user_id: int, title: str, short_text: str, push_type: str,
                               main_text: str = '0', img_url: str = '0'):
    sql = f"INSERT INTO sending (user_id, title, short_text, main_text, img_url, push_type, msg_line_id) " \
          f"VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT DO NOTHING;"
    await db.fetch(sql, user_id, title, short_text, main_text, img_url, push_type, msg_id)
    print('save to push', user_id)


# Создаем много новых записей в таблице рассылки
async def save_msg(db: Depends, msg: dict):
    now = datetime.datetime.now()
    data = await db.fetch(f"INSERT INTO messages (text, from_id, reply_id, chat_id, file_id, create_date) "
                          f"VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING RETURNING msg_id;",
                          msg['text'], msg['from_id'], msg['reply_id'], msg['chat_id'], msg['file_id'],
                          int(time.mktime(now.timetuple())))
    return data


# Создаем новое комюнити
async def create_community(db: Depends, owner_id: int, name: str, main_chat_id: int, join_code: str, open_profile: bool,
                           send_media: bool, send_voice: bool, moder_create_chat: bool):
    now = datetime.datetime.now()
    data = await db.fetch(f"INSERT INTO community (owner_id, name, main_chat_id, join_code, open_profile, send_media, "
                          f"send_voice, moder_create_chat, create_date) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) "
                          f"ON CONFLICT DO NOTHING RETURNING *;",
                          owner_id, name, main_chat_id, join_code, open_profile, send_media, send_voice,
                          moder_create_chat, int(time.mktime(now.timetuple())))
    return data


# Создаем новый чат
async def create_chat(db: Depends, owner_id: int, name: str = '0', img_url: str = '0', little_img_url: str = '0',
                      chat_type: str = 'dialog', community_id: int = 0):
    now = datetime.datetime.now()
    data = await db.fetch(f"INSERT INTO all_chats (owner_id, community_id, name, img_url, little_img_url, chat_type, "
                          f"create_date) VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT DO NOTHING RETURNING *;",
                          owner_id, community_id, name, img_url, little_img_url, chat_type,
                          int(time.mktime(now.timetuple())))
    return data


# Добавляем пользователя в комюнити
async def save_user_to_comm(db: Depends, com_id: int, user_id: int, status: str = 'user'):
    now = datetime.datetime.now()
    data = await db.fetch(f"INSERT INTO users_community (community_id, user_id, status, create_date) "
                          f"VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING RETURNING *;",
                          com_id, user_id, status, int(time.mktime(now.timetuple())))
    return data


# Добавляем пользователя в чат
async def save_user_to_chat(db: Depends, chat_id: int, user_id: int, status: str = 'user'):
    now = datetime.datetime.now()
    data = await db.fetch(f"INSERT INTO users_chat (chat_id, user_id, status, create_date) "
                          f"VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING RETURNING *;",
                          chat_id, user_id, status, int(time.mktime(now.timetuple())))
    return data


# получаем данные с одним фильтром
async def read_data(db: Depends, table: str, id_name: str, id_data, name: str = '*'):
    data = await db.fetch(f"SELECT {name} FROM {table} WHERE {id_name} = $1;", id_data)
    return data


# получаем данные с одним фильтром
async def get_users_by_phone_list(db: Depends, users_phones: list):
    sql_where = ''
    for phone in users_phones:
        if phone.isdigit():
            sql_where = f'{sql_where}phone = {phone} OR '
    if sql_where == '':
        return []
    data = await db.fetch(f"SELECT * FROM all_users WHERE {sql_where[:-4]};")
    return data


# получаем данные с одним фильтром
async def get_users_in_chat(db: Depends, chat_id: int, offset: int = 0, limit: int = 10):
    data = await db.fetch(f"SELECT all_users.user_id, all_users.phone, all_users.email, all_users.name, "
                          f"all_users.middle_name, all_users.surname, all_users.image_link, "
                          f"all_users.image_link_little, all_users.description, all_users.lang, all_users.status, "
                          f"all_users.push, all_users.last_active, all_users.create_date FROM users_chat "
                          f"JOIN all_users "
                          f"ON users_chat.user_id = all_users.user_id "
                          f"WHERE users_chat.chat_id = $1 ORDER BY users_chat.id OFFSET $2 LIMIT $3;",
                          chat_id, offset, limit)
    return data


# получаем данные с одним фильтром
async def get_count_users_in_chat(db: Depends, chat_id: int,):
    data = await db.fetch(f"SELECT COUNT(all_users.user_id) FROM users_chat "
                          f"JOIN all_users "
                          f"ON users_chat.user_id = all_users.user_id "
                          f"WHERE users_chat.chat_id = $1;",
                          chat_id)
    return data


# получаем данные с одним фильтром
async def get_users_dialog(db: Depends, user_id: int):
    data = await db.fetch(f"SELECT users_chat.chat_id, all_chats.owner_id FROM users_chat JOIN all_chats "
                          f"ON users_chat.chat_id = all_chats.chat_id "
                          f"WHERE users_chat.user_id = $1 AND all_chats.chat_type = 'dialog';", user_id, )
    return data


# получаем данные с одним фильтром
async def get_users_chats(db: Depends, user_id: int):
    data = await db.fetch(f"SELECT users_chat.chat_id, "
                          f"all_chats.owner_id, all_chats.community_id, all_chats.name, all_chats.img_url,"
                          f" all_chats.little_img_url, all_chats.chat_type, all_chats.status, all_chats.open_profile, "
                          f"all_chats.send_media, all_chats.send_voice, all_chats.deleted_date, all_chats.create_date "
                          f"FROM users_chat JOIN all_chats "
                          f"ON users_chat.chat_id = all_chats.chat_id "
                          f"WHERE users_chat.user_id = $1 AND all_chats.status != 'delete';", user_id, )
    return data


# получаем данные с одним фильтром
async def get_users_community(db: Depends, user_id: int):
    data = await db.fetch(f"SELECT users_community.community_id, "
                          f"community.owner_id, community.name, community.main_chat_id, community.join_code, "
                          f"community.img_url, community.little_img_url, community.status, community.open_profile, "
                          f"community.send_media, community.send_voice, community.moder_create_chat, "
                          f"community.deleted_date, community.create_date "
                          f"FROM users_community JOIN community "
                          f"ON users_community.community_id = community.community_id "
                          f"WHERE users_community.user_id = $1 AND community.deleted_date = 0;", user_id, )
    return data


# получаем данные с одним фильтром
async def check_user_in_chat(db: Depends, user_id: int, chat_id: int):
    data = await db.fetch(f"SELECT users_chat.chat_id "
                          f"FROM users_chat JOIN all_chats "
                          f"ON users_chat.chat_id = all_chats.chat_id "
                          f"WHERE users_chat.user_id = $1 "
                          f"AND users_chat.chat_id = $2 "
                          f"AND all_chats.status != 'delete';", user_id, chat_id)
    return data


# получаем 20 не прочитанных сообщений
async def get_users_unread_messages(db: Depends, chat_id: int, ):
    data = await db.fetch(f"SELECT * FROM messages "
                          f"WHERE chat_id = $1 "
                          f"AND read_date = 0 "
                          f"AND deleted_date = 0 ORDER BY create_date DESC LIMIT 20;", chat_id)
    return data


# получаем 20 не прочитанных сообщений
async def get_chat_messages_by_last_msg(db: Depends, lust_msg_id: int, chat_id: int, old_msg_scroll: bool):
    if old_msg_scroll:
        return await db.fetch(f"SELECT * FROM messages "
                              f"WHERE chat_id = $1 "
                              f"AND msg_id < $2 "
                              f"AND deleted_date = 0 ORDER BY create_date DESC LIMIT 20;", chat_id, lust_msg_id)
    else:
        return await db.fetch(f"SELECT * FROM messages "
                              f"WHERE chat_id = $1 "
                              f"AND msg_id > $2 "
                              f"AND deleted_date = 0 ORDER BY create_date LIMIT 20;", chat_id, lust_msg_id)


# получаем данные с одним фильтром
async def get_users_unread_messages_count(db: Depends, chat_id: int, ):
    data = await db.fetch(f"SELECT COUNT(*) FROM messages "
                          f"WHERE chat_id = $1 "
                          f"AND read_date = 0 "
                          f"AND deleted_date = 0;", chat_id)
    return data


# получаем данные с одним фильтром
async def read_data_order(db: Depends, table: str, id_name: str, id_data, name: str = '*', order: str = 'id DESC'):
    data = await db.fetch(f"SELECT {name} FROM {table} WHERE {id_name} = $1 ORDER BY {order};", id_data)
    return data


# получаем количество данных с одним фильтром
async def count_data(db: Depends, table: str, id_name: str, id_data):
    data = await db.fetch(f"SELECT COUNT(*) FROM {table} WHERE {id_name} = $1;", id_data)
    return data


# получаем пользователей для рассылки с фильтрацией
async def get_users_for_push(db: Depends, lang: str, users_account_type: str, ):
    sql_where = ''
    if lang in ('ru', 'en', 'he'):
        sql_where = f"AND lang = '{lang}' "

    if users_account_type in ('worker', 'customer'):
        sql_where = f"{sql_where}AND status = '{users_account_type}'"

    if sql_where != '':
        sql_where = f" WHERE {sql_where[4:]}"

    data = await db.fetch(f"SELECT user_id FROM all_users{sql_where};")
    return data


# получаем данные без фильтров
async def read_all(db: Depends, table: str, order: str, name: str = '*'):
    data = await db.fetch(f"SELECT {name} FROM {table} ORDER BY {order};")
    return data


# получаем все новые сообщения для пользователя с id
async def read_all_msg(db: Depends, user_id: int, offset: int = 0, limit: int = 0, ):
    offset_limit = ''

    if offset != 0 or limit != 0:
        offset_limit = f" OFFSET {offset} LIMIT {limit}"
    data = await db.fetch(f"SELECT * FROM message_line "
                          f"WHERE (to_id=$1 OR (to_id=0 AND user_type='admin')) "
                          f"AND (status='created' OR status='read') ORDER BY id DESC{offset_limit};", user_id)
    return data


# получаем все новые сообщения для пользователя с id
async def read_job_app_msg(db: Depends, order_id: int, ):
    data = await db.fetch(f"SELECT * FROM message_line "
                          f"WHERE msg_id=$1 AND msg_type='job_application' "
                          f"AND (status='created' OR status='read') ORDER BY id DESC;", order_id)
    return data


# получаем все новые сообщения для пользователя с id
async def read_all_msg_user(db: Depends, user_id: int, offset: int = 0, limit: int = 0, ):
    offset_limit = ''

    if offset != 0 or limit != 0:
        offset_limit = f" OFFSET {offset} LIMIT {limit}"
    data = await db.fetch(f"SELECT * FROM message_line "
                          f"WHERE to_id=$1 "
                          f"AND (status='created' OR status='read') ORDER BY id DESC{offset_limit};", user_id)
    return data


# получаем данные без фильтров
async def count_admin_msg(db: Depends, user_id: int):
    data = await db.fetch(f"SELECT COUNT(id) FROM message_line "
                          f"WHERE (to_id=$1 OR (to_id=0 AND user_type='admin')) AND status='created';",
                          user_id)
    return data


# получаем данные без фильтров
async def count_users_msg(db: Depends, user_id: int):
    data = await db.fetch(f"SELECT COUNT(id) FROM message_line "
                          f"WHERE to_id=$1 "
                          f"AND (status='created' OR status='read');",
                          user_id)
    return data


# получаем данные без фильтров
async def count_msg_user(db: Depends, user_id: int):
    data = await db.fetch(f"SELECT COUNT(id) FROM message_line "
                          f"WHERE to_id=$1 AND status='created';", user_id)
    return data


# получаем данные с 2 фильтрами
async def read_data_2_were(db: Depends, table: str, id_name1: str, id_name2: str, id_data1, id_data2, name: str):
    data = await db.fetch(f"SELECT {name} FROM {table} WHERE {id_name1} = $1 AND  {id_name2} = $1;", id_data1, id_data2)
    return data


# Проверяем токен на валидность и возвращаем user_id
async def get_token(db: Depends, token_type: str, token: str):
    now = datetime.datetime.now()
    data = await db.fetch(f"SELECT user_id, death_date FROM token "
                          f"WHERE token_type = $1 "
                          f"AND token = $2 "
                          f"AND death_date > $3 "
                          f"AND change_password = 0;",
                          token_type, token, now)
    return data


# Создаем новую таблицу
async def update_user(db: Depends, name: str, surname: str, midl_name: str, lang: str, image_link: str,
                      image_link_little: str, user_id: int, push: str = '0'):

    if name == '0' and surname == '0' and midl_name == '0' and lang == '0' and image_link == '0' \
            and push == '0':
        return user_id
    if name != '0':
        await db.fetch(f"UPDATE all_users SET name=$1 WHERE user_id=$2;",
                       name, user_id)
    if surname != '0':
        await db.fetch(f"UPDATE all_users SET surname=$1 WHERE user_id=$2;",
                       surname, user_id)
    if midl_name != '0':
        await db.fetch(f"UPDATE all_users SET middle_name=$1 WHERE user_id=$2;",
                       midl_name, user_id)
    if lang != '0':
        await db.fetch(f"UPDATE all_users SET lang=$1 WHERE user_id=$2;",
                       lang, user_id)
    if image_link != '0':
        await db.fetch(f"UPDATE all_users SET image_link=$1 WHERE user_id=$2;",
                       image_link, user_id)

    if image_link_little != '0':
        await db.fetch(f"UPDATE all_users SET image_link_little=$1 WHERE user_id=$2;",
                       image_link_little, user_id)
    if push != '0':
        await db.fetch(f"UPDATE all_users SET push=$1 WHERE user_id=$2;",
                       push, user_id)
    return user_id


# Обновляем данные в комюнити
async def update_community(db: Depends, community_id: int, name: str, open_profile: bool,
                           send_media: bool, send_voice: bool, moder_create_chat: bool):
    data = await db.fetch(f"UPDATE community SET name=$1, open_profile=$2, send_media=$3, "
                          f"send_voice=$4, moder_create_chat=$5 WHERE community_id=$6;",
                          name, open_profile, send_media, send_voice, moder_create_chat, community_id)
    return data


# Обновляем информацию
async def update_data(db: Depends, table: str, name: str, id_data, data, id_name: str = 'id'):
    await db.execute(f"UPDATE {table} SET {name}=$1 WHERE {id_name}=$2;",
                     data, id_data)


# Обновляем информацию
async def update_users_chat_push(db: Depends, chat_id: int, user_id: int):
    await db.execute(f"UPDATE users_chat SET push_sent=$1 WHERE chat_id=$2 AND user_id=$3;",
                     True, chat_id, user_id)


# Обновляем информацию
async def clear_users_chat_push(db: Depends, user_id: int):
    await db.execute(f"UPDATE users_chat SET push_sent=$1 WHERE user_id=$2;",
                     False, user_id)


# Обновляем информацию
async def update_user_active(db: Depends, user_id: int):
    now = datetime.datetime.now()
    await db.fetch(f"UPDATE all_users SET last_active=$1 WHERE user_id=$2;",
                   int(time.mktime(now.timetuple())), user_id)


# Обновляем информацию
async def update_password(db: Depends, user_id: int, password_hash: str):
    await db.fetch(f"UPDATE all_users SET password_hash=$1 WHERE user_id=$2;",
                   password_hash, user_id)


# Удаляем токены
async def delete_old_tokens(db: Depends):
    now = datetime.datetime.now()
    await db.execute(f"DELETE FROM token WHERE death_date < $1", now)


# Удаляем токены
async def delete_all_tokens(db: Depends, user_id: int):
    await db.execute(f"DELETE FROM token WHERE user_id = $1", user_id)


# Удаляем все сообщения
async def delete_all_messages(db: Depends, chat_id: int):
    await db.execute(f"DELETE FROM messages WHERE chat_id = $1", chat_id)


# Удаляем все записи из таблицы по ключу
async def delete_where(db: Depends, table: str, id_name: str, data):
    await db.execute(f"DELETE FROM {table} WHERE {id_name} = $1", data)


# Удаляем все записи из таблицы
async def delete_from_table(db: Depends, table: str):
    await db.execute(f"DELETE FROM {table};")
