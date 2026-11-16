#include <stdio.h>
#include <string.h>

/* ---- tiny test runner ---------------------------------------------------- */
static int checks = 0, failures = 0;
#define CHECK(cond) do { checks++; if (!(cond)) { failures++; \
    printf("  FAIL %s:%d: %s\n", __FILE__, __LINE__, #cond); } } while (0)
#define CHECK_NEAR(a, b) CHECK(((a) - (b)) < 1e-9 && ((b) - (a)) < 1e-9)
#define CHECK_STR(a, b) do { checks++; if (strcmp((a), (b)) != 0) { failures++; \
    printf("  FAIL %s:%d: expected\n\"%s\"\n  got\n\"%s\"\n", __FILE__, __LINE__, (b), (a)); } } while (0)
#define FINISH() do { printf("%d checks, %d failed\n", checks, failures); return failures != 0; } while (0)
/* Unbuffered output, so results still appear if a sanitizer aborts the run. */
__attribute__((constructor)) static void unbuffered_stdout(void) { setvbuf(stdout, NULL, _IONBF, 0); }
/* -------------------------------------------------------------------------- */

/* Provided by AddressSanitizer's runtime (we build with -fsanitize=address). */
size_t __sanitizer_get_current_allocated_bytes(void);

#include "words.h"

int main(void) {
    size_t count = 99;
    char **words = split_words("  the quick  brown fox ", &count);
    CHECK(words != NULL);
    CHECK(count == 4);
    if (words && count == 4) {
        CHECK_STR(words[0], "the");
        CHECK_STR(words[1], "quick");
        CHECK_STR(words[2], "brown");
        CHECK_STR(words[3], "fox");
    }
    free_words(words, count);

    /* growth past the initial capacity */
    words = split_words("a b c d e f g h i j k l m n o p q r s t", &count);
    CHECK(count == 20);
    if (words && count == 20) {
        CHECK_STR(words[19], "t");
    }
    free_words(words, count);

    /* exactly MAX_WORD_LEN is fine */
    words = split_words("fifteen_letters", &count);
    CHECK(words != NULL && count == 1);
    free_words(words, count);

    /* nothing to split */
    words = split_words("", &count);
    CHECK(words != NULL && count == 0);
    free_words(words, count);
    words = split_words("     ", &count);
    CHECK(words != NULL && count == 0);
    free_words(words, count);

    /* too-long word after several good ones (and after the array has grown):
     * must return NULL, set count to 0, and NOT LEAK anything allocated so far. */
    size_t heap_before = __sanitizer_get_current_allocated_bytes();
    count = 99;
    words = split_words("one two three four five six sixteen_letters! seven", &count);
    size_t leaked = __sanitizer_get_current_allocated_bytes() - heap_before;
    CHECK(words == NULL);
    CHECK(count == 0);
    if (leaked != 0) {
        printf("  split_words leaked %zu bytes when it gave up on the long word\n", leaked);
    }
    CHECK(leaked == 0);

    /* free_words(NULL, 0) must be harmless */
    free_words(NULL, 0);

    FINISH();  /* LeakSanitizer also checks for leaks after main returns */
}
