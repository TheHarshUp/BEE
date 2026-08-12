import json

from rich.console import Console
from rich.panel import Panel

from bee.command import Command
from bee.command_loader import load_commands
from bee.context import CommandContext
from bee.filesystem import FileSystem
from bee.llm import LLM
from bee.memory import Memory
from bee.tools import ToolExecutor


console = Console()


class Agent:
    VERSION = "0.1.0"

    def __init__(self):
        self.llm = LLM()
        self.memory = Memory()
        self.fs = FileSystem()

        self.context = CommandContext(
            console=console,
            agent=self,
            fs=self.fs,
        )

        self.tools = ToolExecutor(self.fs)
        self.commands = load_commands()

    def run(self):
        self.banner()

        while True:
            command = console.input(
                "[bold yellow]bee > [/]"
            ).strip()

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
                    self.commands[
                        self.context.command.name
                    ](self.context)
                else:
                    console.print(
                        f"[red]❌ Unknown command:[/] "
                        f"{self.context.command.name}"
                    )

            else:
                self.handle_chat(command)

    def handle_chat(self, command):
        self.memory.add_user(command)

        while True:
            response = self.llm.generate(
                self.memory.get_messages()
            )

            try:
                data = json.loads(response)

            except json.JSONDecodeError:
                console.print(
                    f"\n🤖 {response}\n"
                )
                self.memory.add_assistant(response)
                return

            tool_name = data.get("tool")

            if tool_name == "none":
                final_response = data.get(
                    "response",
                    "",
                )

                self.memory.add_assistant(
                    final_response
                )

                console.print(
                    f"\n🤖 {final_response}\n"
                )

                return

            try:
                console.print(
                    f"\n🔧 {tool_name}"
                )

                result = self.tools.execute(
                    response
                )

                console.print(
                    f"[green]✔ Tool completed[/]\n"
                )

                if tool_name in {"write_file", "edit_file"}:
                    console.print(
                        f"🤖 {result}\n"
                    )

                    self.memory.add_assistant(
                        result
                    )

                    return

                self.memory.add_assistant(
                    response
                )

                self.memory.add_tool_result(
                    result
                )

            except Exception as e:
                console.print(
                    f"\n[red]❌ Tool error:[/] {e}\n"
                )

                self.memory.add_tool_result(
                    f"Tool failed: {e}. "
                    "You must read the file first before attempting another edit."
                )

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