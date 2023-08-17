get_me_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "user": {
                                "user_id": 1,
                                "name": "Nik",
                                "middle_name": "0",
                                "surname": "Ivanov",
                                "phone": 375123456,
                                "email": "0",
                                "image_link": "http://jfnskjf",
                                "image_link_little": "http://sdfsfsdf",
                                "description": "0",
                                "lang": "ru",
                                "status": "active",
                                "last_active": 1688890372,
                                "create_date": 1688890372
                            }

                        }
                    },
                }
            }
        }
    },
    401: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": False,
                                  'description': 'Bad auth_id or access_token'}
                    },
                }
            }
        }
    },
}

get_users_by_contact_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  "user_list": ["user_object", "user_object", "user_object"],
                                  "phones_list": [43543543, 54363642345, 645746]
                                  }
                    },
                }
            }
        }
    },
    401: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": False,
                                  'description': 'Bad auth_id or access_token'}
                    },
                }
            }
        }
    },
}

check_sms_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'description': 'Confirm phone number', }
                    },
                }
            }
        }
    },
    400: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": False,
                            'description': 'SMS code not confirm'
                        }
                    },
                }
            }
        }
    },
}

check_email_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'description': 'This email is not in database', }
                    },
                }
            }
        }
    },
    400: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": False,
                            'description': 'This email is in database',
                        }
                    },
                }
            }
        }
    },
}

check_phone_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'description': 'This phone is not in database', }
                    },
                }
            }
        }
    },
    400: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": False,
                            'description': 'This phone is in database',
                        }
                    },
                }
            }
        }
    },
}

send_sms_code_to_phone_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'description': 'Code for phone created'}
                    },
                }
            }
        }
    },
}

access_token_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'user_id': 12,
                                  'access_token': 'fFsok0mod3y5mgoe203odk3f',
                                  'refresh_token': 'e45wfknwfooii3n43948unf3n932k'}
                    },
                }
            }
        }
    },
    401: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": False,
                                  'description': 'bad refresh token, please login'}
                    },
                }
            }
        }
    },
}

create_user_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'user': {
                                      "user_id": 1,
                                      "name": "Nik",
                                      "middle_name": "0",
                                      "surname": "Ivanov",
                                      "phone": 375123456,
                                      "email": "0",
                                      "image_link": "jfnskjf",
                                      "image_link_little": "sdfsfsdf",
                                      "description": "0",
                                      "lang": "ru",
                                      "status": "active",
                                      "last_active": 1688890372,
                                      "create_date": 1688890372
                                  },
                                  'access_token': '123',
                                  'refresh_token': '123'}
                    },
                }
            }
        }
    },
}

create_community_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "main_chat": {
                                "chat_id": 8,
                                "owner_user": {
                                    "user_id": 1,
                                    "name": "Nik",
                                    "middle_name": "0",
                                    "surname": "Ivanov",
                                    "phone": 375123456,
                                    "email": "0",
                                    "image_link": "jfnskjf",
                                    "image_link_little": "sdfsfsdf",
                                    "description": "0",
                                    "lang": "ru",
                                    "status": "active",
                                    "last_active": 1688890372,
                                    "create_date": 1688890372
                                },
                                "all_users_count": 1,
                                "all_users": [
                                    {
                                        "user_id": 1,
                                        "name": "Nik",
                                        "middle_name": "0",
                                        "surname": "Ivanov",
                                        "phone": 375123456,
                                        "email": "0",
                                        "image_link": "jfnskjf",
                                        "image_link_little": "sdfsfsdf",
                                        "description": "0",
                                        "lang": "ru",
                                        "status": "active",
                                        "last_active": 1688890372,
                                        "create_date": 1688890372
                                    }
                                ],
                                "community_id": 0,
                                "name": "Chat with owner",
                                "img_url": "0",
                                "little_img_url": "0",
                                "chat_type": "main_chat",
                                "status": "create",
                                "open_profile": True,
                                "send_media": True,
                                "send_voice": True,
                                "deleted_date": 0,
                                "create_date": 1690962201,
                                "unread_message": [],
                                "unread_count": 0
                            },
                            "community": {
                                "community_id": 5,
                                "owner_id": 1,
                                "name": "Super comunity",
                                "main_chat_id": 8,
                                "join_code": "3czmfs",
                                "img_url": "0",
                                "little_img_url": "0",
                                "status": "create",
                                "open_profile": True,
                                "send_media": True,
                                "send_voice": True,
                                "moder_create_chat": True,
                                "deleted_date": 0,
                                "create_date": 1690962201
                            }
                        }
                    },
                }
            }
        }
    },
}


