#ifndef WORDS_H
#define WORDS_H

#include <stddef.h>

#define MAX_WORD_LEN 15

/* Split text on spaces into a newly allocated array of newly allocated words.
 * On success: returns the array and sets *count (the array may hold 0 words).
 * If any word is longer than MAX_WORD_LEN: returns NULL and sets *count to 0.
 * The caller releases a successful result with free_words(). */
char **split_words(const char *text, size_t *count);

void free_words(char **words, size_t count);

#endif
