import json
import random

import gen
from structure import QuizContent

words = []
quizs = []


def generate() -> None:
    with open("word(win).txt", "r", encoding="utf8") as file:
        for line in file:
            formated = line.rstrip()
            words.append(formated.split('|'))

    for pars in words:
        word = pars[0]
        comment = None
        if len(pars) > 1:
            comment = pars[1]
        variants = list(gen.get_vars(word))
        pos = 0
        for j, i in enumerate(variants):
            if i == word:
                pos = j
        quizs.append(QuizContent(correct_variant=pos, variants=variants, comment=comment))


def make_content():
    words.clear()
    generate()
    random.shuffle(quizs)
    with open("polls.json", "w") as file:
        json.dump([dict(obj) for obj in quizs], file)


def load_content() -> list[QuizContent]:
    with open("polls.json", "r") as file:
        json_list = json.load(file)
        res_list = [QuizContent(**obj) for obj in json_list]
        return res_list
