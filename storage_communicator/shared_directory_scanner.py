from directory_scanner import DirectoryScanner


class SharedDirectoryScanner(DirectoryScanner):

    def __init__(self, path: str = "/", recursive: bool = False):
        self.path = path
        self.recursive = recursive

    def get_size(self):
        pass

    def list_files(self):
        pass


if __name__ == "__main__":
    shared = SharedDirectoryScanner()
    print(shared.path)
