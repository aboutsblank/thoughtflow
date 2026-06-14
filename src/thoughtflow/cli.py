import argparse
import dataclasses as dc
import functools as ft
import json
import os
import tomllib
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# APP_NAME <category> (-l|-g) "..."
# workflow idea -g "Das ist eine globale Idee"
# workflow idea (-l|--local) "Das ist eine lokale Idee"
# workflow idea (-g|--global) "Das ist eine globale Idee"

# alias idea=$(workflow idea $*)
# alias problem=$(workflow problem $*)

# inside of workflow.main you could then do things differently based on the arguments


# GLOBALS
APP_NAME: str = "thoughtflow"
AUTHOR: str = "aboutsblank"

PYPROJECT_NAME: str = "pyproject.toml"
OPTIONS_NAME: str = "options.toml"


class Scope(Enum):
    LOCAL = 0
    GLOBAL = 1


@dc.dataclass
class AppSettings:

    usecase: str = "UNDEF"
    scope: Scope = Scope.LOCAL
    verbosity: bool = False


@dc.dataclass
class Element:

    date: datetime
    msg: str
    author: str


@ft.singledispatch
def encode_value(x: Any) -> Any:
    if dc.is_dataclass(x):
        return dc.asdict(x)

    return x


@encode_value.register(datetime)
def _(x: datetime) -> str:
    return x.isoformat()


def serialize(x):
    return json.dumps(x, default=encode_value)


settings: AppSettings
element: Element


def initParser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog=APP_NAME, description="Personal Workflow Helper", epilog="Have a good life"
    )

    # positional arguments
    parser.add_argument("USECASE")
    parser.add_argument("message")

    # value option arguments

    # on/off flag option arguments
    parser.add_argument("-l", "--local", action="store_true")
    parser.add_argument(
        "-g", "--global", action="store_true"
    )  # global is reserverd in python
    parser.add_argument("-v", "--verbose", action="store_true")

    return parser


def parseArgs(parser: argparse.ArgumentParser) -> dict:

    # possible program exit in parse_args()
    args: dict = vars(parser.parse_args())

    isCorrectConfig: bool = True
    error: str = ""

    isCorrectConfig, error = checkConfigCorrectness(args)
    if not isCorrectConfig:
        print("ERROR: {}\nExiting the program".format(error))
        exit(1)

    return args


def checkConfigCorrectness(args: dict) -> tuple[bool, str]:

    if args["local"] and args["global"]:
        return False, "Options local and global can't both be set to true"

    return True, ""


def newSettingsFromArgs(args: dict) -> AppSettings:

    settings: AppSettings = AppSettings()

    if args["local"]:
        settings.scope = Scope.LOCAL
    elif args["global"]:
        settings.scope = Scope.GLOBAL

    settings.usecase = args["USECASE"]
    settings.verbosity = args["verbose"]

    return settings


def initApp() -> tuple[AppSettings, Element]:

    parser = initParser()
    args = parseArgs(parser)

    el: Element = Element(
        msg=args["message"], author=AUTHOR, date=datetime.now()
    )

    return newSettingsFromArgs(args), el


def getLocalPath(recursiveDepth: int = 0) -> Path:

    cwd: Path = Path(os.getcwd())

    for i in range(0, recursiveDepth):
        cwd = cwd.parent
    return cwd


def getGlobalPath() -> Path:

    return Path.home()


def searchAll() -> Path:
    raise NotImplementedError()


def main():

    settings, element = initApp()

    path = getLocalPath()

    if settings.scope == Scope.GLOBAL:
        path = getGlobalPath()

    path = path / ".{}".format(APP_NAME)
    if not Path.exists(path):
        os.mkdir(path)

    path = path / "{}".format(settings.usecase)

    # test if exists and writable
    # if yes open in append mode otherwise error
    with path.open(mode="a+") as file:
        serialized = serialize(element)
        file.write("{}\n".format(serialized))


# def getLastNElements(n, scope)
# list of last n elements from both local&global scope (n adjustable, default)
# list of last n elemnts from global scope (n adjustable, default 10)
# list of last n elements local scope (n adjustable, default 10)

# def getGlobalElements

# def getLocalElements


# settings - view or modify the list of things that can be set
# options - we have set some things already, and give you the option th change them
# preferences - tell us how you prefer this to work
# properties - change one or more properties of this item
# edit - this thing is already in a good state, but you can change it if you like
# configuration - we have defaults, but theyre so barebones you probably want to configure it yourself


def _projectRoot() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / PYPROJECT_NAME).is_file():
            return parent
    raise FileNotFoundError()


@ft.cache
def loadOptions() -> dict:
    fpath: Path = _projectRoot() / OPTIONS_NAME
    with open(fpath, "rb") as f:
        return tomllib.load(f)


# HELPERs for serialization
