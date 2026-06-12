import argparse
import dataclasses
import datetime as dt
import functools
import json
import os
from pathlib import Path
from typing import Any

from datamodels import AppSettings, Element, Scope

# APP_NAME <category> (-l|-g) "..."
# workflow idea -g "Das ist eine globale Idee"
# workflow idea (-l|--local) "Das ist eine lokale Idee"
# workflow idea (-g|--global) "Das ist eine globale Idee"

# alias idea=$(workflow idea $*)
# alias problem=$(workflow problem $*)

# inside of workflow.main you could then do things differently based on the arguments


# GLOBALS
APP_NAME: str = "workflow"
AUTHOR: str = "aboutsblank"

settings: AppSettings
element: Element


@functools.singledispatch
def encode_value(x: Any) -> Any:
    if dataclasses.is_dataclass(x):
        return dataclasses.asdict(x)

    return x


@encode_value.register(dt.datetime)
def _(x: dt.datetime) -> str:
    return x.isoformat()


def serialize(x):
    return json.dumps(x, default=encode_value)


def initParser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        prog=APP_NAME, description="Personal Workflow Helper", epilog="Have a good life"
    )

    # positional arguments
    parser.add_argument("USECASE")
    parser.add_argument("message")

    # value option arguments

    # on/off flag option arguments
    parser.add_argument(
        "-l", "--local", action="store_true"
    )
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

    el: Element = Element(msg=args["message"], author=AUTHOR, date=dt.datetime.now())

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


if __name__ == "__main__":

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
