from pathlib import Path


class FileSystem:
    def __init__(self):
        self.cwd = Path.cwd()

    def pwd(self):
        return self.cwd