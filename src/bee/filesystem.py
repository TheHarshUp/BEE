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