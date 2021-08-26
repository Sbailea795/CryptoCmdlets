#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>

#define alphabet "abcdefghijklmnopqrstuvwxyz"
#define tebahpla "zyxwvutsrqponmlkjihgfedcba"
int main(int argc, char **argv)
{
    if(argc == 2)
    {
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if(argv[1][i] >= 0x41 && argv[1][i] <= 0x122)
            {
                argv[1][i] = 122 - tolower(argv[1][i]) + 97;
            }
        }
        printf("%s\n", argv[1]);
        return EXIT_SUCCESS;
    }
    else
    {
        printf("Usage: atbash.exe <Phrase>\n");
        return EXIT_FAILURE;
    }
}