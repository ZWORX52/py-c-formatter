from typing import Union

from compact import compact
from expand import expand

import colorama as col
import os
import sys
import json

# Default settings
settings = {
    "newlines_before_curly_brackets": True,
    "spaces_before_parenthesis": False,
    "spaces_before_square_brackets": False,
    "spaces_between_function_parameters": True,
    "spaces_after_conditionals": True,
    "spaces_around_equals": True,
    "spaces_around_comparisons": True,
    "spaces_after_ampersands": False,
    "spaces_in_include_statements": True,
    "spaces_around_operations": True,
    "spaces_before_double_operators": False,
    "spaces_after_*'s": False,
    "spaces_before_*'s": True,
    "indentation_spaces": 4,
    "lines_between_functions": 2
}

# C keywords from https://en.cppreference.com/w/c/keyword
keywords = ["auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern",
            "float", "for", "goto", "if", "inline", "int", "long", "register", "restrict", "return", "short", "signed",
            "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
            "_Alignas", "_Alignof", "_Atomic", "_Bool", "_Complex", "_Decimal128", "_Decimal64", "_Decimal32",
            "_Generic", "_Imaginary", "_Noreturn", "_Static_assert", "_Thread_local"]


def main(infile=None):
    # Ask for filename
    print(f"{col.Fore.YELLOW}Note: This program does not address the following possible C situations:\n"
          f"  - Pointer dereferences\n"
          f"  - Smarter asterix handling\n"
          f"  - 'for' loop recognition\n"
          f"  - Any assignment operator that's not /=, *=, -= or +="
          f"  - a ? b : c type statements{col.Style.RESET_ALL}")

    debug = input(f"{col.Fore.BLUE}Enable debug mode? ONLY ANSWER YES IF YOU ARE TESTING OR DEVELOPING THE PROGRAM!"
                  f"{col.Style.RESET_ALL} ")
    debug = debug.strip().lower() == "y"

    if infile is None:
        infile = input("Enter the name of the file to format: ")

    compiles = input("Does your program compile (y/n)? ")
    if compiles.strip().lower() == "y":
        print(f"{col.Fore.LIGHTRED_EX}WARNING! This program expects your code to compile, so you may get incorrect "
              f"results if your program doesn't compile!{col.Style.RESET_ALL}")
    else:
        # Their program doesn't compile, and therefore we can't trust it; things may go wrong. Exit.
        print(f"{col.Fore.RED}Please try again when your program compiles.{col.Style.RESET_ALL}")
        sys.exit(1)

    # Get settings
    if os.path.exists("settings.json"):
        settings_file = open("settings.json")
        existing_settings = json.load(settings_file)
    else:
        settings_file = open("settings.json", "w+")
        json.dump({"cs50_default": settings}, settings_file, indent=4)
        existing_settings = {"cs50_default": settings}

    print("Allowed profiles:")
    for profile in existing_settings.keys():
        print(f"  {profile}")
    profile_name = input(f"Which profile do you want ('n' to create a new profile)? ")

    if profile_name == "":
        profile_name = "cs50_default"

    if profile_name == "n":
        # They want to make a new profile! Ask them the questions and save it as such.
        profile_name = input("What should the new profile be called? ")
        temp_settings = settings.copy()
        for setting in temp_settings.keys():
            if isinstance(temp_settings[setting], bool):
                temp_settings[setting] = input(f"Should there be {col.Fore.GREEN}"
                                               f"{setting.replace('_', ' ')}{col.Style.RESET_ALL} (y/n)? ") \
                                             .lower().strip() == "y"
            elif isinstance(temp_settings[setting], int):
                temp_settings[setting] = int(input(f"How many {col.Fore.GREEN}{setting.replace('_', ' ')} "
                                                   f"{col.Style.RESET_ALL}should there be? ").strip())

        existing_settings.update({profile_name: temp_settings})
        json.dump(existing_settings, open("settings.json", "w"), indent=4)
        reformat(infile, temp_settings, debug)

    else:
        # They didn't want to make a new profile
        if profile_name not in existing_settings.keys():
            print("That profile doesn't exist!")
            return
        these_settings = existing_settings[profile_name]
        reformat(infile, these_settings, debug)


def reformat(filename: str, settings_: dict[str: Union[int, bool]], debug: bool = False):
    compacted = compact(open(filename).read(), debug).rstrip()
    if debug:
        print(compacted)
    with open(filename + "1", "w+") as out:
        for line in compacted.split("\n"):
            out.write(line + "\n")
    expanded = expand(open(filename + "1", "r").read(), settings_, keywords, debug).rstrip()
    if debug:
        print(expanded)
    with open(filename + "2", "w+") as out:
        for line in expanded.split("\n"):
            out.write(line + "\n")
    print(f"Here is your reformatted code:\n{expanded}")


if __name__ == '__main__':
    col.init()
    if len(sys.argv) == 1:
        main()

    if len(sys.argv) == 2:
        main(sys.argv[1])
