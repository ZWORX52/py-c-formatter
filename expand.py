import string as s
from typing import Union


def expand(inpt: str, settings: dict[str: Union[int, bool]], keywords, debug: bool):
    inpt = list(inpt)
    if inpt[-1] == "\n":
        inpt = inpt[:-1]
    # We need to expand the input to be correct. This is going to be a bit challenging.
    # As with compact, we need a while loop so that we can manually change the index that we are at in the loop
    char = 0
    indent_level = 0
    in_preprocessor = False
    in_comment = False
    in_string = False

    while char < len(inpt):
        try:
            if debug:
                print("".join(inpt[char - 50:char + 51]))
            if debug:
                print(f"just ran attempt {char - 1}")
            if debug:
                print(inpt[char - 1] + " is where we're at")
            if debug:
                print(f"surrounding 10 characters: {inpt[char - 10:char + 11]}")
            if debug:
                print("-----------------------------------")

            match inpt[char]:
                case ";":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if inpt[char + 1] == "}":
                        # it's the last line in a block we need to treat it as such: deplete indentation and all the
                        # good stuff
                        inpt.insert(char + 1, "\n")
                        indent_level -= 1
                        to_insert = _generate_indentation(indent_level, settings)
                        inpt = _insert_position(char + 2, inpt, to_insert)
                        # the extra one is for the newline
                        char += len(to_insert) + 3

                        if indent_level == 0:
                            to_insert2 = ["\n"] * (_get_setting("lines_between_functions", settings) + 1)
                            inpt = _insert_position(char, inpt, to_insert2)
                            char += len(to_insert2)

                        elif inpt[char] != "}":
                            # Otherwise, the correct case will take care of it
                            inpt.insert(char, "\n")
                            to_insert = _generate_indentation(indent_level, settings)
                            inpt = _insert_position(char + 1, inpt, to_insert)
                            char += len(to_insert) + 1

                        else:
                            char -= 1

                    else:
                        to_insert = ["\n"] + _generate_indentation(indent_level, settings)
                        inpt = _insert_position(char + 1, inpt, to_insert)
                        char += len(to_insert)

                case "{":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if _get_setting("newlines_before_curly_brackets", settings):
                        inpt.insert(char, "\n")
                        to_insert = _generate_indentation(indent_level, settings)
                        inpt = _insert_position(char + 1, inpt, to_insert)
                        indent_level += 1
                        char += len(to_insert) + 1
                        inpt.insert(char + 1, "\n")
                        to_insert2 = _generate_indentation(indent_level, settings)
                        inpt = _insert_position(char + 1, inpt, to_insert2)
                        char += len(to_insert2)
                    else:
                        inpt.insert(char, " ")
                        char += 1
                        inpt.insert(char + 1, "\n")
                        indent_level += 1
                        to_insert = _generate_indentation(indent_level, settings)
                        inpt = _insert_position(char + 1, inpt, to_insert)

                case "}":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    indent_level -= 1
                    inpt.insert(char, "\n")
                    to_insert = _generate_indentation(indent_level, settings)
                    inpt = _insert_position(char - 1, inpt, to_insert)
                    if indent_level == 0:
                        to_insert2 = ["\n"] * _get_setting("lines_between_functions", settings)
                        inpt = _insert_position(char + 2, inpt, to_insert2)
                        char += len(to_insert2)
                    char += len(to_insert) + 1
                    print(indent_level)

                case "\n":
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    # The only newlines left are after the comments and in the preprocessor. This time,
                    # the preprocessor doesn't need any exceptions as we should always indent to the current
                    # indentation level even to the point of indenting preprocessor statements
                    if in_preprocessor:
                        in_preprocessor = False

                    elif in_comment:
                        in_comment = False

                    to_insert = _generate_indentation(indent_level, settings)
                    inpt = _insert_position(char + 1, inpt, to_insert)
                    char += len(to_insert)

                case ",":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if _get_setting("spaces_between_function_parameters", settings):
                        inpt.insert(char + 1, " ")
                        char += 2

                case "=":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if _get_setting("spaces_around_equals", settings):
                        if inpt[char + 1] == "=" and _get_setting("spaces_around_comparisons", settings):
                            # We are in the first equals in an "==" statement. Place a space after and before and
                            # then skip past the second equals
                            inpt.insert(char, " ")
                            inpt.insert(char + 3, " ")
                            char += 3
                        else:
                            # This one is a variable assignment. Wrap it with spaces, and we're good to go.
                            inpt.insert(char, " ")
                            inpt.insert(char + 2, " ")
                            char += 2

                case "+" | "-" | "/" | "%":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    # Okay. This is an operation, all we need to do is get the setting and wrap with spaces if we're
                    # supposed to
                    # But! what about +=, -= and /=? well, I wil treat that as a part of the "spaces_wrap_equals" set
                    if (inpt[char + 1] == "/" or inpt[char - 1] == "/") and not in_string:
                        # what
                        in_comment = True
                        char += 2
                    elif inpt[char + 1] in "+-":
                        if debug:
                            print("double operator")
                        if _get_setting("spaces_before_double_operators", settings):
                            inpt.insert(char, " ")
                            char += 1
                        else:
                            char += 1

                    elif inpt[char + 1] == "=":
                        if debug:
                            print("assignment operator")
                        if _get_setting("spaces_around_equals", settings):
                            inpt.insert(char + 2, " ")
                            inpt.insert(char, " ")
                            char += 3

                    elif _get_setting("spaces_around_operations", settings):
                        if debug:
                            print("normal operator")
                        inpt.insert(char + 1, " ")
                        inpt.insert(char, " ")
                        char += 2

                case "*":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    is_deref = _is_not_operator(char, inpt, keywords, debug)
                    if is_deref:
                        if debug:
                            print("i decided that it wasn't an operation")
                        if _get_setting("spaces_before_*'s", settings):
                            inpt.insert(char, " ")
                            char += 1
                        if _get_setting("spaces_after_*'s", settings):
                            inpt.insert(char + 1, " ")

                    else:
                        if debug:
                            print("this time I decided that it was one")
                        if _get_setting("spaces_around_operations", settings):
                            inpt.insert(char + 1, " ")
                            inpt.insert(char, " ")
                            char += 1

                case "(":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if is_prev_word_keyword(inpt, keywords, char - 1):
                        # for loop, if statement, while loop...
                        if _get_setting("spaces_after_control_statements", settings):
                            inpt.insert(char, " ")
                        char += 1
                    elif _get_setting("spaces_before_parenthesis", settings):
                        inpt.insert(char, " ")
                        char += 1

                case "[":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if _get_setting("spaces_before_square_brackets", settings):
                        inpt.insert(char, " ")
                        char += 1

                case "<" | ">":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    if inpt[char + 1] == "=":
                        if _get_setting("spaces_around_comparisons", settings):
                            inpt.insert(char + 3, " ")
                            inpt.insert(char, " ")
                            char += 1
                    elif in_preprocessor and inpt[char] == "<" and \
                            _get_setting("spaces_in_include_statements", settings):
                        if debug:
                            print("im-a in da preprocessor")
                        inpt.insert(char, " ")
                        char += 1
                    elif not in_preprocessor:
                        if _get_setting("spaces_around_comparisons", settings):
                            inpt.insert(char + 1, " ")
                            inpt.insert(char, " ")
                            char += 1

                case "!":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if debug:
                        print(f"I got to a case, it's {inpt[char]}")
                    # If we're doing something like !<expr>, I don't have a setting for a space there. So if we don't
                    # see an "=" directly after we can assume to leave it alone.
                    if inpt[char + 1] == "=":
                        if _get_setting("spaces_around_comparisons", settings):
                            inpt.insert(char + 2, " ")
                            inpt.insert(char, " ")
                            char += 3

                case "#":
                    if not in_string and not in_comment:
                        in_preprocessor = True

                case "\"":
                    if in_preprocessor:
                        if _get_setting("spaces_in_include_statements", settings) and inpt[char + 1] != "\n":
                            inpt.insert(char, " ")
                            char += 2
                    elif not in_comment:
                        in_string = not in_string

                case "'":
                    # skip char literals
                    if not in_string and not in_comment:
                        if inpt[char + 1] == "\\":
                            char += 3
                        else:
                            char += 2

                case "&":
                    if in_comment or in_string:
                        char += 1
                        continue
                    if inpt[char + 1] == "&":
                        if _get_setting("spaces_around_logical_operators", settings):
                            inpt.insert(char + 2, " ")
                            inpt.insert(char, " ")
                            char += 2
                    elif _get_setting("spaces_after_ampersands", settings):
                        inpt.insert(char + 1, " ")

                case "|":
                    if not in_comment and not in_string and inpt[char + 1] == "|" and\
                            _get_setting("spaces_around_logical_operators", settings):
                        inpt.insert(char + 2, " ")
                        inpt.insert(char, " ")
                        char += 2

                case _:
                    if debug:
                        print(f"I got to no case, but we're here {inpt[char]}")

        except IndexError:
            char -= 1

        char += 1

    return "".join(inpt)