create_event_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "event": {
                                "community_id": 5,
                                "owner_id": 1,
                                "name": "Super comunity",
                                "main_chat_id": 8,
                                "join_code": "3czmfs",
                                "img_url": "0",
                                "little_img_url": "0",
                                "status": "create",
                                "open_profile": True,
                                "send_media": True,
                                "send_voice": True,
                                "moder_create_chat": True,
                                "deleted_date": 0,
                                "create_date": 1690962201
                            }
                        }
                    },
                }
            }
        }
    },
}

delete_event_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "description": "Event successful deleted"
                        }
                    },
                }
            }
        }
    },
}

create_chat_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'user': {
                                      "user_id": 1,
                                      "name": "Nik",
                                      "middle_name": "0",
                                      "surname": "Ivanov",
                                      "phone": 375123456,
                                      "email": "0",
                                      "image_link": "jfnskjf",
                                      "image_link_little": "sdfsfsdf",
                                      "description": "0",
                                      "lang": "ru",
                                      "status": "active",
                                      "last_active": 1688890372,
                                      "create_date": 1688890372
                                  },
                                  'access_token': '123',
                                  'refresh_token': '123'}
                    },
                }
            }
        }
    },
}

update_user_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'desc': 'all users information updated'}
                    },
                }
            }
        }
    },
}

delete_user_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'desc': 'all users information deleted'}
                    },
                }
            }
        }
    },
}

get_user_profession_list_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'users_work_list': [
                                      {
                                          "work_id": 1,
                                          "work_type": "clean",
                                          "object_id": 1,
                                          "object_name_ru": "Квартира",
                                          "object_name_en": "Apartment",
                                          "object_name_he": "דִירָה",
                                          "object_size": 1
                                      }

                                  ]
                                  }
                    },
                }
            }
        }
    },
}

login_get_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'desc': 'all users information updated'}
                    },
                }
            }
        }
    },
    401: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": False,
                                  'description': 'Bad auth_id or access_token'}
                    },
                }
            }
        }
    },
}

upload_files_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value":
                            {'ok': True,
                             'creator_id': 3,
                             'file_name': '12.jpg',
                             'file_type': 'image',
                             'file_id': 12,
                             'url': f"http://127.0.0.1:80/file_download?file_id=12"}
                    }
                },
            }
        }
    }
}

create_file_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value":
                            {'ok': True,
                             'desc': "all file list by file line",
                             'files': [{
                                 'file_id': 22,
                                 'name': '12.jpg',
                                 'file_type': 'image',
                                 'owner_id': 12,
                                 'create_date': '2023-01-17 21:54:23.738397',
                                 'url': f"http://127.0.0.1:80/file_download?file_id=12"
                             }]}
                    }
                },
            }
        }
    }
}

upload_files_list_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value":
                            {'ok': True,
                             'desc': "all file list by file line",
                             'files': [{
                                 'file_id': 22,
                                 'name': '12.jpg',
                                 'file_type': 'image',
                                 'owner_id': 12,
                                 'create_date': '2023-01-17 21:54:23.738397',
                                 'url': f"http://127.0.0.1:80/file_download?file_id=12"
                             }]}
                    }
                },
            }
        }
    }
}

get_object_list_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'object_types': [{
                                      "id": 1,
                                      "name_ru": "Квартира",
                                      "name_en": "Apartment",
                                      "name_heb": "דִירָה"
                                  }]
                                  }
                    },
                }
            }
        }
    },
}

update_push_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {'ok': True, 'desc': 'successfully updated'}
                    },
                }
            }
        }
    },
}

send_push_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {'ok': True, 'desc': 'successful send push'}
                    },
                }
            }
        }
    },
}

