#include "words.h"

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#define INITIAL_CAPACITY 4

/* Allocate a NUL-terminated copy of len bytes starting at start. */
static char *copy_word(const char *start, size_t len) {
    char *word = malloc(len + 1);
    if (word == NULL) {
        return NULL;
    }
    memcpy(word, start, len);
    word[len] = '\0';
    return word;
}

/* Double the array's capacity. On failure the old array is left untouched. */
static bool grow(char ***words, size_t *capacity) {
    size_t new_capacity = *capacity * 2;
    char **bigger = realloc(*words, new_capacity * sizeof **words);
    if (bigger == NULL) {
        return false;
    }
    *words = bigger;
    *capacity = new_capacity;
    return true;
}

char **split_words(const char *text, size_t *count) {
    size_t n = 0;
    size_t capacity = INITIAL_CAPACITY;
    char **words = malloc(capacity * sizeof *words);
    if (words == NULL) {
        goto fail;
    }

    const char *p = text;
    for (;;) {
        p += strspn(p, " ");           /* skip spaces */
        size_t len = strcspn(p, " ");  /* measure the word */
        if (len == 0) {
            break;
        }
        if (len > MAX_WORD_LEN || (n == capacity && !grow(&words, &capacity))) {
            goto fail;
        }
        words[n] = copy_word(p, len);
        if (words[n] == NULL) {
            goto fail;
        }
        n++;
        p += len;
    }
    *count = n;
    return words;

fail:
    /* Single exit for every error: release whatever we own so far. */
    free_words(words, n);
    *count = 0;
    return NULL;
}

void free_words(char **words, size_t count) {
    for (size_t i = 0; i < count; i++) {
        free(words[i]);
    }
    free(words);
}
