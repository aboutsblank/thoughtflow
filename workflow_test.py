import pytest

import workflow

# end to end test cases are also needed


def test_checkConfigCorrectness1():
    args = {"local": 1, "global": True}

    isCorrectConfig, error = workflow.checkConfigCorrectness(args)

    assert not isCorrectConfig


def test_checkConfigCorrectness2():
    args = {"local": 0, "global": False}

    isCorrectConfig, error = workflow.checkConfigCorrectness(args)

    assert isCorrectConfig


def test_checkConfigCorrectness3():
    args = {"local": 1, "global": False}

    isCorrectConfig, error = workflow.checkConfigCorrectness(args)

    assert isCorrectConfig


def test_checkConfigCorrectness4():
    args = {"local": 0, "global": True}

    isCorrectConfig, error = workflow.checkConfigCorrectness(args)

    assert isCorrectConfig


def test_searchOnlyLocal():
    workflow.getLocalPath(2)
