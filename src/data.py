from os import path
from typing import Dict, Optional, Tuple, List

import asyncio

import pendulum
import toml
import dateparser
from loguru import logger

from src.entities import DayType, WeekType, Unit

import config


class ScheduleData:
    EVEN_WEEK: Optional[Dict[str, List[Unit]]] = None
    ODD_WEEK: Optional[Dict[str, List[Unit]]] = None

    @classmethod
    def setup_data(cls):
        data = toml.load(path.join(path.dirname(__file__), "../data/even_week.toml"))
        cls.EVEN_WEEK = {k: [Unit(**x) for x in v] for k, v in data.items()}

        data = toml.load(path.join(path.dirname(__file__), "../data/odd_week.toml"))
        cls.ODD_WEEK = {k: [Unit(**x) for x in v] for k, v in data.items()}

        logger.info("Schedule data has been loaded into ScheduleData class")

    @staticmethod
    async def even_or_odd(*, moment: pendulum.DateTime = None) -> WeekType:
        """Определяет чётность недели"""
        moment = moment or pendulum.now()
        _, week_num, _ = moment.isocalendar()
        return WeekType.even if (week_num + config.WEEKS_OFFSET) % 2 == 0 else WeekType.odd

    @staticmethod
    async def get_requested_date(*, timestr: str = None) -> Tuple[pendulum.DateTime, DayType, WeekType]:
        """
        Возвращает кортеж времени, типа дня, типа недели, основываясь на строковом представлении запрошенного времени
        """

        def runner():
            __dt = dateparser.parse(timestr, settings={"PREFER_DATES_FROM": "future"})
            __moment = pendulum.from_timestamp(__dt.timestamp(), tz=config.TIMEZONE)
            __day_type = DayType(__moment.weekday() + 1)
            return __moment, __day_type

        moment, day_type = await asyncio.get_event_loop().run_in_executor(None, runner)
        week_type = await ScheduleData.even_or_odd(moment=moment)

        return moment, day_type, week_type

    @classmethod
    async def get_schedule(cls, wtype: WeekType):
        return cls.EVEN_WEEK if wtype is WeekType.even else cls.ODD_WEEK
