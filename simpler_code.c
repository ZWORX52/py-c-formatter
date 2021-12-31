#include <stdio.h>
#include <cs50.h>

int main(int argc, string argv[])
{
    unsigned long long input = get_long_long("Input a number to square: ");
    printf("Your result is: %llu\n", input * input);
    return 0;
}
