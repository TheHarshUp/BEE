from pathlib import Path


def run(context):
    if not context.command.args:
        context.console.print(
            "[red]Usage:[/] /write <filename>"
        )
        return


    context.console.print(
        "[cyan]Enter file content.[/]"
    )
    context.console.print(
        "[dim]Type :wq on a new line to save.[/]\n"
    )

    lines = []

    while True:
        line = input()

        if line == ":wq":
            break

        lines.append(line)

    context.fs.write_file(
        context.command.args[0],
        "\n".join(lines),
    )

    context.console.print(
        f"[green]✔ Saved {context.command.args[0]}[/]"
    )