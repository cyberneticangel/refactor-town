#ifndef RECEIPT_H
#define RECEIPT_H

#include <stddef.h>

typedef struct {
    const char *name;
    int qty;
    int cents; /* unit price */
} Item;

/* Write a receipt into out, which has room for out_size bytes.
 * The result is always NUL-terminated (if out_size > 0) and is truncated
 * if the buffer is too small. */
void format_receipt(char *out, size_t out_size, const Item *items, size_t count);

#endif
