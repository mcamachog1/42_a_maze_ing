#!/usr/bin/env python3


import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:  python3 a_maze_ing.py <config.txt>")
        sys.exit()
    try:
        with open(sys.argv[1]) as f:
            print(f"Leyendo archivo: {sys.argv[1]}")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        sys.exit()
    except PermissionError:
        print("RESPONSE:  Security protocols deny access")
        sys.exit()
    except Exception as e:
        print(
            f"RESPONSE:  Unexpected error: {e}"
            f"- Type: {type(e).__name__}")
        sys.exit()


if __name__ == "__main__":
    main()
