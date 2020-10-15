import importlib
import logging
import os
import sys
import textwrap

import pendulum
from aiogram import Dispatcher, Bot, types
from loguru import logger

import config
import handlers
from src.data import ScheduleData
from utils.logging import InterceptHandler

dp = Dispatcher()
dp.include_router(handlers.schedule.router)


@dp.message(commands=["start"])
async def start(msg: types.Message):
    text = f"""
            ***Привет, {msg.from_user.full_name}!***

            Список доступных команд:
             - /schedule [день недели] — узнать расписание
            """

    await msg.answer(textwrap.dedent(text))


def main():
    try:
        uvloop = importlib.import_module("uvloop")
        uvloop.install()
        logger.info("uvloop package was found, using it as a loop policy.")
    except ModuleNotFoundError:
        logger.warning("Couldn't find uvloop package, using default loop policy.")

    bot = Bot(config.TOKEN, parse_mode="markdown")
    dp.run_polling(bot)


def setup_logging():
    l = logging.getLogger()
    l.setLevel(os.environ.get("LOGGING_LEVEL", "INFO"))
    l.handlers = [InterceptHandler()]

    logger.remove()
    logger.add(sys.stderr, enqueue=True)


if __name__ == "__main__":
    setup_logging()
    pendulum.set_locale("ru")
    pendulum.set_local_timezone(config.TIMEZONE)
    ScheduleData.setup_data()
    main()
