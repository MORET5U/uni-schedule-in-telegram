import re
import sys

from aiogram import Router, types
from loguru import logger

from src.data import ScheduleData
from src.entities import WeekType, UnitTime
from utils.decos import cooldown

DAYS_NAMES_REGEX = re.compile(
    r"(?i)сегодня|послезавтра|завтра|пн|понедельник|вт|вторник|ср|среда|чт|четверг|пт|пятница|сб|суббота"
)


router = Router()


@router.message()
@cooldown(rate=1)
async def process_schedule_check(msg: types.Message):
    if found := re.findall(DAYS_NAMES_REGEX, msg.text):
        dt, day_type, week_type = await ScheduleData.get_requested_date(timestr=found[0])
    else:
        return

    if week_type is WeekType.even:
        evenoddstr = "четная"
    else:
        evenoddstr = "нечетная"

    dateinfostr = "{} ({} неделя)".format(dt.format("dddd, D MMMM YYYY г.").capitalize(), evenoddstr)

    schedule = await ScheduleData.get_schedule(week_type)

    try:
        units = schedule[day_type.name]
    except KeyError:
        await msg.answer("❌ Расписание на {0} не найдено.".format(dt.format("D MMMM YYYY г.")))
    else:
        msgfmt = f"{dateinfostr}\n"
        for i, unit in enumerate(units):
            msgfmt += "\n\n{}\n{}. *{}*\n".format(UnitTime(i).label, i + 1, "Окно" if not unit else unit.name)

            if unit:
                msgfmt += f"     {unit.teacher}\n     _{unit.type}_\n"
                if unit.room:
                    if unit.room > 0:
                        msgfmt += f"     ауд. {unit.room}\n"

        logger.debug(f"msgfmt size - {sys.getsizeof(msgfmt)}")

        await msg.answer(msgfmt)
        return True
