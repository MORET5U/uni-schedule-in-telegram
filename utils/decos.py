from functools import wraps
from typing import Coroutine, Callable, Any

import pendulum
from aiogram import types

import config

cooldowns = {}


def cooldown(**kwargs):
    """Декоратор для анти-флуда"""
    def wrapper(func: Callable[..., Coroutine[Any, Any, Any]]):
        @wraps(func)
        async def wrapped(msg: types.Message):
            rate = kwargs.get("rate", 1)
            timestamp = pendulum.now(config.TIMEZONE).float_timestamp

            author_id = msg.from_user.id if msg.from_user is not None else -1
            current_cooldown = cooldowns.get(f"{author_id}_{func.__name__}", 0)

            if timestamp >= current_cooldown:
                is_success = await func(msg)
                if is_success:
                    cooldowns.update({f"{author_id}_{func.__name__}": timestamp + rate})
            else:
                difference = round(timestamp - current_cooldown, 2)
                await msg.answer(
                    f"❌ Не флудите! Попробуйте ещё раз через {difference * -1 if difference < 0 else difference} сек."
                )

        return wrapped

    return wrapper
