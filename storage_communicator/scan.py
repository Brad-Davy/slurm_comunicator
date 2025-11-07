from directory_report import DirectoryReport
import subprocess

root_directory = "/opt"
recursive = True

directory = DirectoryReport(path=root_directory, recursive=recursive)
print(directory.get_size())
