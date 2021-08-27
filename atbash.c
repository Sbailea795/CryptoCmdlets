#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <io.h>

void usage(void);
void atbash(char *);

int main(int argc, char **argv)
{
    if (argc > 1)
    {
        for (int args = 1; args < argc; args++)
        {
            atbash(argv[args]);
        }
        return EXIT_SUCCESS;
    }
    else if (!_isatty(_fileno(stdin)))
    {
        char *flag;
        while (scanf("%s", flag) == 1)
        {
            atbash(flag);
        }
    }
    else
    {
        usage();
    }
}

void atbash(char *text)
{
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] >= 0x41 && text[i] <= 0x122)
        {
            text[i] = 122 - tolower(text[i]) + 97;
        }
    }
    fprintf(stdout, "%s\n", text);
}

void usage()
{
    fprintf(stdout, "Usage: atbash.exe [Phrase1] [Phrase2]...\n");
    exit(EXIT_FAILURE);
}