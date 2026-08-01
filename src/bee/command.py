from dataclasses import dataclass


@dataclass
class Command:
    raw: str
    name: str
    args: list[str]