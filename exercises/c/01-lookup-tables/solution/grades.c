#include "grades.h"

#include <stdbool.h>

typedef struct {
    int min_score;
    char letter;
    double points;
} GradeBand;

/* Highest band first; the last band catches everything. */
static const GradeBand GRADE_BANDS[] = {
    {90, 'A', 4.0},
    {80, 'B', 3.0},
    {70, 'C', 2.0},
    {60, 'D', 1.0},
    {0, 'F', 0.0},
};
static const size_t BAND_COUNT = sizeof GRADE_BANDS / sizeof GRADE_BANDS[0];
static const char FAILING_LETTER = 'F';

static const GradeBand *band_for(int score) {
    for (size_t i = 0; i < BAND_COUNT - 1; i++) {
        if (score >= GRADE_BANDS[i].min_score) {
            return &GRADE_BANDS[i];
        }
    }
    return &GRADE_BANDS[BAND_COUNT - 1];
}

char letter_grade(int score) {
    return band_for(score)->letter;
}

double grade_points(int score) {
    return band_for(score)->points;
}

double gpa(const int *scores, size_t count) {
    if (count == 0) {
        return 0;
    }
    double total = 0;
    for (size_t i = 0; i < count; i++) {
        total += grade_points(scores[i]);
    }
    return total / count;
}

static bool is_passing(int score) {
    return letter_grade(score) != FAILING_LETTER;
}

size_t count_passing(const int *scores, size_t count) {
    size_t passing = 0;
    for (size_t i = 0; i < count; i++) {
        passing += is_passing(scores[i]);
    }
    return passing;
}
