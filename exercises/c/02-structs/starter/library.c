#include <string.h>

#include "library.h"

void library_init(Library *lib) {
    lib->count = 0;
}

int library_add(Library *lib, const char *title, int year) {
    if (lib->count == 50) {
        return -3;
    }
    strcpy(lib->titles[lib->count], title);
    lib->years[lib->count] = year;
    lib->available[lib->count] = 1;
    lib->count++;
    return 0;
}

int library_checkout(Library *lib, const char *title) {
    int i;
    for (i = 0; i < lib->count; i++) {
        if (strcmp(lib->titles[i], title) == 0) {
            if (lib->available[i] == 0) {
                return -2;
            }
            lib->available[i] = 0;
            return 0;
        }
    }
    return -1;
}

int library_return(Library *lib, const char *title) {
    int i;
    for (i = 0; i < lib->count; i++) {
        if (strcmp(lib->titles[i], title) == 0) {
            if (lib->available[i] == 1) {
                return -4;
            }
            lib->available[i] = 1;
            return 0;
        }
    }
    return -1;
}

int library_count_available(const Library *lib) {
    int i;
    int n = 0;
    for (i = 0; i < lib->count; i++) {
        if (lib->available[i] == 1) {
            n++;
        }
    }
    return n;
}

const char *library_oldest(const Library *lib) {
    int i;
    int best = -1;
    for (i = 0; i < lib->count; i++) {
        if (best == -1 || lib->years[i] < lib->years[best]) {
            best = i;
        }
    }
    if (best == -1) {
        return 0;
    }
    return lib->titles[best];
}
