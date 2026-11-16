#ifndef GRADES_H
#define GRADES_H

#include <stddef.h>

char letter_grade(int score);
double grade_points(int score);
double gpa(const int *scores, size_t count);
size_t count_passing(const int *scores, size_t count);

#endif
