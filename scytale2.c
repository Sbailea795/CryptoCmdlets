#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <io.h>

void usage(void);
void scytale(bool, int, char*);
int main(int argc, char **argv)
{
    bool decrypt = true;
    char *charPtr;
    int polygonalSize;
    if (argc > 3)
    {
        if (strcmp(argv[1], "-s") != 0) usage();
        polygonalSize = strtol(argv[2], &charPtr, 10);
        if (*charPtr != 0) usage();
        if (strcmp(argv[3], "-r") == 0) decrypt = true;
        for (int args = (decrypt) ? 4 : 3; args < argc; args++)
        {
            scytale(decrypt, polygonalSize, argv[args]);
        }
        return EXIT_SUCCESS;
    }
    else if (!_isatty(_fileno(stdin)))
    {
        char *flag;
        if( !(scanf("%s", flag) == 1 && strcmp(flag, "-s")) ) usage();
        if( !(scanf("%s", flag) == 1) ) usage();
        polygonalSize = strtol(flag, &charPtr, 10);
        if (*charPtr != 0) usage();
        if( !(scanf("%s", flag) == 1) ) usage();
        if ( strcmp(flag, "-r") ){
            decrypt = true;
            if ( !(scanf("%s", flag) == 1) ) usage();
        }
        do
        {
            scytale(decrypt, polygonalSize, flag);
        }
        while (scanf("%s", flag) == 1);
    }
    else
    {
        usage();
    }
    return EXIT_SUCCESS;
}

void scytale(bool reverse, int size, char* text)
{
    
    int counter = 0;
    int columns = size;
    int rows = ceil((double)strlen(text)/size);
    char *scytaleTable;
    if(reverse)
    {
        char *scytaleTable = malloc(sizeof(columns * rows));
        scytaleTable[0] = '\0';
        for (int column = 0; column < columns; column++)
        {
            for (int row = 0; row < rows; row++)
            {
                scytaleTable[column * rows + row] = *(text+counter++);
            }
            
        }
        for (int row = 0; row < rows; row++)
        {
            for (int column = 0; column < columns; column++)
            {
                fprintf(stdout, "%c", scytaleTable[column * rows + row]);
            }
        }
        fprintf(stdout, "\n");
    }
    else
    {
        char *scytale = (char *)malloc(sizeof(text));
        scytale[0] = '\0';
        for (int faces = 0; faces < size; faces++)
        {
            for (int index = faces; index < strlen(text); index += size)
            {
                *(scytale + counter++) = text[index];
            }
        }
        *(scytale + counter) = '\0';
        fprintf(stdout, "%s\n", scytale);
    }
    free(scytaleTable);
}

void usage()
{
  printf("Usage: scytale -s <Size> [-r] <Text1> [Text2]...\n\n");
  printf("  -s: size - sets the gap between letters. functionally -s denotes the sides of a polygon, wherein scytale reads across the first face.\n");
  printf("  -r: reverse - reads scytale with the key of <Size>\n\n");
  exit(EXIT_FAILURE);
}