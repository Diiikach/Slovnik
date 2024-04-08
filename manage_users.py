import os
import json
from random import randint

from manage_content import load_content
from structure import User, Quizs, Quiz

content = load_content()

if not os.path.exists(os.path.join(os.getcwd(), "quizs.json")):
    path = os.path.join(os.getcwd(), "quizs.json")
    with open(path, 'w', encoding="utf8") as file:
        json.dump(dict(Quizs(quizs=dict())), file)


def initialize_user(user_id: str):
    path = os.path.join(os.getcwd(), user_id, "info.json")
    with open(path, "w", encoding="utf8") as file:
        last_used = [0 for _ in range(len(content))]
        user = User(cnt=0, last_used=last_used)
        print(user)
        json.dump(dict(user), file)


def get_user_info(user_id: str):
    path = os.path.join(os.getcwd(), user_id, "info.json")
    with open(path, "r", encoding="utf8") as file:
        return User(**json.load(file))


def update_user(user_id: str, user: User):
    path = os.path.join(os.getcwd(), user_id, "info.json")
    with open(path, "w", encoding="utf8") as file:
        json.dump(dict(user), file)


def get_quizs():
    path = os.path.join(os.getcwd(), "quizs.json")
    with open(path, "r", encoding="utf8") as file:
        return Quizs.model_validate_json(file.read())


def update_quizs(opened: Quizs):
    path = os.path.join(os.getcwd(), "quizs.json")
    with open(path, 'w', encoding="utf8") as file:
        file.write(opened.model_dump_json())

def add_quiz(user_id: str, quiz_id: str, pos: int):
    quizs = get_quizs()
    quizs.quizs[quiz_id] = Quiz(user=user_id, pos=pos)
    update_quizs(quizs)

def check_quiz(user_id: str, quiz_id):
    quizs = get_quizs()
    print(quizs)
    res = quizs.quizs[quiz_id]
    if res.user == user_id:
        quizs.quizs.pop(quiz_id, None)
        update_quizs(quizs)
        return res
    else:
        return False


def check_user(user_id: str) -> None:
    if os.path.exists(os.path.join(os.getcwd(), user_id)):
        return
    os.mkdir(os.path.join(os.getcwd(), user_id))
    initialize_user(user_id)


def get_quiz(user_id: str):
    info = get_user_info(user_id)
    pos = 0
    for i in range(len(content)):
        if info.last_used[i] < info.last_used[pos]:
            pos = i
    info.last_used[pos] = info.cnt
    info.cnt += 1
    update_user(user_id=user_id, user=info)
    return pos