get_me_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'user': {}}
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
                        "value": 'bad access token'
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
                                  'access_token': 'fFsok0mod3y5mgoe203odk3f'}
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
                        "value": 'bad refresh token, please login'
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
                        "value": {"ok": True, 'desc': 'no phone in database'}
                    },
                }
            }
        }
    },
    226: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": 'have user with same phone'
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
                                  'user_id': 1,
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

update_user_status_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'desc': 'users status updated'}
                    },
                }
            }
        }
    },
}

update_user_profession_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'description': 'users work list updated'}
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

update_pass_res = {
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
                        "value": "bad phone or password"
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

new_msg_created_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True, 'desc': 'New message was created successfully.'}
                    },
                }
            }
        }
    },
}

get_msg_list_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "count": 1,
                            "msg_list": [
                                {
                                    "id": 1,
                                    "msg_id": 0,
                                    "msg_type": "text",
                                    "title": "Test Title",
                                    "text": "text",
                                    "description": "0",
                                    "lang": "en",
                                    "from_user": 2,
                                    "to_user": 2,
                                    "status": "created",
                                    "user_type": "user",
                                    "read_date": "None",
                                    "deleted_date": "None",
                                    "create_date": "2023-04-24 11:17:13.655705"
                                }
                            ]
                        }
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

create_get_order_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {"ok": True,
                                  'from_user': "{user object here}",
                                  "admin_comments": ["{message object here}","{message object here}"],
                                  'order': {
                                      "ok": True,
                                      "order": {
                                          "order_id": 12,
                                          "creator_id": 14,
                                          "worker_id": 345,
                                          "address": {
                                              "city": "Minsk",
                                              "street": "Mosprospect",
                                              "house": "1 2",
                                              "latitudes": 21.323,
                                              "longitudes": 32.344
                                          },
                                          "object_type_id": 1,
                                          "object_name_ru": "Убираю квартиры",
                                          "object_name_en": "I clean apartments",
                                          "object_name_he": "I clean apartments",
                                          "object_size": 1,
                                          "comment": "Hack world",
                                          "status": "created",
                                          "review": {
                                              "order_id": 20,
                                              "worker_id": 0,
                                              "review_text": "0",
                                              "score": 0,
                                              "review_status": "created",
                                              "review_date": "None"
                                          },
                                          "start_work": "2023-11-27 14:35:45",
                                          "create_date": "2023-05-17 12:42:53.153262"
                                      }
                                  }}
                    },
                }
            }
        }
    },
}

get_all_order_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "orders_in_deal": [
                                1,

                            ],
                            "orders": [
                                {
                                    "order_id": 1,
                                    "creator_id": 1,
                                    "worker_id": 1,
                                    "address": {
                                        "city": "Минск ",
                                        "street": "брикеля ",
                                        "house": "12",
                                        "latitudes": 23.847127,
                                        "longitudes": 53.699845
                                    },
                                    "object_type_id": 1,
                                    "object_name_ru": "Убираю квартиры",
                                    "object_name_en": "I clean apartments",
                                    "object_name_he": "I clean apartments",
                                    "object_size": 1,
                                    "comment": "помыть пол ",
                                    "status": "created",
                                    "review": {
                                        "order_id": 1,
                                        "worker_id": 0,
                                        "review_text": "0",
                                        "score": 0,
                                        "review_status": "created",
                                        "review_date": "None"
                                    },
                                    "start_work": "2023-05-18 09:04:00",
                                    "status_date": "None",
                                    "create_date": "2023-05-18 15:07:07.185038"
                                }
                            ]
                        }
                    },
                }
            }
        }
    },
}

delete_order_res = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "odd": {
                        "summary": "Success",
                        "value": {
                            "ok": True,
                            "description": 'The order was successfully deleted.'
                        }
                    },
                }
            }
        }
    },
}
