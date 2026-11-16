#include <stdio.h>
#include <stdlib.h>
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

#include "receipt.h"

static const Item ITEMS[] = {
    {"Coffee", 3, 450},
    {"Bagel", 2, 225},
    {"Orange juice", 1, 399},
};

static const char *FULL =
    "RECEIPT\n"
    " 3 x Coffee       $  13.50\n"
    " 2 x Bagel        $   4.50\n"
    " 1 x Orange juice $   3.99\n"
    "TOTAL             $  21.99\n";

int main(void) {
    char big[512];
    format_receipt(big, sizeof big, ITEMS, 3);
    CHECK_STR(big, FULL);

    format_receipt(big, sizeof big, ITEMS, 0);
    CHECK_STR(big, "RECEIPT\nTOTAL             $   0.00\n");

    /* long names are printed in full when there's room */
    const Item fancy[] = {{"Single-origin Ethiopian pour-over with oat milk foam", 1, 1250}};
    format_receipt(big, sizeof big, fancy, 1);
    CHECK_STR(big,
              "RECEIPT\n"
              " 1 x Single-origin Ethiopian pour-over with oat milk foam $  12.50\n"
              "TOTAL             $  12.50\n");

    /* a small buffer: truncated, NUL-terminated, and nothing written past the end */
    struct {
        char buf[32];
        char guard[16];
    } small;
    memset(&small, '#', sizeof small);
    format_receipt(small.buf, sizeof small.buf, ITEMS, 3);
    CHECK(strlen(small.buf) == 31);
    CHECK(strncmp(small.buf, FULL, 31) == 0);
    for (size_t i = 0; i < sizeof small.guard; i++) {
        CHECK(small.guard[i] == '#');
    }

    /* every possible size, including 1 */
    for (size_t size = 1; size < 140; size++) {
        char *exact = malloc(size);
        format_receipt(exact, size, ITEMS, 3);
        size_t expect = strlen(FULL) < size - 1 ? strlen(FULL) : size - 1;
        CHECK(strlen(exact) == expect);
        free(exact);
    }

    /* size 0 must not write anything */
    char untouched = 'x';
    format_receipt(&untouched, 0, ITEMS, 3);
    CHECK(untouched == 'x');

    FINISH();
}
