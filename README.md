# Python C Formatter

A formatter for C code, (badly) written in Python. Uses [colorama](https://pypi.org/project/colorama/) for coloring.

## Note

The colorama Python library is required for this to run as of now as I use it to color my outputs. It should be cross-platform

--------------------------------------------------------------------------------

## Syntax

### Basic run

Use `python main.py` to pull up the question form that gets the program all it needs to know.\ Some questions that it will ask without arguments are:

- Filename - what is the name of the file that you want formatted?
- Does your code compile? This is important as my program assumes that your code compiles.
- What setting profile do you want? (This actually brings up the setting system which I talk about in more detail later)

### Other running methods

`python main.py <filename>` where `<filename>` is the name of the file you want to format. This will skip the program asking the first question, instead it just checks that the program compiles and also initiate the setting selection system.

### Expected output

When you run the program and answer all of the questions that it presents to you, it will immediately start running the formatter. The process that this entails is discussed in some detail below.

Once it is done running, it will output the finished, formatted code but also write the code out into files that are named based on the name of the original file. The compressed code will be written to `<filename> + "1"`, and the final version (the fully formatted one) will be output to `<filename> + "2"`. For example, if the name of your C file is `code.c`, then code.c1 will contain the compressed code and code.c2 will contain the stylized code.

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
5. Spaces around equals: Applies to simple assignment statements and also +=, -=, *=, and /= statements.
6. Spaces around comparisons: Applies to comparisons between two things (comparisons checked for are: ==, >=, <=, >, <, !=)
7. Spaces after ampersands: Self-explanatory, if enabled turns the statement &x into & x.
8. Spaces in include statements: Should #include statements have a space between the "include" and the `<header>` or `"header"`?
9. Spaces around operations: Should there be spaces around operations (e.g. +, *, -, /)?
10. Spaces before double operators: This one is pretty self-explanatory, if the formatter encounters something like `x++;` and this is on it will output `x ++;`.
11. Spaces after `*`'s and spaces before `*`'s: These refer to similar situations, if the program detects something like `char*x = &y;`, then it will move the `*` based on these settings, for example if the first one is on and the second is also on then it will output `char * x = &y;` (remember that there is a setting for spaces before the ampersand!)
12. Spaces after control statements: This refers to situations like `if (expr)`; if this is on then there will be a space between the if and the parenthesis and if it's off then there will not be one.
13. Indentation spaces: This simply controls how many spaces the indentation consists of. Not much to say here ._.
14. Lines between functions: This one controls how many lines there should be between each function (body) definition, specifically if there is a close curly bracket and the indentation level then becomes zero it will apply this many line feeds before the next comment or function definition.

### Settings storage

All of the settings are stored in a file called `settings.json`. The program tries to load this file when it prompts for the settings profile, but if it can't find it, it will make one and then input the default settings into it, in a profile called cs50_default. It will then act as if the settings file existed and continue with asking for your profile choice (still giving the option to make a new one)

Once the file is loaded, whether it existed or not, and the profile is chosen, then the program will run the compacter, and send the output into the expander, supplying the settings.

Technical note: this file is loaded as a Python dictionary and saved in proper JSON format with the python built-in JSON library.

--------------------------------------------------------------------------------

## Contributing

Contributing to the project is really easy, if you want to run it you will need colorama installed into your Python interpreter (the PyPI project and how to install colorama is [here](https://pypi.org/project/colorama/)).

If you noticed an issue you want fixed, feel free to report it in the "issues" tab of GitHub and it (should) be fixed (maybe) (if I feel like it).
