from rich.console import Console
from rich.panel import Panel
from bee.llm import LLM
from bee.memory import Memory
from bee.context import CommandContext
from bee.filesystem import FileSystem
from bee.command import Command
from bee.command_loader import load_commands
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

        self.commands = load_commands()
    VERSION = "0.1.0"

    def run(self):
        self.banner()

        while True:
            command = console.input("[bold yellow]bee > [/]").strip()

            if not command:
                continue

            if command.startswith("/"):
                parts = command.split()

                self.context.command = Command(
                    raw=command,
                    name=parts[0],
                    args=parts[1:],
                )

                if self.context.command.name in self.commands:
                    self.commands[self.context.command.name](self.context)
                else:
                    console.print(
                        f"[red]❌ Unknown command:[/] {self.context.command.name}"
                    )
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