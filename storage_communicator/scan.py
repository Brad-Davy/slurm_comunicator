from directory_report import DirectoryReport
import subprocess

root_directory = "/home"
recursive = False

paths = subprocess.run(
    ["ls", root_directory],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
).stdout.splitlines()

for path in paths:
    directory = DirectoryReport(path=path, recursive=recursive)
    directory.get_size()
    print(directory)
