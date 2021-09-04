#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <io.h>

#define GET(N) { if(fscanf(f##N,"%d",&b##N ) != 1) f##N = NULL; }
#define PUT(N) { printf("%d\n", b##N); GET(N) }

void usage(void);
void scytale(bool, int, char*);
void merge(FILE*, FILE*);
void merge(FILE *Appended, FILE *Appendee)
{
    while (fscanf(Appendee, Appended) != 1) fputc(getc(Appended), Appendee);
}
int main(int argc, char **argv)
{
    FILE *fp1 = malloc(sizeof(char) * 1024 * 10);
    FILE *fp2;
    if (argc > 1){
        fp2 = fopen(argv[1],"r");
        for (int i = 1; i < argc; i++)
        {
            merge(fp1, fopen(argv[i],"r"));
        } 
    }
    fp2 = stdin;
    merge(fp1, fp2);
    bool decrypt = true;
    char *charPtr;
    int polygonalSize;
        char *flag;
        if( !(fscanf(fp1,"%s", &flag) == 1 && strcmp(flag, "-s")) ) usage();
        if( !(fscanf(fp1,"%s", flag) == 1) ) usage();
        polygonalSize = strtol(flag, &charPtr, 10);
        if (*charPtr != 0) usage();
        if( !(fscanf(fp1, "%s", flag) == 1) ) usage();
        if ( strcmp(flag, "-r") ){
            decrypt = true;
            if ( !(fscanf(fp1, "%s", flag) == 1) ) usage();
        }
        do
        {
            scytale(decrypt, polygonalSize, flag);
        }
        while (fscanf(fp1, "%s", flag) == 1);

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