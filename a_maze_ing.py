#!/usr/bin/env python3

from typing import List, Dict, Any, Tuple,  Optional, Union
import sys
from MazeGenerator import MazeGenerator


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:  python3 a_maze_ing.py <config.txt>")
        sys.exit()
    config: Dict[str, Any] = read_config(sys.argv[1])
    config = convert_values(config)
    print(config)
    maze = MazeGenerator(config["WIDTH"], config["HEIGHT"])
    maze.generate_maze()
    maze.print_maze()

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
                    raise ValueError(f"Invalid key '{key}'.")
                config[key] = value
            for key in mandatory_keys:
                if key not in config:
                    raise ValueError(f"'{key}' is missing.")

    except FileNotFoundError:
        print("RESPONSE: Archive not found")
        sys.exit()
    except PermissionError:
        print("RESPONSE: Archive deny access")
        sys.exit()
    except ValueError as error:
        print(f'RESPONSE: Incorrect config format. {error} Check "config.txt" file')
        sys.exit()
    except Exception as error:
        print(
            f"RESPONSE:  Unexpected error: {error}"
            f"- Type: {type(error).__name__}")
        sys.exit()
    return config

def parse_output_file(output_file: str) -> bool:
    name: str
    type: str
    if output_file.count(".") != 1:
        raise ValueError("'OUTPUT_FILE' must be like -> 'name.txt'")
    name, type = output_file.split(".")

    return type.lower() == "txt"

def convert_values(config: Dict[str, Any]) -> Dict[str, Any]:
    #transformar width em int
    try:
        x: int
        y: int
        w: int
        z: int
        width: int = int(config["WIDTH"])
        height: int = int(config["HEIGHT"])
        if width < 0 or height < 0:
            raise ValueError("Width and Height must be positive")
        if "," not in config["ENTRY"] or "," not in config["EXIT"]:
            raise ValueError("'ENTRY' and 'EXIT' must have only two values separated by ','")
        x, y = config["ENTRY"].split(",")
        entry: tuple = int(x), int(y)
        w, z = config["EXIT"].split(",")
        exit: tuple = int(w), int(z)
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("ENTRY outside maze")
        if not (0 <= exit[0] < width and 0 <= exit[1] < height):
            raise ValueError("EXIT outside maze")
        if entry == exit:
            raise ValueError("ENTRY and EXIT must be different")
        if config["PERFECT"].lower() not in ["true", "false"]:
            raise ValueError("'PERFECT' must be 'True' or 'False'")
        perfect = config["PERFECT"].lower() == "true"
        if not parse_output_file(config["OUTPUT_FILE"]):
            raise ValueError("'OUTPUT_FILE' must be '.txt' file")
        return {
            "WIDTH": width,
            "HEIGHT": height,
            "ENTRY": entry,
            "EXIT": exit,
            "OUTPUT_FILE": config["OUTPUT_FILE"].lower(),
            "PERFECT": perfect
        }
    except ValueError as error:
        value = error.args[0].split(":")[-1].strip()
        print(f"Invalid value: {value}")
        sys.exit()
    except Exception as error:
        print(
            f"RESPONSE:  Unexpected error: {error}"
            f"- Type: {type(error).__name__}"
        )
        sys.exit()


if __name__ == "__main__":
    main()
