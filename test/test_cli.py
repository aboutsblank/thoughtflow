# import pytest

from thoughtflow import cli

# end to end test cases are also needed


def test_checkConfigCorrectness1():
    args = {"local": 1, "global": True}

    isCorrectConfig, error = cli.checkConfigCorrectness(args)

    assert not isCorrectConfig


def test_checkConfigCorrectness2():
    args = {"local": 0, "global": False}

    isCorrectConfig, error = cli.checkConfigCorrectness(args)

    assert isCorrectConfig


def test_checkConfigCorrectness3():
    args = {"local": 1, "global": False}

    isCorrectConfig, error = cli.checkConfigCorrectness(args)

    assert isCorrectConfig


def test_checkConfigCorrectness4():
    args = {"local": 0, "global": True}

    isCorrectConfig, error = cli.checkConfigCorrectness(args)

    assert isCorrectConfig


def test_searchOnlyLocal():
    cli.getLocalPath(2)