create_dialog_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "dialog": {
                                "msg_chat_id": 1,
                                "owner_status": "active",
                                "to_status": "active",
                                "create_date": 1688889141,
                                "owner": {
                                    "user_id": 1,
                                    "name": "Nik",
                                    "middle_name": "0",
                                    "surname": "Mislivets",
                                    "phone": 123456789,
                                    "email": "0",
                                    "image_link": "http://127.0.0.1:10020/file_download?file_id=15",
                                    "image_link_little": "http://127.0.0.1:10020/file_download?file_id=16",
                                    "description": "0",
                                    "lang": "en",
                                    "status": "active",
                                    "push": "0",
                                    "last_active": 1688878732,
                                    "create_date": 1688878732
                                },
                                "user_to": {
                                    "user_id": 2,
                                    "name": "Helen",
                                    "middle_name": "0",
                                    "surname": "Kryvetskaya",
                                    "phone": 1237328399,
                                    "email": "0",
                                    "image_link": "http://127.0.0.1:10020/file_download?file_id=7",
                                    "image_link_little": "http://127.0.0.1:10020/file_download?file_id=8",
                                    "description": "0",
                                    "lang": "ru",
                                    "status": "active",
                                    "push": "0",
                                    "last_active": 1688888732,
                                    "create_date": 1688888732
                                }
                            }
                        }
                    },
                }
            }
        }
    },
}

delete_dialog_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  "description": 'dialog and all messages was deleted'}
                    },
                }
            }
        }
    },
    400: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": False,
                                  'description': "not enough rights", }
                    },
                }
            }
        }
    },
    401: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": False,
                                  'description': "bad access token", }
                    },
                }
            }
        }
    },
}

get_all_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'user': "{user_object}",
                                  "chats": ["{chat_object}", "{chat_object}"],
                                  "community_list": ["{community_object}", "{community_object}"]}
                    },
                }
            }
        }
    },
}

get_msg_by_id_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "message": {
                                "id": 1,
                                "msg_id": 0,
                                "msg_type": "text",
                                "title": "Test Title",
                                "text": "text",
                                "description": "0",
                                "lang": "en",
                                "from_user": {
                                    "user_id": 2,
                                    "phone": 37529821,
                                    "email": "windownik@gmail.com",
                                    "image_link": "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=6116895105070527&width=200&ext=1684829559&hash=AeQ4MUkYJgAP4GeFRx8",
                                    "name": "Никита Мисливец",
                                    "auth_type": "fb",
                                    "auth_id": 6116895105070527,
                                    "description": "Nothing about me\n",
                                    "lang": "en",
                                    "status": "admin",
                                    "score": 5,
                                    "score_count": 0,
                                    "total_score": 0,
                                    "address": {
                                        "city": "Paris",
                                        "street": "San Marino ",
                                        "house": "1",
                                        "latitudes": 53.6878483,
                                        "longitudes": 53.6878483
                                    },
                                    "last_active": "2023-04-23 13:29:29.788615",
                                    "create_date": "2023-04-23 12:30:39.470459"
                                },
                                "to_user": {
                                    "user_id": 2,
                                    "phone": 37529821,
                                    "email": "windownik@gmail.com",
                                    "image_link": "https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=6116895105070527&width=200&ext=1684829559&hash=AeQ4MUkYJgAP4GeFRx8",
                                    "name": "Никита Мисливец",
                                    "auth_type": "fb",
                                    "auth_id": 6116895105070527,
                                    "description": "Nothing about me\n",
                                    "lang": "en",
                                    "status": "admin",
                                    "score": 5,
                                    "score_count": 0,
                                    "total_score": 0,
                                    "address": {
                                        "city": "Paris",
                                        "street": "San Marino ",
                                        "house": "1",
                                        "latitudes": 53.6878483,
                                        "longitudes": 53.6878483
                                    },
                                    "last_active": "2023-04-23 13:29:29.788615",
                                    "create_date": "2023-04-23 12:30:39.470459"
                                },
                                "status": "created",
                                "user_type": "user",
                                "read_date": "None",
                                "deleted_date": "None",
                                "create_date": "2023-04-24 11:17:13.655705"
                            }
                        }
                    },
                }
            }
        }
    },
}
