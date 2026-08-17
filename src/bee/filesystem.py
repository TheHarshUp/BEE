from pathlib import Path
import subprocess


class FileSystem:
    def __init__(self):
        self.cwd = Path.cwd()

    def read_file(self, path: str) -> str:
        file_path = self.cwd / path

        if not file_path.exists():
            raise FileNotFoundError(path)

        if file_path.is_dir():
            raise IsADirectoryError(path)

        return file_path.read_text(encoding="utf-8")

    def write_file(self, path: str, content: str):
        file_path = self.cwd / path

        file_path.write_text(
            content,
            encoding="utf-8",
        )
    def edit_file(self, path: str, old_text: str, new_text: str):
        content = self.read_file(path)

        if old_text not in content:
            raise ValueError(
                f"Text to replace was not found. "
                f"Current file content:\n{content}"
            )

        if new_text.count(old_text) > 1:
            raise ValueError(
                "Edit rejected because the new text duplicates existing content."
            )

        updated_content = content.replace(
            old_text,
            new_text,
            1,
        )

        self.write_file(path, updated_content)
    def run_command(self, command: str) -> str:
        result = subprocess.run(
            command,
            shell=True,
            cwd=self.cwd,
            capture_output=True,
            text=True,
        )

        output = result.stdout

        if result.stderr:
            output += result.stderr

        if result.returncode != 0:
            output += f"\nCommand exited with code {result.returncode}"

        return output.strip()

    def exists(self, path: str):
        return (self.cwd / path).exists()

    def is_dir(self, path: str):
        return (self.cwd / path).is_dir()

    def list_dir(self):
        return sorted(
            self.cwd.iterdir(),
            key=lambda x: (x.is_file(), x.name.lower()),
        )
    def list_project(self):
        ignored = {
            ".git",
            ".venv",
            "__pycache__",
            ".DS_Store",
            "dist",
            "build",
            ".env",
        }

        files = []

        for path in self.cwd.rglob("*"):
            if not path.is_file():
                continue

            if any(part in ignored for part in path.parts):
                continue

            if any(
                part.endswith(".egg-info")
                for part in path.parts
            ):
                continue

            files.append(
                str(path.relative_to(self.cwd))
            )

        return "\n".join(
            sorted(files)
        )
    def search_project(self, query: str):
        ignored = {
            ".git",
            ".venv",
            "__pycache__",
            ".DS_Store",
            "dist",
            "build",
            ".env",
        }

        terms = [
            term.lower()
            for term in query.split()
            if term.strip()
        ]

        matches = {}

        for path in self.cwd.rglob("*"):
            if not path.is_file():
                continue

            if any(part in ignored for part in path.parts):
                continue

            if any(
                part.endswith(".egg-info")
                for part in path.parts
            ):
                continue

            try:
                lines = path.read_text(
                    encoding="utf-8"
                ).splitlines()
            except (UnicodeDecodeError, OSError):
                continue

            relative_path = str(
                path.relative_to(self.cwd)
            )

            for line_number, line in enumerate(
                lines,
                start=1,
            ):
                line_lower = line.lower()

                score = sum(
                    term in line_lower
                    for term in terms
                )

                if score > 0:
                    if relative_path not in matches:
                        matches[relative_path] = {
                            "lines": lines,
                            "matches": [],
                            "score": 0,
                        }

                    matches[relative_path]["matches"].append(
                        line_number
                    )

                    matches[relative_path]["score"] += score

        if not matches:
            return "No matches found."

        ranked_files = sorted(
            matches.items(),
            key=lambda item: (
                -item[1]["score"],
                item[0].lower(),
            ),
        )

        results = []

        for relative_path, data in ranked_files:
            lines = data["lines"]
            matched_lines = data["matches"]

            groups = []
            current_group = []

            for line_number in matched_lines:
                if not current_group:
                    current_group = [line_number]
                    continue

                if line_number <= current_group[-1] + 5:
                    current_group.append(line_number)
                else:
                    groups.append(current_group)
                    current_group = [line_number]

            if current_group:
                groups.append(current_group)

            file_output = [
                relative_path
            ]

            for group in groups:
                start = max(
                    1,
                    group[0] - 2,
                )

                end = min(
                    len(lines),
                    group[-1] + 2,
                )

                for line_number in range(
                    start,
                    end + 1,
                ):
                    file_output.append(
                        f"  {line_number}: "
                        f"{lines[line_number - 1]}"
                    )

                file_output.append("")

            results.append(
                "\n".join(file_output).rstrip()
            )

            if len(results) >= 20:
                break

        return "\n\n".join(results)
        