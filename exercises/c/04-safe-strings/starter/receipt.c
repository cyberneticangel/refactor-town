#include <stdio.h>
#include <string.h>

#include "receipt.h"

void format_receipt(char *out, size_t out_size, const Item *items, size_t count) {
    char line[48];
    int total = 0;
    size_t i;
    (void)out_size;
    strcpy(out, "RECEIPT\n");
    for (i = 0; i < count; i++) {
        int line_cents = items[i].qty * items[i].cents;
        total = total + line_cents;
        sprintf(line, "%2d x %-12s $%4d.%02d\n", items[i].qty, items[i].name,
                line_cents / 100, line_cents % 100);
        strcat(out, line);
    }
    sprintf(line, "TOTAL             $%4d.%02d\n", total / 100, total % 100);
    strcat(out, line);
}
