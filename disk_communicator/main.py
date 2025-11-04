import shutil
import subprocess

def check_usage(path="/"):
    total, used, free = shutil.disk_usage(path)

    if total != 0:
        percent = used / total * 100
    else:
        percent = 100
    print(
        f"{path}: {used // (2**30)} GiB used / {total // (2**30)} GiB total ({percent:.1f}%)"
    )


paths = subprocess.run(
            ["ls", "/"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.splitlines()


for p in paths:
    try:
        check_usage(f'/{p}')
    except FileNotFoundError:
        print(f"{p}: not found")
