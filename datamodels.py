from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Usecase(Enum):
    UNDEF = 0
    IDEA = 1
    TASK = 2
    # ... should not be hard coded (e.g. read from a config file)


class Scope(Enum):
    LOCAL = 0
    GLOBAL = 1


@dataclass
class AppSettings:

    usecase: Usecase = Usecase.UNDEF
    scope: Scope = Scope.LOCAL
    verbosity: bool = False


@dataclass
class Element:

    date: datetime
    msg: str
    author: str
