import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("usage: thaw <source>")
        return 1

    source = Path(sys.argv[1])

    if not source.is_file():
        print(f"error: source file not found: {source}")
        return 1

    print(f"source: {source}")

    return 0


if __name__ == "__main__":
    sys.exit(main())