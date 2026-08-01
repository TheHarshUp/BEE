from pathlib import Path


def build_tree(path: Path, prefix=""):
    IGNORE = {
        ".git",
        ".venv",
        "__pycache__",
        ".DS_Store",
        "dist",
        "build",
        "*.egg-info",
    }


    entries = sorted(
        [
            p
            for p in path.iterdir()
            if not (
                p.name.startswith(".")
                or p.name == "__pycache__"
                or p.name.endswith(".egg-info")
                or p.name == "dist"
                or p.name == "build"
            )
        ],
        key=lambda x: (x.is_file(), x.name.lower()),
    )

    tree = ""

    for index, entry in enumerate(entries):
        connector = "└── " if index == len(entries) - 1 else "├── "

        tree += f"{prefix}{connector}"

        if entry.is_dir():
            tree += f"📁 {entry.name}\n"

            extension = "    " if index == len(entries) - 1 else "│   "

            tree += build_tree(
                entry,
                prefix + extension,
            )

        else:
            tree += f"📄 {entry.name}\n"

    return tree


def run(context):
    tree = build_tree(context.fs.cwd)

    context.console.print(tree)