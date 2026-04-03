#!/usr/bin/env python3

from typing import List, Dict, Any, Tuple,  Optional, Union
import sys
from MazeGenerator import MazeGenerator
from load_maze import read_maze_from_file
import os


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:  python3 a_maze_ing.py <config.txt>", file=sys.stderr)
        sys.exit()
    config: Dict[str, Any] = read_config_file(sys.argv[1])
    convert_config_values(config)
    maze = MazeGenerator(config)
    if config["WIDTH"] < 9 or config["HEIGHT"] < 7:
        print("“42” pattern is omitted in case Width is lower than 9 and Height is lower than 7", file=sys.stderr)
    else:
        maze.make_42()
    begin_x, begin_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]
    # print(f"Begin = {maze.grid[begin_y][begin_x].is_42}")
    # print(f"Exit = {maze.grid[exit_y][exit_x].is_42}")
    if maze.grid[begin_y][begin_x].is_42 or maze.grid[exit_y][exit_x].is_42:
        print("Entry or Exit are invalid cells, position belongs to 42", file=sys.stderr)
        sys.exit()
    # maze.generate_maze()
    # maze.print_maze_ascii()
    # maze.create_output_hexa_file(config["OUTPUT_FILE"])
    # path_1 = []
    # path_2 = []

    # # Load maze
    # # new_maze = read_maze_from_file(config["OUTPUT_FILE"])

    # start_x, start_y = config["ENTRY"]
    # exit_x, exit_y = config["EXIT"]

    # # maze.print_maze_ascii([(0,0), (1, 1)])
    # # Get 1st solution
    # path_1 = maze.find_first_solution()
    
    # # If PERFECT is False make imperfect
    # if not config["PERFECT"]:
    #     maze.make_imperfect(path_1)
    #     print("This maze IS NOT PERFECT")
    # else:
    #     print("This maze IS PERFECT")

    # # Print maze with 1st solution
    # print("Try 1st path:")
    # #maze.print_maze_ascii(path_1)

    # # If maze is imperfect get 2nd solution
    # if not config["PERFECT"]:
    #     path_2 = maze.find_second_solution(start_x, start_y, exit_x, exit_y)
    #     print("Try 2nd path:")
    #     maze.print_maze_ascii(path_2)
    
    # # Get de best path (shorter one)
    # print(f"One of the shortest path is:\n")
    # path = maze.find_best_path(config["ENTRY"], config["EXIT"])
    # maze.add_path_to_file(path, config["OUTPUT_FILE"])
    #maze.print_maze_ascii()
    
# *******************
    #print("Interface with menu options:")

    path: List[Tuple[int, int]] = []
    option_2: int = 0
    maze.generate_maze()
    path = maze.find_best_path(config["ENTRY"], config["EXIT"])
    maze.create_output_hexa_file(path, config["OUTPUT_FILE"])
    os.system("clear")
    #maze.print_maze_ascii()
    flag = 0
    first = True
    while True:
        try:
            if first:
                maze.print_maze_ascii()
                first = False
            n_options = [1, 2, 3, 4]
            print("Interface with menu options:")
            options = int(input("1: regen; 2: path; 3: color; 4: quit\n").strip().lower())
            if options not in n_options:
                raise ValueError
        except ValueError:
            print(f"Invalid input. Expected one of: {n_options}")
            os.system("clear")
            first = True
            continue
        if options == 1:
            option_2 = 0
            maze.generate_maze()
            path = maze.find_best_path(config["ENTRY"], config["EXIT"])
            maze.create_output_hexa_file(path, config["OUTPUT_FILE"])
            os.system("clear")
            maze.print_maze_ascii()
            flag = 0
        elif options == 2:
            option_2 += 1
            # if not path:
            #     path = maze.find_best_path(config["ENTRY"], config["EXIT"])
            #     maze.add_path_to_file(path, config["OUTPUT_FILE"])
            if option_2  % 2 != 0:
                os.system("clear")
                maze.print_maze_ascii(path)
                flag = 1
            else:
                os.system("clear")
                maze.print_maze_ascii()
                flag = 0
        elif options == 3:
            maze.change_color()
            os.system("clear")
            if flag == 0:
                maze.print_maze_ascii()
            elif path:
                maze.print_maze_ascii(path)
        elif options == 4:
            os.system("clear")
            sys.exit()

# *******************




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
        print("RESPONSE: Archive not found", file=sys.stderr)
        sys.exit()
    except PermissionError:
        print("RESPONSE: Archive deny access", file=sys.stderr)
        sys.exit()
    except ValueError as error:
        print(f'RESPONSE: Incorrect config format. {error} Check "config.txt" file', file=sys.stderr)
        sys.exit()
    except Exception as error:
        print(
            f"RESPONSE:  Unexpected error: {error}"
            f"- Type: {type(error).__name__}", file=sys.stderr)
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
        #if config["WIDTH"] < 9 or config["HEIGHT"] < 7:
        #    raise ValueError("Width must be at least 9 and Height must be at least 7")        
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
        print(f"Invalid value: {value}", file=sys.stderr)
        sys.exit()
    except Exception as error:
        print(
            f"RESPONSE:  Unexpected error: {error}"
            f"- Type: {type(error).__name__}", file=sys.stderr
        )
        sys.exit()


if __name__ == "__main__":
    main()
