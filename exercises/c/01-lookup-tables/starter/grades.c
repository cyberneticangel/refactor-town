#include "grades.h"

char letter_grade(int s) {
    if (s >= 90) {
        return 'A';
    } else if (s >= 80) {
        return 'B';
    } else if (s >= 70) {
        return 'C';
    } else if (s >= 60) {
        return 'D';
    } else {
        return 'F';
    }
}

double grade_points(int s) {
    if (s >= 90) {
        return 4.0;
    } else if (s >= 80) {
        return 3.0;
    } else if (s >= 70) {
        return 2.0;
    } else if (s >= 60) {
        return 1.0;
    } else {
        return 0.0;
    }
}

double gpa(int *s, int n) {
    double t = 0;
    int i;
    if (n == 0) {
        return 0;
    }
    for (i = 0; i < n; i++) {
        t = t + grade_points(s[i]);
    }
    return t / n;
}

int count_passing(int *s, int n) {
    int c = 0;
    int i;
    for (i = 0; i < n; i++) {
        if (s[i] >= 60) {
            c++;
        }
    }
    return c;
}
