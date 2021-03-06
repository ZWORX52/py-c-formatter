#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include "cs50.h"

#define STRLEN_ALLOCATED_IN_SWAP 8192

char substitute_char(char c, string k);

string perform_substitution(string s, string k);

int main(int argc, string argv[])
{
    // Exit if too many arguments or too few
    if (argc != 2)
    {
        printf("Usage: ./substitution <key>\n");
        return 1;
    }
    // Exit if key length is not 26
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    string key = argv[1];
    // Check that all characters in the key are letters
    char letters_used_in_key[26] = "                          ";
    for (int i = 0, n = strlen(key); i < n; i++)
    {
        char this_char = key[i];
        if (!isalpha(this_char))
        {
            printf("Key must be comprised of letters!\n");
            return 1;
        }
        if (strchr(letters_used_in_key, this_char) != NULL)
        {
            // Check that all characters are only used once
            // I don't need to check that they're all used once, only that none are used twice because there are 26 possibilities and 26 slots.
            printf("Only one of each letter is allowed! (You used %c twice!)\n", this_char);
            return 1;
        }
        letters_used_in_key[i] = this_char;
    }
    // Get plaintext
    string plaintext = get_string("plaintext:  ");
    if (strlen(plaintext) > STRLEN_ALLOCATED_IN_SWAP)
    {
        printf("Your plaintext is too long!\n");
        return 1;
    }
    // Encrypt
    char *result = perform_substitution(plaintext, key);
    // Present result
    printf("ciphertext: ");
    for (int i = 0, n = strlen(result); i < n; i++)
    {
        printf("%c", result[i]);
    }
    printf("\n");
}

// Substitute a single character
char substitute_char(char c, string k)
{
    if (isupper(c))
    {
        // If the character is uppercase, return the key index of that character:
        // The "- 'A'" gives the right index, because if the character is 'A', it would be the first character in the alphabet and therefore should the get the first character in the key.
        // 'A' - 'A' = 0!
        return toupper(k[c - 'A']);
    }
    else
    {
        // The same thing, but with lowercase characters:
        // 'a' - 'a' = 0.
        return tolower(k[c - 'a']);
    }
}

// k is the key, s is the input
string perform_substitution(string s, string k)
{
    // Just call "substitute_char" on every char in the string.
    char *output = (char *)malloc(sizeof(char) * STRLEN_ALLOCATED_IN_SWAP);
    output[0] = '\0';
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        char this_char = s[i];
        char to_append = this_char;
        if (isalpha(this_char))
        {
            to_append = substitute_char(this_char, k);
        }
        strncat(output, &to_append, 1);
    }
    return output;
}
