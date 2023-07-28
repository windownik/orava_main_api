import os

from fastapi import Depends
from fastapi.responses import JSONResponse

from fastapi import UploadFile
import starlette.status as _status
from lib import sql_connect as conn
from lib.response_examples import *

from lib.sql_connect import data_b, app
from fastapi.responses import FileResponse

from PIL import Image
from moviepy.editor import VideoFileClip

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.get(path='/file_download', tags=['For all'])
async def download_file(file_id: int, db=Depends(data_b.connection), ):
    """Get all company in database"""
    file = await conn.read_data(db=db, table='files', id_name='id', id_data=file_id, name='*')
    if not file:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={'desc': 'bad file id'})
    file_path = file[0]['file_path']
    return FileResponse(path=file_path, media_type='multipart/form-data', filename=file[0]['file_name'])


@app.get(path='/file', tags=['For all'])
async def download_file(file_id: int, db=Depends(data_b.connection), ):
    """Get all company in database"""
    file = await conn.read_data(db=db, table='files', id_name='id', id_data=file_id, name='*')
    if not file:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={'desc': 'bad file id'})

    little_id = file[0]['little_file_id']
    little_file = await conn.read_data(db=db, table='files', id_name='id', id_data=little_id, name='*')
    middle_id = file[0]['middle_file_id']
    resp = {"ok": True,
            'file_type': file[0]['file_type'],
            'url': f"http://{ip_server}:{ip_port}/file_download?file_id={file_id}",
            }

    if little_id != 0:
        resp['little_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={little_file[0][0]}"

    if middle_id != 0:
        resp['middle_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={middle_id}"

    return JSONResponse(content=resp,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.get(path='/files_in_line', tags=['For all'], responses=upload_files_list_res)
async def get_files_by_line(file_id_line: str, db=Depends(data_b.connection)):
    """Get all files in file_id_line\n
    file_id_line - '1,2,3,4,5,6' for one filein line '5'
    """
    files_list = []
    file_line = file_id_line.split(',')
    for file_id in file_line:
        if not file_id.isdigit():
            continue
        file = await conn.read_data(db=db, table='files', id_name='id', id_data=int(file_id), name='*')
        if not file:
            continue
        files_list.append(
            {
                'file_id': file[0]['id'],
                'name': file[0]['file_name'],
                'file_type': file[0]['file_type'],
                'owner_id': file[0]['owner_id'],
                'create_date': str(file[0]['create_date']),
                'url': f"http://{ip_server}:{ip_port}/file_download?file_id={file_id}"
            }
        )
    return JSONResponse(content={"ok": True, 'desc': "all file list by file line", 'files': files_list},
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.post(path='/file_upload', tags=['For all'], responses=upload_files_res)
async def upload_file(file: UploadFile, access_token: str = '0', msg_id: int = 0, db=Depends(data_b.connection), ):
    """
    Upload file to server\n
    file_type in response: .jpg and .png is image,\n
    .xlsx and .doc is ms_doc,\n
    other files get type file\n
    msg_id: if file attached to message with msg_id
    """
    user_id = (await conn.get_token(db=db, token_type='access', token=access_token))
    if not user_id:
        user_id = 0
    else:
        user_id = user_id[0][0]
    if (file.filename.split('.')[1]).lower() == 'jpg' or (file.filename.split('.')[1]).lower() == 'png':
        file_path = f'files/img/'
        file_type = 'image'
    elif file.filename.split('.')[1] == 'xlsx' or file.filename.split('.')[1] == 'doc':
        file_path = f'files/ms_doc/'
        file_type = 'ms_doc'
    elif file.filename.split('.')[1] == 'txt' or file.filename.split('.')[1] == 'pdf':
        file_path = f'files/docs/'
        file_type = 'document'
    elif file.filename.split('.')[1] == 'mp4':
        file_path = f'files/video/'
        file_type = 'video'
    else:
        file_path = f'files/file/'
        file_type = 'file'
    file_id = (await conn.save_new_file(db=db, file_name=file.filename, file_path=file_path, owner_id=user_id,
                                        file_type=file_type))[0][0]
    filename = f"{file_id}.{file.filename.split('.')[1]}"
    await conn.update_data(table='files', name='file_path', data=f"{file_path}{filename}",
                           id_data=file_id, db=db)
    b = file.file.read()

    f = open(f"{file_path}{filename}", 'wb')
    f.write(b)
    f.close()
    if msg_id != 0 and user_id != 0:
        await conn.update_data(table='messages', name='file_id', data=file_id, id_name='msg_id', id_data=msg_id, db=db)

    if file_type == 'image':
        middle_file_id = await save_resize_img(db=db, file=file, file_path=file_path, file_type=file_type,
                                               user_id=user_id, file_id=file_id, filename=filename, size=2)

        small_file_id = await save_resize_img(db=db, file=file, file_path=file_path, file_type=file_type,
                                              user_id=user_id, file_id=file_id, filename=filename, )

        return JSONResponse(content={'ok': True,
                                     'creator_id': user_id,
                                     'file_name': file.filename,
                                     'file_type': file_type,
                                     'file_id': file_id,
                                     'url': f"http://{ip_server}:{ip_port}/file_download?file_id={file_id}",
                                     'middle_url': f"http://{ip_server}:{ip_port}/file_download?file_id={middle_file_id}",
                                     'little_url': f"http://{ip_server}:{ip_port}/file_download?file_id={small_file_id}"
                                     },
                            headers={'content-type': 'application/json; charset=utf-8'})

    elif file_type == 'video':

        screen_id = await save_video_screen(db=db, file=file, user_id=user_id, file_id=file_id, filename=filename)

        return JSONResponse(content={'ok': True,
                                     'creator_id': user_id,
                                     'file_name': file.filename,
                                     'file_type': file_type,
                                     'file_id': file_id,
                                     'video_url': f"http://{ip_server}:{ip_port}/file_download?file_id={file_id}",
                                     'screen_url': f"http://{ip_server}:{ip_port}/file_download?file_id={screen_id}"
                                     },
                            headers={'content-type': 'application/json; charset=utf-8'})

    return JSONResponse(content={'ok': True,
                                 'creator_id': user_id,
                                 'file_name': file.filename,
                                 'file_type': file_type,
                                 'file_id': file_id,
                                 'url': f"http://{ip_server}:{ip_port}/file_download?file_id={file_id}",
                                 },
                        headers={'content-type': 'application/json; charset=utf-8'})


async def save_resize_img(db: Depends, file: UploadFile, file_path: str, file_type: str, user_id: int, file_id: int,
                          filename: str, size: int = 1):
    small_file_id = (await conn.save_new_file(db=db, file_name=file.filename, file_path=file_path, owner_id=user_id,
                                              file_type=file_type))[0][0]
    small_filename = f"{small_file_id}.{file.filename.split('.')[1]}"
    await conn.update_data(table='files', name='file_path', data=f"{file_path}{small_filename}",
                           id_data=small_file_id, db=db)
    await conn.update_data(table='files', name='little_file_id', data=small_file_id,
                           id_data=file_id, db=db)

    image = Image.open(f"{file_path}{filename}")
    width, height = image.size
    coefficient = height / 100
    new_width = (width / coefficient) * size

    resized_image = image.resize((int(new_width), 100 * size))
    resized_image.save(f"{file_path}{small_filename}")
    return small_file_id


async def save_video_screen(db: Depends, file: UploadFile, user_id: int, file_id: int,
                            filename: str):
    screen_file_id = (await conn.save_new_file(db=db, file_name=file.filename, file_path='files/img/', owner_id=user_id,
                                               file_type='image'))[0][0]
    small_filename = f"{screen_file_id}.jpg"
    await conn.update_data(table='files', name='file_path', data=f"files/img/{small_filename}",
                           id_data=screen_file_id, db=db)

    await conn.update_data(table='files', name='file_name', data=small_filename,
                           id_data=screen_file_id, db=db)

    await conn.update_data(table='files', name='little_file_id', data=screen_file_id,
                           id_data=file_id, db=db)

    # Загрузите видео с помощью moviepy
    video = VideoFileClip(f"files/video/{filename}")
    if video.duration < 5:
        screenshot_time = 0
    else:
        screenshot_time = video.duration / 5

    # Получите кадр на определенной секунде времени
    frame = video.get_frame(screenshot_time)

    # Создайте изображение с помощью Pillow из кадра
    image = Image.fromarray(frame)
    image.save(f"files/img/{small_filename}")
    print(small_filename)
    video.reader.close()
    video.audio.reader.close_proc()

    return screen_file_id
