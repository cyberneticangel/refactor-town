#ifndef LIBRARY_H
#define LIBRARY_H

#include <stdbool.h>
#include <stddef.h>

#define MAX_BOOKS 50
#define TITLE_SIZE 64

typedef enum {
    LIB_OK = 0,
    LIB_NOT_FOUND = -1,
    LIB_UNAVAILABLE = -2,
    LIB_FULL = -3,
    LIB_NOT_CHECKED_OUT = -4,
} LibStatus;

typedef struct {
    char title[TITLE_SIZE];
    int year;
    bool available;
} Book;

typedef struct {
    Book books[MAX_BOOKS];
    size_t count;
} Library;

void library_init(Library *lib);
LibStatus library_add(Library *lib, const char *title, int year);
LibStatus library_checkout(Library *lib, const char *title);
LibStatus library_return(Library *lib, const char *title);
size_t library_count_available(const Library *lib);
const char *library_oldest(const Library *lib);

#endif
