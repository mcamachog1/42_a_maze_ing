#!/usr/bin/env python3

from typing import List, Dict, Any, Tuple,  Optional, Union
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:  python3 a_maze_ing.py <config.txt>")
        sys.exit()
    config: Dict[str, Any] = read_config(sys.argv[1])
    config = convert_values(config)
    print(config)

def read_config(filename: str) -> Dict[str, Any]:
    config: Dict[str, Any] = {}
    try:
        mandatory_keys: List[str] = [
            "WIDTH", 
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
            ]
        all_keys: List[str] = mandatory_keys
        all_keys.extend(["SEED", "ALGORITHM", "DISPLAY_MODE"])

        with open(filename) as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=")
                if key not in all_keys:
                    raise ValueError
                print(f"key={key}, value={value}")
                config[key] = value
            for key in mandatory_keys:
                if key not in config.keys():
                    raise ValueError

    except FileNotFoundError:
        print("RESPONSE: Archive not found")
        sys.exit()
    except PermissionError:
        print("RESPONSE: Archive deny access")
        sys.exit()
    except ValueError:
        print('RESPONSE: Incorrect config format. Check "config.txt" file')
        sys.exit()
    except Exception as e:
        print(
            f"RESPONSE:  Unexpected error: {e}"
            f"- Type: {type(e).__name__}")
        sys.exit()
    return config

def convert_values(config: Dict[str, Any]) -> Dict[str, Any]:
    #transformar width em int
    #transformar height em int
    #ENTRY e EXIT
    #'PERFECT'
    #SEED
    pass


if __name__ == "__main__":
    main()
