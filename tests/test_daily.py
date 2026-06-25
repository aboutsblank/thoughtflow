import thoughtflow.daily as daily
from datetime import date
from pathlib import Path

import pytest


def test_parse_date_plus1():
    today: date = date(2026, 6, 1)
    goal = daily.parse_date("+1", today)

    assert goal == date(2026, 6, 2)

def test_parse_date_minus1():
    today: date = date(2026, 6, 1)
    goal = daily.parse_date("-1", today)

    assert goal == date(2026, 5, 31)

def test_parse_date_0():
    today: date = date(2026, 6, 1)
    goal = daily.parse_date("0", today)

    assert goal == date(2026, 6, 1)
