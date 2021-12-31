#include <stdio.h>
#include <cs50.h>

int main() {
    int n1, n2, max;
    printf("Enter two positive integers: ");
    n1 = get_int("");
    n2 = get_int("Enter the other positive integer: ")

    // maximum number between n1 and n2 is stored in max
    max = (n1 > n2) ? n1 : n2;

    while (1) {
        if (max % n1 == 0 && max % n2 == 0) {
            printf("The LCM of %d and %d is %d.", n1, n2, max);
            break;
        }
        max++;
    }
    return 0;
}
