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
    if (strcmp(argv[1], "-s") != 0) usage();
    int polygonalSize; char *charPtr; bool decrypt = false;
    polygonalSize = strtol(argv[2], &charPtr, 10);
    if (*charPtr != 0 || polygonalSize < 1) usage();
    if (argc >= 4 && strcmp(argv[3], "-r") == 0 ) decrypt = true;
    for (int i = (decrypt ? 4 : 3); i < argc; i++)
    {
        scytale(decrypt, polygonalSize, argv[i]);
    }
    /*
    printf("testing loop");
    char flag[1024];
    FILE *test = fopen(stdin, "a");
    fputs( (int*) EOF, test);
    close(test);
    printf("testing loop");
    while (fgetc(stdin))
    {
        fgets(flag, sizeof(flag), stdin);
        printf("flag:%s", flag);
        scytale(decrypt, polygonalSize, flag);

    }
    /**/
    fprintf(stdout, "%S" ,EOF);
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