def _get_setting(setting_name, settings):
    return settings[setting_name]


def _generate_indentation(indent_level, settings):
    return [" "] * _get_setting("indentation_spaces", settings) * indent_level


def _is_not_operator(index, inpt, keywords, debug):
    # check if the previous word is a keyword or if the next word is a keyword
    char = index - 1
    # if the next or previous token is a keyword then we are not multiplying. that is currently the logic
    alphanum = s.ascii_letters + s.digits + "_"
    explored_left = ""
    while inpt[char] in alphanum:
        explored_left += inpt[char]
        char -= 1

    # Got to reverse it as it would be backwards otherwise
    explored_left = explored_left[::-1]

    explored_right = ""
    char = index + 1
    while inpt[char] in alphanum:
        explored_right += inpt[char]
        char += 1

    if debug:
        print(f"left is .{explored_left}., right is .{explored_right}.")
    if explored_right in keywords or explored_left in keywords:
        return True

    return False


def is_prev_word_keyword(inpt, keywords, index):
    word = ""
    char = index
    if inpt[char] == " ":
        # We need to march back to find it; this is only useful for when this function is called in expand.py
        while inpt[char] == " ":
            char -= 1
    while inpt[char] not in " ;" and char != -1:
        word += inpt[char]
        char -= 1
    # Don't forget to reverse it first
    return word[::-1] in keywords


def _insert_position(position: int, list1: list, list2: list) -> list:
    return list1[:position] + list2 + list1[position:]
