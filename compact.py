import string as s


def compact(inpt: str, debug: bool):
    # The input needs to be a list, so we can do .pop() on it later (we will turn it back into a str with .join())
    inpt = list(inpt)
    char = 0
    in_comment = False
    in_string = False
    in_preprocessor = False
    alphanum = s.ascii_letters + s.digits

    while char < len(inpt):
        # print(f"attempt number {char + 1}")
        try:
            if inpt[char] == '"':
                in_string = not in_string
            if inpt[char] == "/" and inpt[char + 1] == "/":
                # Comment!
                in_comment = True
                char += 2
                continue
            if in_comment and inpt[char] == "\n":
                in_comment = False
                char += 1
                continue
            if inpt[char] == "#" and not in_preprocessor:
                in_preprocessor = True
                char += 1
                continue
            if inpt[char] == "\n" and in_preprocessor:
                in_preprocessor = False
                char += 1
                continue

            # print("".join(inpt)[char - 10:char + 11])
            # print(in_string, in_comment, in_preprocessor)

            if inpt[char] in s.whitespace:
                if not in_string and not in_comment and not in_preprocessor:
                    # If you're in normal code
                    if debug:
                        print("remove clause 1")
                    if inpt[char - 1] in alphanum and inpt[char + 1] in alphanum and inpt[char] in s.whitespace:
                        # and before and after are alpha characters then skip this one
                        if debug:
                            print("part 1")
                        char += 1
                        continue
                    elif (inpt[char - 1] not in alphanum and inpt[char + 1] in alphanum) or \
                            (inpt[char + 1] not in alphanum and inpt[char - 1] in alphanum) and\
                            inpt[char] in s.whitespace:
                        # If you have an ascii character on one side and a non-ascii on the other,
                        # Then it's safe to remove
                        if debug:
                            print("part 2")
                        if debug:
                            print(f"removed .{inpt[char]}.")
                        inpt.pop(char)
                        char -= 1
                    elif inpt[char - 1] not in alphanum and inpt[char + 1] not in alphanum and\
                            inpt[char] in s.whitespace:
                        if debug:
                            print("part 3")
                        if debug:
                            print(f"removed .{inpt[char]}.")
                        inpt.pop(char)
                        char -= 1

                # Remember to finish this up!
                elif inpt[char + 1] in s.whitespace and not in_string and not in_comment:
                    # If the next character is also a whitespace, then the previous or next possible keywords
                    # will be buffered by the second whitespace
                    if debug:
                        print("remove clause 2")
                    if debug:
                        print(f"removed .{inpt[char]}.")
                    inpt.pop(char)
                    char -= 1
                if in_preprocessor and inpt[char + 1] not in alphanum and \
                        inpt[char - 1] not in alphanum or inpt[char + 1] in "<\"" and inpt[char] in s.whitespace:
                    # This one's tricky. We are in the preprocessor so the first clause, which would normally resolve
                    # this, fails. So we need to pay attention to a simple #include situation. But to also take care of
                    # #define abc xyz situations we need to do the same thing as clause 1, but this time instead of
                    # s.ascii_letters we need s.ascii_letters AND s.digits
                    if debug:
                        print("remove clause 3")
                    if debug:
                        print(f"removed .{inpt[char]}.")
                    inpt.pop(char)
                    char -= 1

            # print("--------------------------")
        except IndexError:
            char += 1
            continue

        char += 1

    result = "".join(inpt)
    result.replace("\n ", "\n")
    return result


# def is_next_word_keyword(inpt, keywords, index):
#     if inpt[index - 1] in ";>)(}=,{":
#         return False
#     word = ""
#     for char in range(index, len(inpt)):
#         if char == " ":
#             break
#         word += inpt[char]
#     return word in keywords


def next_two_in(inpt, index, valids):
    next_two = inpt[index] + inpt[index + 1]
    for valid in valids:
        if valid.startswith(next_two):
            return True
    return False
