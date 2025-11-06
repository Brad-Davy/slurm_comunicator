from abc import ABC, abstractmethod


class DirectoryScanner(ABC):

    def __init__(self, path: str, recursive: bool):
        self.path = path
        self.recursive = recursive

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def list_files(self) -> list:
        pass
