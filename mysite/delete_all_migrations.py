import os
from pathlib import Path


def main():
    migration_path_list = list(Path("./").glob(r"**/migrations/[0-9]*.py"))
    for path in migration_path_list:
        os.remove(str(path))


if __name__ == "__main__":
    main()
