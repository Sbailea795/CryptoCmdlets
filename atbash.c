#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <ctype.h>

#define alphabet "abcdefghijklmnopqrstuvwxyz"
#define tebahpla "zyxwvutsrqponmlkjihgfedcba"
int main(int argc, char **argv)
{
    if(argc > 1)
    {
        for (int args = 1; args < argc; args++)
        {
            char *argPtr = argv[args];
            for (int i = 0; i < strlen(argPtr); i++)
            {
                if(argPtr[i] >= 0x41 && argPtr[i] <= 0x122)
                {
                    argPtr[i] = 122 - tolower(argPtr[i]) + 97;
                }
        }
        printf("%s\n", argPtr);
        }
        return EXIT_SUCCESS;
    }
    else
    {
        printf("Usage: atbash.exe [Phrase1] [Phrase2]...\n");
        return EXIT_FAILURE;
    }
}