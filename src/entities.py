from enum import Enum


class Unit:
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name")
        self.type = kwargs.get("type")
        self.teacher: str = kwargs.get("teacher")
        self.room: int = kwargs.get("room")
        self.skip = kwargs.get("skip", False)

    def __setattr__(self, key, value):
        if not hasattr(self, key):
            super().__setattr__(key, value)
        else:
            raise AttributeError("'{}' can not be modified.".format(key)) from None

    def __repr__(self):
        items = ("%s=%r" % (k, v) for k, v in self.__dict__.items())
        return "<%s %s>" % (self.__class__.__name__, " ".join(items))

    def __bool__(self):
        return bool(self.name) and bool(self.teacher)


class DayType(Enum):
    Sunday = 7
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6


class WeekType(Enum):
    even = "even"
    odd = "odd"


class UnitTime(bytes, Enum):
    def __new__(cls, value, label):
        obj = bytes.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

    First = (0, "8:00 - 9:30")
    Second = (1, "9:40 - 11:10")
    Third = (2, "11:35 - 13:05")
    Fourth = (3, "13:15 - 14:45")
    Fifth = (4, "15:05 - 16:35")
    Sixth = (5, "16:45 - 18:15")
