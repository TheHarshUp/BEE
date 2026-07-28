from rich.console import Console
from rich.panel import Panel
from bee.llm import LLM

console = Console()


class Agent:
    def __init__(self):
        self.llm = LLM()
    VERSION = "0.1.0"

    def run(self):
        self.banner()

        commands = {
            "/help": self.cmd_help,
            "/version": self.cmd_version,
            "/clear": self.cmd_clear,
            "/exit": self.cmd_exit,
        }

        while True:
            command = console.input("[bold yellow]bee > [/]").strip()

            if not command:
                continue

            if command.startswith("/"):
                if command in commands:
                    commands[command]()
                else:
                    console.print(f"[red]❌ Unknown command:[/] {command}")
            else:
                response = self.llm.generate(command)
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

    def cmd_help(self):
        console.print(
            Panel.fit(
                """
[bold cyan]Available Commands[/]

[yellow]/help[/]      Show this menu
[yellow]/version[/]   Show version
[yellow]/clear[/]     Clear the screen
[yellow]/exit[/]      Exit BEE
""",
                title="Help",
                border_style="cyan",
            )
        )

    def cmd_version(self):
        console.print(f"\n🐝 [bold green]BEE v{self.VERSION}[/]\n")

    def cmd_clear(self):
        console.clear()
        self.banner()

    def cmd_exit(self):
        console.print("\n👋 [bold red]Goodbye![/]")
        raise SystemExit