import os

import starlette.status as _status
from PIL import Image
from fastapi import Depends
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from lib import sql_connect as conn
from lib.response_examples import *
from lib.routes.files.files_scripts import create_file_json
from lib.sql_connect import data_b, app

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


@app.get(path='/file_download', tags=['For all'])
async def download_file(file_id: int, db=Depends(data_b.connection), ):
    """Here you download file by id"""
    file = await conn.read_data(db=db, table='files', id_name='id', id_data=file_id, name='*')
    if not file:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={'desc': 'bad file id'})
    file_path = file[0]['file_path']
    return FileResponse(path=file_path, media_type='multipart/form-data', filename=file[0]['file_name'])


@app.get(path='/file', tags=['For all'], responses=create_file_res)
async def get_file_links_name_and_other(file_id: int, db=Depends(data_b.connection), ):
    """Get all information about file by file_id"""
    file = await conn.read_data(db=db, table='files', id_name='id', id_data=file_id, name='*')
    if not file:
        return JSONResponse(status_code=_status.HTTP_400_BAD_REQUEST,
                            content={'desc': 'bad file id'})

    resp = create_file_json(file[0])

    return JSONResponse(content=resp,
                        headers={'content-type': 'application/json; charset=utf-8'})


@app.post(path='/file_upload', tags=['For all'], responses=create_file_res)
async def upload_file(file: UploadFile, access_token: str = '0', msg_id: int = 0,
                      client_file_id: int = 0, db=Depends(data_b.connection), ):
    """
    Upload file to server\n
    file_type in response:
    .jpg and .jpeg is image,\n
    .xlsx and .doc is ms_doc,\n
    .mp4  is video,\n
    other files get type file\n
    msg_id: if file attached to message with msg_id
    """

    user_id = (await conn.get_token(db=db, token_type='access', token=access_token))
    if not user_id:
        user_id = 0
    else:
        user_id = user_id[0][0]
    if (file.filename.split('.')[-1]).lower() == 'jpg' or (file.filename.split('.')[-1]).lower() == 'jpeg':
        file_path = f'files/img/'
        file_type = 'image'
    elif file.filename.split('.')[1] == 'xlsx' or file.filename.split('.')[1] == 'doc':
        file_path = f'files/ms_doc/'
        file_type = 'ms_doc'
    # elif file.filename.split('.')[1] == 'txt' or file.filename.split('.')[1] == 'pdf':
    #     file_path = f'files/docs/'
    #     file_type = 'document'
    elif file.filename.split('.')[1] == 'mp4':
        file_path = f'files/video/'
        file_type = 'video'
    else:
        file_path = f'files/file/'
        file_type = 'file'
    file_data = (await conn.save_new_file(db=db, file_name=file.filename, file_path=file_path, owner_id=user_id,
                                          file_type=file_type, file_size=file.size, client_file_id=client_file_id))[0]
    file_id = file_data[0]

    filename = f"{file_id}.{file.filename.split('.')[1]}"
    await conn.update_data(table='files', name='file_path', data=f"{file_path}{filename}", id_data=file_id, db=db)
    b = file.file.read()

    f = open(f"{file_path}{filename}", 'wb')
    f.write(b)
    f.close()

    resp = {'ok': True,
            'file_id': file_data['id'],
            'file_name': file_data['file_name'],
            'file_type': file_data['file_type'],
            'creator_id': file_data['owner_id'],
            'file_size': file_data['file_size'],
            'client_file_id': file_data['client_file_id'],
            'url': f"http://{ip_server}:{ip_port}/file_download?file_id={file_id}",
            }
    if file_type == 'image':
        middle_file_id = await save_resize_img(db=db, file=file, file_path=file_path, file_type=file_type,
                                               user_id=user_id, file_id=file_id, filename=filename, size=3)

        small_file_id = await save_resize_img(db=db, file=file, file_path=file_path, file_type=file_type,
                                              user_id=user_id, file_id=file_id, filename=filename, )
        if middle_file_id != 0:
            resp['middle_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={middle_file_id}"
        if small_file_id != 0:
            resp['little_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={small_file_id}"

    if file_type == 'video':
        screen_id = await save_video_screen(db=db, file=file, user_id=user_id, file_id=file_id, filename=filename)
        resp['screen_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={screen_id}"

    if msg_id != 0 and user_id != 0:
        await conn.update_data(table='messages', name='file_id', data=file_id, id_name='msg_id', id_data=msg_id, db=db)
        await conn.update_data(table='messages', name='status', data='not_read', id_name='msg_id',
                               id_data=msg_id, db=db)

    return JSONResponse(content=resp,
                        headers={'content-type': 'application/json; charset=utf-8'})


async def save_resize_img(db: Depends, file: UploadFile, file_path: str, file_type: str, user_id: int, file_id: int,
                          filename: str, size: int = 1):
    small_file_id = (await conn.save_new_file(db=db, file_name=file.filename, file_path=file_path, owner_id=user_id,
                                              file_type=file_type, file_size=0, client_file_id=0))[0][0]
    small_filename = f"{small_file_id}.{file.filename.split('.')[1]}"
    await conn.update_data(table='files', name='file_path', data=f"{file_path}{small_filename}",
                           id_data=small_file_id, db=db)
    await conn.update_data(table='files', name='little_file_id' if size == 1 else 'middle_file_id', data=small_file_id,
                           id_data=file_id, db=db)

    image = Image.open(f"{file_path}{filename}")
    width, height = image.size
    coefficient = height / 100
    new_width = (width / coefficient) * size
    try:
        resized_image = image.resize((int(new_width), 100 * size))
        resized_image.save(f"{file_path}{small_filename}")
    except Exception as ex:
        print(ex)
        await conn.delete_where(table='files', id_name='id', data=small_file_id, db=db)
        await conn.update_data(table='files', name='little_file_id' if size == 1 else 'middle_file_id',
                               data=0,
                               id_data=file_id, db=db)
        small_file_id = 0
    return small_file_id


async def save_video_screen(db: Depends, file: UploadFile, user_id: int, file_id: int,
                            filename: str):
    from moviepy.editor import VideoFileClip

    screen_file_id = (await conn.save_new_file(db=db, file_name=file.filename, file_path='files/img/', owner_id=user_id,
                                               file_type='image', file_size=0, client_file_id=0))[0][0]
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
