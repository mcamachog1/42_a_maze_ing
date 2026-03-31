#!/usr/bin/env python3

from typing import List, Dict, Any, Tuple,  Optional, Union
import sys
from MazeGenerator import MazeGenerator
from load_maze import read_maze_from_file


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:  python3 a_maze_ing.py <config.txt>")
        sys.exit()
    config: Dict[str, Any] = read_config_file(sys.argv[1])
    convert_config_values(config)
    maze = MazeGenerator(config)
    maze.make_42()
    begin_x, begin_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]
    print(f"Begin = {maze.grid[begin_y][begin_x].is_42}")
    print(f"Exit = {maze.grid[exit_y][exit_x].is_42}")
    if maze.grid[begin_y][begin_x].is_42 or maze.grid[exit_y][exit_x].is_42:
        print("Entry or Exit are invalid cells, position belongs to 42")
        sys.exit()
    maze.generate_maze()
    maze.print_maze_ascii()
    maze.create_output_hexa_file(config["OUTPUT_FILE"])
    path_1 = []
    path_2 = []

    # Load maze
    new_maze = read_maze_from_file(config["OUTPUT_FILE"])

    start_x, start_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]

    # maze.print_maze_ascii([(0,0), (1, 1)])
    # Get 1st solution
    path_1 = maze.find_first_solution(start_x, start_y, exit_x, exit_y)
    
    # If PERFECT is False make imperfect
    if not config["PERFECT"]:
        maze.make_imperfect(path_1)
        print("This maze IS NOT PERFECT")
    else:
        print("This maze IS PERFECT")

    # Print maze with 1st solution
    print("Try 1st path:")
    maze.print_maze_ascii(path_1)

    # If maze is imperfect get 2nd solution
    if not config["PERFECT"]:
        path_2 = maze.find_second_solution(start_x, start_y, exit_x, exit_y)
        print("Try 2nd path:")
        maze.print_maze_ascii(path_2)
    
    # Get de best path (shorter one)
    print(f"One of the shortest path is:\n")
    path = maze.find_best_path(config["ENTRY"], config["EXIT"])
    maze.add_path_to_file(path, config["OUTPUT_FILE"])
    maze.print_maze_ascii(path)
    



def read_config_file(filename: str) -> Dict[str, Any]:
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
        all_keys: List[str] = list(mandatory_keys)
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


def is_format_output_file_name(output_file: str) -> bool:
    name: str
    type: str
    if output_file.count(".") != 1:
        raise ValueError("'OUTPUT_FILE' must be like -> 'name.txt'")
    name, type = output_file.split(".")

    return type.lower() == "txt"


def convert_config_values(config: Dict[str, Any]) -> None:
    #transformar width em int
    try:
        x: int
        y: int
        w: int
        z: int
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])
        if config["WIDTH"] < 0 or config["HEIGHT"] < 0:
            raise ValueError("Width and Height must be positive")
        if config["WIDTH"] < 9 or config["HEIGHT"] < 7:
            raise ValueError("Width must be at least 9 and Height must be at least 7")        
        if "," not in config["ENTRY"] or "," not in config["EXIT"]:
            raise ValueError("'ENTRY' and 'EXIT' must have only two values separated by ','")
        x, y = config["ENTRY"].split(",")
        config["ENTRY"] = int(x), int(y)
        w, z = config["EXIT"].split(",")
        config["EXIT"] = int(w), int(z)
        if not (0 <= config["ENTRY"][0] < config["WIDTH"] and 0 <= config["ENTRY"][1] < config["HEIGHT"]):
            raise ValueError("ENTRY outside maze")
        if not (0 <= config["EXIT"][0] < config["WIDTH"] and 0 <= config["EXIT"][1] < config["HEIGHT"]):
            raise ValueError("EXIT outside maze")
        if config["ENTRY"] == config["EXIT"]:
            raise ValueError("ENTRY and EXIT must be different")
        if config["PERFECT"].lower() not in ["true", "false"]:
            raise ValueError("'PERFECT' must be 'True' or 'False'")
        config["PERFECT"] = config["PERFECT"].lower() == "true"
        if not is_format_output_file_name(config["OUTPUT_FILE"]):
            raise ValueError("'OUTPUT_FILE' must be '.txt' file")
        config["OUTPUT_FILE"] = config["OUTPUT_FILE"].lower()
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
