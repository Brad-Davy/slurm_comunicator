from directory_scanner import DirectoryScanner
import subprocess


class LocalDirectoryScanner(DirectoryScanner):

    def __init__(self, path: str = "/", recursive: bool = False):
        self.path = path
        self.recursive = recursive

    def get_size(self):
        pass

    def list_files(self) -> list:
        return subprocess.run(
            ["ls", self.path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.splitlines()


if __name__ == "__main__":
    local = LocalDirectoryScanner()
    print(local.path)
