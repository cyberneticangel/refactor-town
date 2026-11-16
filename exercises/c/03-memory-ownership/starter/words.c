#include <stdlib.h>

#include "words.h"

char **split_words(const char *text, size_t *count) {
    int cap = 4;
    int n = 0;
    char **words = malloc(sizeof(char *) * cap);
    int i = 0;
    while (text[i] != '\0') {
        while (text[i] == ' ') {
            i++;
        }
        if (text[i] == '\0') {
            break;
        }
        int start = i;
        while (text[i] != ' ' && text[i] != '\0') {
            i++;
        }
        int len = i - start;
        if (len > MAX_WORD_LEN) {
            *count = 0;
            return NULL;
        }
        if (n == cap) {
            cap = cap * 2;
            words = realloc(words, sizeof(char *) * cap);
        }
        char *w = malloc(len + 1);
        int j;
        for (j = 0; j < len; j++) {
            w[j] = text[start + j];
        }
        w[len] = '\0';
        words[n] = w;
        n++;
    }
    *count = n;
    return words;
}

void free_words(char **words, size_t count) {
    size_t i;
    for (i = 0; i < count; i++) {
        free(words[i]);
    }
    free(words);
}
