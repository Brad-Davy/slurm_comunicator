from directory_scanner import DirectoryScanner
import subprocess
from pathlib import Path


class LocalDirectoryScanner(DirectoryScanner):

    def __init__(self, path: str = "/", recursive: bool = True):
        self.path = path
        self.recursive = recursive

    def get_size(self) -> int:
        print( f'{self.path}/*')
        size_byt = subprocess.run(
                ["du", '-s', f'{self.path}/*'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
                ).stdout
        print(size_byt)
        for s in size_byt:
            print(s)
        return sum([int(s.split()[0]) for s in size_byt])

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
