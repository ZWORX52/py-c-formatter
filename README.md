# Python C Formatter

A formatter for C code, (badly) written in Python. Uses [colorama](https://pypi.org/project/colorama/) for coloring.

I made this to give IDEs that don't have this feature a way to still have access to this type of program. It's meant to be used on the command line, but most IDEs will have some sort of built-in terminal window which you can use this in when you need it.

--------------------------------------------------------------------------------

## Syntax

### Basic run

Use `python main.py` to pull up the question form that gets the program all it needs to know. Some questions that it will ask without arguments are:

- Filename - what is the name of the file that you want formatted?
- Does your code compile? This is important as my program assumes that your code compiles.
- What setting profile do you want? (This actually brings up the setting system which I talk about in more detail later)

### Other running methods

`python main.py <filename>` where `<filename>` is the name of the file you want to format. This will skip the program asking the first question, instead it just checks that the program compiles and also initiate the setting selection system.

### Expected output

When you run the program and answer all of the questions that it presents to you, it will immediately start running the formatter. The process that this entails is discussed in some detail below.

Once it is done running, it will output the finished, formatted code but also write the code out into files that are named based on the name of the original file. The compressed code will be written to `<filename> + "1"`, and the final version (the fully formatted one) will be output to `<filename> + "2"`. For example, if the name of your C file is `code.c`, then `code.c1` will contain the compressed code and `code.c2` will contain the stylized code.

--------------------------------------------------------------------------------

## Settings

### Settings selection

When the program first starts up and it's time to select your settings, you are prompted with a list of profiles that the program found in your `settings.json` file discussed below. If you type nothing, you are given the default profile. If you type a valid profile name, then that profile is loaded and used as the settings for this session.

### Settings list

This is a list of the settings that you can change to edit the behavior of the formatting program, in order of when they are asked (when you create a new profile)

1. Newlines before curly brackets: Newlines before curly brackets or spaces? (yes means newlines, no means spaces instead of the newline)
2. Spaces before parenthesis: Spaces before the parenthesis in function calls and function signatures
3. Spaces before square brackets: Spaces before square brackets
4. Spaces between function parameters: Spaces between the parameters to function calls and functions signatures
5. Spaces around equals: Applies to simple assignment statements and also +=, -=, *=, /=, and %= statements.
6. Spaces around comparisons: Applies to comparisons between two things (comparisons checked for are: ==, >=, <=, >, <, !=)
7. Spaces after ampersands: Self-explanatory, if enabled turns the statement &x into & x.
8. Spaces in include statements: Should #include statements have a space between the "include" and the `<header>` or `"header"`?
9. Spaces around operations: Should there be spaces around operations (e.g. +, *, -, /, %)?
10. Spaces before double operators: This one is pretty self-explanatory, if the formatter encounters something like `x++;` and this is on it will output `x ++;`.
11. Spaces after `*`'s and spaces before `*`'s: These refer to similar situations, if the program detects something like `char*x = &y;`, then it will move the `*` based on these settings, for example if the first one is on and the second is also on then it will output `char * x = &y;` (remember that there is a setting for spaces before the ampersand!)
12. Spaces after control statements: This refers to situations like `if (expr)`; if this is on then there will be a space between the if and the parenthesis and if it's off then there will not be one.
13. Spaces around logical operators: This is a bit counter-intuitive, but it actually means spaces around the || and && operators.
14. Indentation spaces: This simply controls how many spaces the indentation consists of. Not much to say here ._.
15. Lines between functions: This one controls how many lines there should be between each function (body) definition, specifically if there is a close curly bracket and the indentation level then becomes zero it will apply this many line feeds before the next comment or function definition.

### Settings storage

All of the settings are stored in a file called `settings.json`. The program tries to load this file when it prompts for the settings profile, but if it can't find it, it will make one and then input the default settings into it, in a profile called cs50_default. It will then act as if the settings file existed and continue with asking for your profile choice (still giving the option to make a new one)

Once the file is loaded, whether it existed or not, and the profile is chosen, then the program will run the compacter, and send the output into the expander, supplying the settings.

Technical note: this file is loaded as a Python dictionary and saved in proper JSON format with the python built-in JSON library.

--------------------------------------------------------------------------------

## How it works

The first thing it does when it's called a la the "syntax" section, is ask whether you are debugging the program. Then, it (may, again see "syntax") ask for a filename to be formatted. Here, it also makes sure that your program compiles, as if it doesn't then it will most likely fail. It then checks whether there is a settings file: if there is, it loads it. If there isn't, it makes a dictionary with one profile, saves it to the settings file, and then continues as normal. It will list the possible settings profiles, retrieved by listing the keys of the dictionary loaded/created earlier. Note that here, if you refuse to refuse to give a profile name by just pressing enter immediately, it gives you the default profile. It also gives an option to create a new profile, which if chosen causes the following events:

1. Ask what the new profile should be named
2. Ask about all of the settings in this method: if the setting has a boolean value, then ask: "Should there be {setting name, but underscores are replaced with spaces}"
3. If the settings doesn't have a boolean value, then it assumes that it's an integer and asks: "How many {setting name, but underscores are replaced with spaces} should there be?". It then tries to convert this into an integer.
4. Once the settings that the user wants have been recorded in memory, it saves those settings into the settings file under the new name as the key. It then assumes that the newly created profile is the one you wanted to use and reformats according to that new profile.

The reformatting process is relatively simple: it simply takes in a file name, a few parameters (namely the settings, the built-in c keywords, defined above, also whether or not you're debugging) and calls the compact function on the read input file. It then writes the compacted code to a file, a la the "expected output" section. It then runs the expander, prints that out, and saves it a la "expected output" again.

The compressor was complicated, but then I rewrote it to be less complicated and accidentally made it more compressed (ironically) and less simple. It starts by defining a few variables: in_comment, in_preprocessor, in_string, char, and alphanum. The first three are booleans, and they store what you think they do. "char" is where in the input the program is at the moment. It's the index. The last one is basically all variable-safe characters. Then follows a bunch of logic that manages those first three booleans (that happens on every character). Then, some logic that basically says "if you can safely get rid of it, get rid of it".

The expander isn't extremely complicated, but it IS long. It essentially starts off by defining similar variables to the compressor. Then, it goes into a loop that contains pretty much only a VERY long match statement that is the entire body of the program. This simply tells the program what to do based on the current character, but it's really complicated because most of the time the match statements also move the cursor so it doesn't break totally, and it's _a bit_ convoluted. I'm not going to be going into full detail here, but of note is how large the semicolon branch is. This is because it actually handles most of the `}` logic, only double `}`s get past it.

Once all of that is done, it writes the output to the files, prints it out (_ahem_ twice with debug on). If you want a full explanation of what everything does, the compressor is pretty well commented but not the expander because... well... honestly I'm just lazy. But if you really want, I _might_ comment it - just be careful as there may be more comments than code.

--------------------------------------------------------------------------------

## Contributing

Contributing to the project is quite simple (hopefully), if you want to run it you will need colorama installed into your Python interpreter (the PyPI project and how to install colorama is [here](https://pypi.org/project/colorama/)).

If you noticed an issue you want fixed, feel free to report it in the "issues" tab of GitHub and it (should) be fixed (maybe) (if I feel like it).
