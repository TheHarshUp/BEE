from rich.syntax import Syntax


def run(context):
    if not context.command.args:
        context.console.print("[red]Usage:[/] /cat <file>")
        return

    path = context.command.args[0]

    try:
        content = context.fs.read_file(path)
    except FileNotFoundError:
        context.console.print("[red]File not found.[/]")
        return
    except IsADirectoryError:
        context.console.print("[red]That's a directory.[/]")
        return

    extension = path.split(".")[-1] if "." in path else ""

    language_map = {
        ".py": "python",
        ".md": "markdown",
        ".toml": "toml",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".html": "html",
        ".css": "css",
        ".js": "javascript",
        ".ts": "typescript",
    }

    language = language_map.get(f".{extension}", "text")

    syntax = Syntax(
        content,
        language,
        line_numbers=True,
        word_wrap=True,
    )

    context.console.print(syntax)