from __future__ import annotations

import os
from dataclasses import dataclass
from getpass import getpass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - handled at runtime
    def load_dotenv() -> bool:
        return False

load_dotenv()


def _env_text(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def prompt_text(
    label: str,
    default: str | None = None,
    *, # *後面的參數是 keyword-only argument ，呼叫時一定要附上參數名稱
    secret: bool = False,
    required: bool = True,
) -> str:
    suffix = f" [{default}]" if default else ""

    while True:
        prompt = f"{label}{suffix}: "
        raw_value = getpass(prompt) if secret else input(prompt)
        value = raw_value.strip()

        if value:
            return value
        if default:
            return default
        if not required:
            return ""

        print(f"{label} is required.")


def prompt_int(
    label: str,
    default: int | None = None,
    *, 
    required: bool = True,
) -> int | None:
    default_text = str(default) if default is not None else None

    while True:
        value = prompt_text(label, default_text, required=required)
        if not value:
            return None
        try:
            return int(value)
        except ValueError:
            print(f"{label} must be an integer.")


def prompt_yes_no(label: str, default: bool = True) -> bool:
    choices = "Y/n" if default else "y/N"

    while True:
        value = input(f"{label} [{choices}]: ").strip().lower()
        if not value:
            return default
        if value in {"y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Please answer with y or n.")


@dataclass(slots=True)
class RakutenCredentials:
    app_id: str
    access_key: str

    @classmethod
    def from_env(cls) -> "RakutenCredentials":
        return cls(
            app_id=_env_text("RAKUTEN_APP_ID"),
            access_key=_env_text("RAKUTEN_ACCESS_KEY"),
        )


def prompt_rakuten_credentials() -> RakutenCredentials:
    current = RakutenCredentials.from_env()
    return RakutenCredentials(
        app_id=prompt_text("Rakuten app ID", current.app_id or None),
        access_key=prompt_text(
            "Rakuten access key",
            current.access_key or None,
            secret=True,
        ),
    )
