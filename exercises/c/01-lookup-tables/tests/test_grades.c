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

#include "grades.h"

int main(void) {
    CHECK(letter_grade(100) == 'A');
    CHECK(letter_grade(90) == 'A');
    CHECK(letter_grade(89) == 'B');
    CHECK(letter_grade(80) == 'B');
    CHECK(letter_grade(75) == 'C');
    CHECK(letter_grade(60) == 'D');
    CHECK(letter_grade(59) == 'F');
    CHECK(letter_grade(0) == 'F');
    CHECK(letter_grade(-5) == 'F');

    CHECK_NEAR(grade_points(95), 4.0);
    CHECK_NEAR(grade_points(85), 3.0);
    CHECK_NEAR(grade_points(70), 2.0);
    CHECK_NEAR(grade_points(61), 1.0);
    CHECK_NEAR(grade_points(12), 0.0);

    int scores[] = {95, 82, 71, 64, 40};
    CHECK_NEAR(gpa(scores, 5), 2.0);
    CHECK_NEAR(gpa(scores, 2), 3.5);
    CHECK_NEAR(gpa(scores, 0), 0.0);
    CHECK_NEAR(gpa(NULL, 0), 0.0);

    CHECK(count_passing(scores, 5) == 4);
    CHECK(count_passing(scores + 4, 1) == 0);
    CHECK(count_passing(NULL, 0) == 0);

    FINISH();
}
