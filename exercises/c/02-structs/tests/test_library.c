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

#include "library.h"

int main(void) {
    Library lib;
    library_init(&lib);
    CHECK(library_oldest(&lib) == NULL);
    CHECK(library_count_available(&lib) == 0);

    CHECK(library_add(&lib, "Dune", 1965) == LIB_OK);
    CHECK(library_add(&lib, "Neuromancer", 1984) == LIB_OK);
    CHECK(library_add(&lib, "Frankenstein", 1818) == LIB_OK);
    CHECK(library_add(&lib, "Emma", 1815) == LIB_OK);
    CHECK(library_count_available(&lib) == 4);
    CHECK_STR(library_oldest(&lib), "Emma");

    CHECK(library_checkout(&lib, "Dune") == LIB_OK);
    CHECK(library_checkout(&lib, "Dune") == LIB_UNAVAILABLE);
    CHECK(library_checkout(&lib, "Ulysses") == LIB_NOT_FOUND);
    CHECK(library_count_available(&lib) == 3);

    CHECK(library_return(&lib, "Dune") == LIB_OK);
    CHECK(library_return(&lib, "Dune") == LIB_NOT_CHECKED_OUT);
    CHECK(library_return(&lib, "Ulysses") == LIB_NOT_FOUND);
    CHECK(library_count_available(&lib) == 4);

    /* checked-out books still count for "oldest" */
    CHECK(library_checkout(&lib, "Emma") == LIB_OK);
    CHECK_STR(library_oldest(&lib), "Emma");

    /* ties keep the first one added */
    Library ties;
    library_init(&ties);
    library_add(&ties, "First", 2000);
    library_add(&ties, "Second", 2000);
    CHECK_STR(library_oldest(&ties), "First");

    /* capacity */
    Library full;
    library_init(&full);
    char title[16];
    for (int i = 0; i < MAX_BOOKS; i++) {
        snprintf(title, sizeof title, "Book %d", i);
        CHECK(library_add(&full, title, 1900 + i) == LIB_OK);
    }
    CHECK(library_add(&full, "One too many", 2024) == LIB_FULL);
    CHECK(library_count_available(&full) == MAX_BOOKS);
    CHECK(library_checkout(&full, "Book 49") == LIB_OK);

    FINISH();
}
