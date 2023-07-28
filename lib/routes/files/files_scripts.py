import os

ip_server = os.environ.get("IP_SERVER")
ip_port = os.environ.get("PORT_SERVER")

ip_port = 80 if ip_port is None else ip_port
ip_server = "127.0.0.1" if ip_server is None else ip_server


def create_file_json(file) -> dict:
    resp = {'ok': True,
            'file_id': file['id'],
            'file_name': file['file_name'],
            'file_type': file['file_type'],
            'creator_id': file['owner_id'],
            'file_size': file['file_size'],
            'client_file_id': file['client_file_id'],
            'url': f"http://{ip_server}:{ip_port}/file_download?file_id={file['id']}",
            }

    little_id = file['little_file_id']
    middle_id = file['middle_file_id']

    if little_id != 0:
        if file['file_type'] == 'video':
            resp['screen_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={little_id}"
        else:
            resp['little_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={little_id}"

    if middle_id != 0:
        resp['middle_url'] = f"http://{ip_server}:{ip_port}/file_download?file_id={middle_id}"
    return resp
