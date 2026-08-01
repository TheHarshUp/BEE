from rich.table import Table


def run(context):
    table = Table(title="Project Files")

    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")

    for item in sorted(context.fs.cwd.iterdir()):
        table.add_row(
            item.name,
            "📁 Folder" if item.is_dir() else "📄 File",
        )

    context.console.print(table)