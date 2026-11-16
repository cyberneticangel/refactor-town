#ifndef LIBRARY_H
#define LIBRARY_H

#define MAX_BOOKS 50

#define LIB_OK 0
#define LIB_NOT_FOUND -1
#define LIB_UNAVAILABLE -2
#define LIB_FULL -3
#define LIB_NOT_CHECKED_OUT -4

typedef struct {
    char titles[MAX_BOOKS][64];
    int years[MAX_BOOKS];
    int available[MAX_BOOKS];
    int count;
} Library;

void library_init(Library *lib);
int library_add(Library *lib, const char *title, int year);
int library_checkout(Library *lib, const char *title);
int library_return(Library *lib, const char *title);
int library_count_available(const Library *lib);
const char *library_oldest(const Library *lib);

#endif
