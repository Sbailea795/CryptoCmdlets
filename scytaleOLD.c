#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

void usage(void);

int main(int argc, char *argv[])
{
  int opt;
  int counter = 0;
  char *charPtr;
  bool readCypher = false;
  int argStart = 3;
  int polygonalSize;
  char *argPtr;
  if (strcmp(argv[1], "-s") != 0)
    usage();
  if (strcmp(argv[3], "-r") == 0)
  {
    argStart++;
    readCypher++;
  }
  polygonalSize = strtol(argv[2], &charPtr, 10);
  if (*charPtr != 0)
    usage();
  argPtr = argv[argStart];
  if (!readCypher)
  {
    for (int args = argStart; args < argc; args++)
    {
      argPtr = argv[argStart];
      char *scytale;
      scytale = (char *)malloc(512 * sizeof(char));
      scytale[0] = '\0';
      for (int size = 0; size < polygonalSize; size++)
      {
        for (int index = size; index < strlen(argPtr); index += polygonalSize)
        {
          *(scytale + counter++) = argPtr[index];
          printf("%c\n", argPtr[index]);
        }
      }
      *(scytale + counter) = '\0';
      printf("%s\n", scytale);
    }
  }
  else
  {
    for (int args = argStart; args < argc; args++)
    {
      argPtr = argv[argStart];
      char *scytale;
      scytale = (char *)malloc(512 * sizeof(char));
      scytale[0] = '\0';
      int passes = ceil((double)strlen(argPtr) / polygonalSize);
      for (int size = 0; size <= polygonalSize; size++)
      {
        for (int index = size; index < strlen(argPtr); index += passes)
        {
          *(scytale + counter++) = argPtr[index];
        }
      }
      *(scytale + counter) = '\0';
      fprintf(stdout, "%s\n", scytale);
    }
  }
  return EXIT_SUCCESS;
}

void usage()
{
  printf("Usage: scytale -s <Size> [-r] <Text1> [Text2]...\n\n");
  printf("  -s: size - sets the gap between letters. functionally -s denotes the sides of a polygon, wherein scytale reads across the first face.\n");
  printf("  -r: reverse - reads scytale with the key of <Size>\n\n");
  exit(EXIT_FAILURE);
}