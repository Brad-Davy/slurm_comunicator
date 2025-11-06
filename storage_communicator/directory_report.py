from local_directory_scanner import LocalDirectoryScanner
from shared_directory_scanner import SharedDirectoryScanner


class DirectoryReport:

    def __init__(self, path: str, recursive: str):
        self.path = path
        self.recursive = recursive

        if self._is_shared():
            self.directory = SharedDirectoryScanner(
                path=self.path, recursive=self.recursive
            )
        else:
            self.directory = LocalDirectoryScanner(
                path=self.path, recursive=self.recursive
            )

    def __str__(self):
        return f"Directory object of: {self.path}"

    def _is_shared(self) -> bool:
        "Determine if directory is in local or network file share."
        return True

    def get_size(self):
        "Return the size of the directory."
        return self.directory.get_size()

    def list_files(self):
        "List all files within the directory."
        return self.directory.list_files()
