import argparse
import datetime as dt
import os
import re
import subprocess
from pathlib import Path


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


def main():
    parser = argparse.ArgumentParser(prog="daily")

    # positional arguments
    parser.add_argument("date")
    args: dict = vars(parser.parse_args())

    path: Path = identify_date_path(args["date"])

    editor = os.getenv("EDITOR", "micro")

    path.parent.mkdir(parents=True, exist_ok=True)

    subprocess.run([editor, str(path)])


def identify_date_path(arg: str) -> Path:
    """Return the notes vault path.

    Raises:
        ConfigError: if $VAULT is unset.
    """

    vault_env: (str | None) = os.getenv("VAULT")

    if vault_env is None:
        raise ConfigError(
            "$VAULT is not set - point it at your notes vault, e.g. export VAULT=~/notes"
        )

    goal_date: dt.date = parse_date(arg, dt.date.today())

    goal_path: Path = Path(f"{vault_env}/daily/{goal_date}.md")

    return goal_path


def parse_date(arg: str, today: dt.date) -> dt.date:
    goal_date: dt.date = today

    re_date = r"^(?:19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"  # <YYYY-MM-DD> pattern
    re_number = r"^([-+]?\d+)$"  # (+i|i|-i) pattern

    if re.match(re_date, arg):
        goal_date = dt.date.strptime(arg, "%Y-%m-%d")
    elif re.match(re_number, arg):
        delta = dt.timedelta(days=int(arg))  # casting int to support "+1"
        goal_date = today + delta
    else:
        raise ValueError(f"Invalied / Malformed / Unsupported argument: {arg}")

    return goal_date


if __name__ == "__main__":
    main()
