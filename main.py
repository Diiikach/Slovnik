import asyncio
import logging
import sys

import manage_users

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, PollAnswer

from manage_content import load_content

# Bot token can be obtained via https://t.me/BotFather
TOKEN = ""

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
quizs = load_content()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = str(message.from_user.id)
    manage_users.check_user(user_id)
    quiz_pos = manage_users.get_quiz(user_id)
    quiz = quizs[quiz_pos]
    text = f"Как правильно пишется слово {quiz.variants[quiz.correct_variant].capitalize()}?"
    if quiz.comment is not None:
        text += f"({quiz.comment})"
    res = await bot.send_poll(chat_id=message.from_user.id, question=text,
                        options=quiz.variants,
                        is_anonymous=False, type="quiz", correct_option_id=quiz.correct_variant)
    manage_users.add_quiz(user_id, res.poll.id, quiz_pos)
    print("added")

@dp.poll_answer()
async def echo_handler(poll : PollAnswer) -> None:
    user_id = str(poll.user.id)
    manage_users.check_user(user_id)
    status = manage_users.check_quiz(user_id, poll.poll_id)
    if status is False:
        return
    if poll.option_ids[0] != quizs[status.pos].correct_variant:
        res = await bot.send_poll(chat_id=user_id, question="Попробуйте ещё раз...",
                                  options=quizs[status.pos].variants,
                                  is_anonymous=False, type="quiz", correct_option_id=quizs[status.pos].correct_variant)
        manage_users.add_quiz(user_id, res.poll.id, status.pos)
        return
    quiz_pos = manage_users.get_quiz(user_id)
    quiz = quizs[quiz_pos]
    text = f"Где должно стоять ударение в слове {quiz.variants[quiz.correct_variant].capitalize()}?"
    if quiz.comment is not None:
        text += f"({quiz.comment})"
    res = await bot.send_poll(chat_id=user_id, question=text,
                        options=quiz.variants,
                        is_anonymous=False, type="quiz", correct_option_id=quiz.correct_variant)
    manage_users.add_quiz(user_id, res.poll.id, quiz_pos)

async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
