from rich.console import Console
from rich.panel import Panel
from bee.llm import LLM
from bee.memory import Memory
from bee.commands import (
    help,
    version,
    clear,
    exit,
    pwd,
    ls,
)
from bee.context import CommandContext
from bee.filesystem import FileSystem
console = Console()


class Agent:
    def __init__(self):
        self.llm = LLM()
        self.memory = Memory()

        self.fs = FileSystem()

        self.context = CommandContext(
            console=console,
            agent=self,
            fs=self.fs,
        )

        self.commands = {
            "/help": help.run,
            "/version": version.run,
            "/clear": clear.run,
            "/exit": exit.run,
            "/pwd": pwd.run,
            "/ls": ls.run,
        }
    VERSION = "0.1.0"

    def run(self):
        self.banner()

        while True:
            command = console.input("[bold yellow]bee > [/]").strip()

            if not command:
                continue

            if command.startswith("/"):
                if command in self.commands:
                    self.commands[command](self.context)
                else:
                    console.print(f"[red]❌ Unknown command:[/] {command}")
            else:
                self.memory.add_user(command)

                response = self.llm.generate(
                    self.memory.get_messages()
                )

                self.memory.add_assistant(response)

                console.print(f"\n🤖 {response}\n")

    def banner(self):
        console.print(
            Panel.fit(
                f"""
[bold yellow]🐝 BEE[/]

AI Coding Agent
Version {self.VERSION}
""",
                border_style="yellow",
            )
        )

        console.print(
            "[dim]Type [bold]/help[/] to see available commands.[/]\n"
        )