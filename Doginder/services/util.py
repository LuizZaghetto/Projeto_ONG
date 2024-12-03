import json


def read_json(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def is_present(arg: list, lookup: str | int):
    for item in arg:
        if item.get('user_id') == lookup:
            return True
    return False


def insert_new_user(data, user_id):
    user = {
        'user_id': user_id,
        'liked': [],
        'disliked': []}
    data.append(user)


def insert_in_user_liked(data: list, user_id: int, animal_id: int):
    for item in data:
        if item.get('user_id') == user_id:
            item.get('liked').append(animal_id)


def insert_in_user_disliked(data, user_id, animal_id):
    for item in data:
        if item.get('user_id') == user_id:
            item.get('disliked').append(animal_id)
