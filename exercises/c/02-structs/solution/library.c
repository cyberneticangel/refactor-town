#include "library.h"

#include <stdio.h>
#include <string.h>

void library_init(Library *lib) {
    lib->count = 0;
}

LibStatus library_add(Library *lib, const char *title, int year) {
    if (lib->count == MAX_BOOKS) {
        return LIB_FULL;
    }
    Book *book = &lib->books[lib->count++];
    snprintf(book->title, sizeof book->title, "%s", title); /* truncates safely */
    book->year = year;
    book->available = true;
    return LIB_OK;
}

static Book *find_book(Library *lib, const char *title) {
    for (size_t i = 0; i < lib->count; i++) {
        if (strcmp(lib->books[i].title, title) == 0) {
            return &lib->books[i];
        }
    }
    return NULL;
}

LibStatus library_checkout(Library *lib, const char *title) {
    Book *book = find_book(lib, title);
    if (book == NULL) {
        return LIB_NOT_FOUND;
    }
    if (!book->available) {
        return LIB_UNAVAILABLE;
    }
    book->available = false;
    return LIB_OK;
}

LibStatus library_return(Library *lib, const char *title) {
    Book *book = find_book(lib, title);
    if (book == NULL) {
        return LIB_NOT_FOUND;
    }
    if (book->available) {
        return LIB_NOT_CHECKED_OUT;
    }
    book->available = true;
    return LIB_OK;
}

size_t library_count_available(const Library *lib) {
    size_t available = 0;
    for (size_t i = 0; i < lib->count; i++) {
        available += lib->books[i].available;
    }
    return available;
}

const char *library_oldest(const Library *lib) {
    const Book *oldest = NULL;
    for (size_t i = 0; i < lib->count; i++) {
        const Book *book = &lib->books[i];
        if (oldest == NULL || book->year < oldest->year) {
            oldest = book;
        }
    }
    return oldest ? oldest->title : NULL;
}
