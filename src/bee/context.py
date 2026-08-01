from dataclasses import dataclass

from rich.console import Console

from bee.command import Command


@dataclass
class CommandContext:
    console: Console
    agent: object
    fs: object
    command: Command | None = None