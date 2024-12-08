from typing import Any


def read_file(filename: str, filter_func: callable = lambda i: i) -> list:
    with open(filename, "r", newline="", encoding="utf-8") as file:
        lines = file.readlines()
    array = []
    for line in lines:
        array.append(filter_func(line.strip()))
    return array


def write_file(filename: str, lines: list) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(lines)


def load_csv(filename) -> list:
    import csv

    rows = []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        for row in csv.reader(file):
            rows.append(row)
            # yield row
    return rows


def check_if_exists(_dir):
    from os.path import exists
    from os import makedirs

    if exists(_dir) is False:
        print("Creating directory:", _dir)
        makedirs(_dir)
        return True
    return False


def listFiles(path, include_directory=False):
    import glob

    files = glob.glob(f"{path}/**/*", recursive=True)
    if include_directory:
        return [i.replace(path, "") for i in files]
    else:
        return [i.replace("\\", "/").split("/")[-1].split(".")[0] for i in files]


def loader(file: str) -> Any | dict[str, Any] | list[Any]:
    import logging, pathlib

    ext = pathlib.Path(file).suffix
    with open(f"data/{file}", "rb", encoding="utf-8") as _file:
        match ext:
            case "json":
                import json

                return json.load(file)
            case "yaml" | "yml":
                try:
                    import yaml

                    return yaml.safe_load(file)
                except ImportError:
                    logging.warning("Attempting to load %s file without yaml package", file)
            case "csv":
                import csv

                return csv.reader(_file.readlines())
            case "toml":
                import tomllib

                return tomllib.load(_file)
            case _:
                return str(_file.read())
