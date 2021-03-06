#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <cs50.h>

#define STRLEN_ALLOCATED_IN_SWAP 8192

char substitute_char(char c, string k);

string perform_substitution(string s, string k);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution <key>\n");
        return 1;
    }
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters\n");
        return 1;
    }
    string key = argv[1];
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
            printf("Only one of each letter is allowed! (You used %c twice!)\n", this_char);
            return 1;
        }
        letters_used_in_key[i] = this_char;
    }
    string plaintext = get_string("plaintext:  ");
    if (strlen(plaintext) > STRLEN_ALLOCATED_IN_SWAP)
    {
        printf("Your plaintext is too long!\n");
        return 1;
    }
    char *result = perform_substitution(plaintext, key);
    printf("ciphertext: ");
    for (int i = 0, n = strlen(result); i < n; i++)
    {
        printf("%c", result[i]);
    }
    printf("\n");
    return 0;
}

char substitute_char(char c, string k)
{
    if (isupper(c))
    {
        return toupper(k[c - 'A']);
    }
    else
    {
        return tolower(k[c - 'a']);
    }
}

string perform_substitution(string s, string k)
{
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
