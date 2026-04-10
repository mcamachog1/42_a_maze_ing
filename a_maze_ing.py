#!/usr/bin/env python3

from typing import List, Dict, Any, Tuple, Optional
import sys
import mazegen
import os
from maze_print import print_maze_ascii, get_color, change_color


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage:  python3 a_maze_ing.py <config.txt>", file=sys.stderr)
        sys.exit()

    config: Dict[str, Any] = read_config_file(sys.argv[1])
    config["CONFIG_FILE"] = sys.argv[1]
    convert_config_values(config)
    maze = mazegen.MazeGenerator(config)
    if config["WIDTH"] < 9 or config["HEIGHT"] < 7:
        print(
            "“42” pattern is omitted in case Width is lower "
            "than 9 and Height is lower than 7",
            file=sys.stderr
        )
    else:
        maze.make_42()
    begin_x, begin_y = config["ENTRY"]
    exit_x, exit_y = config["EXIT"]
    if maze.grid[begin_y][begin_x].is_42 or maze.grid[exit_y][exit_x].is_42:
        cells_42: List[Tuple[int, int]] = maze.get_42_cells()
        print(
            "Entry or Exit are invalid cells, "
            f"position belongs to 42\nMust be different than: {cells_42}",
            file=sys.stderr)
        sys.exit()

    print(config)
    path: List[Tuple[int, int]] = []
    option_2: int = 0
    maze.generate_maze()
    path = maze.find_best_path(config["ENTRY"], config["EXIT"])
    maze.create_output_hexa_file(path, config["OUTPUT_FILE"])
    os.system("clear")
    flag = 0
    first = True
    if config["WIDTH"] < 9 or config["HEIGHT"] < 7:
        print(
            "“42” pattern is omitted in case Width is "
            "lower than 9 and Height is lower than 7"
        )
    while True:
        try:
            if first:
                if flag == 0:
                    print_maze_ascii(maze)
                elif path:
                    print_maze_ascii(maze, path)
                first = False
            n_options = [1, 2, 3, 4]
            print("Interface with menu options:")
            options = int(input(
                "1: regen; 2: path; 3: color; 4: quit\n").strip().lower()
            )
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
            print_maze_ascii(maze)
            flag = 0
        elif options == 2:
            option_2 += 1
            if option_2 % 2 != 0:
                os.system("clear")
                print_maze_ascii(maze, path)
                flag = 1
            else:
                os.system("clear")
                print_maze_ascii(maze)
                flag = 0
        elif options == 3:
            color = get_color()
            while change_color() == color:
                continue
            os.system("clear")
            if flag == 0:
                print_maze_ascii(maze)
            elif path:
                print_maze_ascii(maze, path)
        elif options == 4:
            os.system("clear")
            sys.exit()


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
                if value == "None" or value == "":
                    value_opt: Optional[str] = None
                else:
                    value_opt = value
                config[key] = value_opt
            for key in mandatory_keys:
                if key not in config or config[key] is None:
                    raise ValueError(f"'{key}' is missing.")

    except FileNotFoundError:
        print("RESPONSE: Archive not found", file=sys.stderr)
        sys.exit()
    except PermissionError:
        print("RESPONSE: Archive deny access", file=sys.stderr)
        sys.exit()
    except ValueError as error:
        print(
            'RESPONSE: Incorrect config format. '
            f'{error} Check "config.txt" file',
            file=sys.stderr
        )
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
    try:
        x: int
        y: int
        w: int
        z: int
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])
        if config["WIDTH"] < 0 or config["HEIGHT"] < 0:
            raise ValueError("Width and Height must be positive")
        if "," not in config["ENTRY"] or "," not in config["EXIT"]:
            raise ValueError(
                "'ENTRY' and 'EXIT' must have only two values separated by ','"
            )
        x, y = config["ENTRY"].split(",")
        config["ENTRY"] = int(x), int(y)
        w, z = config["EXIT"].split(",")
        config["EXIT"] = int(w), int(z)
        if not (
            0 <= config["ENTRY"][0] < config["WIDTH"]
            and 0 <= config["ENTRY"][1] < config["HEIGHT"]
        ):
            raise ValueError("ENTRY outside maze")
        if not (
            0 <= config["EXIT"][0] < config["WIDTH"]
            and 0 <= config["EXIT"][1] < config["HEIGHT"]
        ):
            raise ValueError("EXIT outside maze")
        if config["ENTRY"] == config["EXIT"]:
            raise ValueError("ENTRY and EXIT must be different")
        if config["PERFECT"].lower() not in ["true", "false"]:
            raise ValueError("'PERFECT' must be 'True' or 'False'")
        config["PERFECT"] = config["PERFECT"].lower() == "true"
        if not is_format_output_file_name(config["OUTPUT_FILE"]):
            raise ValueError("'OUTPUT_FILE' must be '.txt' file")
        config["OUTPUT_FILE"] = config["OUTPUT_FILE"].lower()
        if config["CONFIG_FILE"] == config["OUTPUT_FILE"]:
            raise ValueError(
                f"OUTPUT_FILE must not be '{config['CONFIG_FILE']}'"
            )
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
