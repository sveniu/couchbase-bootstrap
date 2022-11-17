import subprocess


def meminfo():
    """Return /proc/meminfo as a dict, with byte units"""
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, rest = line.split(":")
            rest_split = rest.strip().split()

            unit = None
            if len(rest_split) == 1:
                num = rest_split[0]
            elif len(rest_split) == 2:
                num, unit = rest_split

            if unit is None:
                num = int(num)
            elif unit == "kB":
                num = int(num) * 1024

            info[key] = num

    return info


def exec_cbq_script(engine, username, password, path):
    args = [
        "cbq",
        "-e",
        engine,
        "-u",
        username,
        "-p",
        password,
        "-f",
        path,
    ]

    return subprocess.check_output(args)
