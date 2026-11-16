#include "receipt.h"

#include <stdarg.h>
#include <stdio.h>

#define CENTS_PER_DOLLAR 100

/* A bounded output buffer: never writes past size, always NUL-terminated. */
typedef struct {
    char *buf;
    size_t size;
    size_t len; /* characters written so far (excluding the NUL) */
} Writer;

static void writer_init(Writer *w, char *buf, size_t size) {
    *w = (Writer){buf, size, 0};
    if (size > 0) {
        buf[0] = '\0';
    }
}

static void append(Writer *w, const char *fmt, ...) {
    if (w->size == 0) {
        return;
    }
    size_t room = w->size - w->len;
    va_list args;
    va_start(args, fmt);
    int wanted = vsnprintf(w->buf + w->len, room, fmt, args);
    va_end(args);
    if (wanted < 0) {
        return;
    }
    /* vsnprintf truncates for us; only advance by what actually fit */
    w->len += (size_t)wanted < room ? (size_t)wanted : room - 1;
}

static void append_money(Writer *w, int cents) {
    append(w, "$%4d.%02d\n", cents / CENTS_PER_DOLLAR, cents % CENTS_PER_DOLLAR);
}

void format_receipt(char *out, size_t out_size, const Item *items, size_t count) {
    Writer w;
    writer_init(&w, out, out_size);
    append(&w, "RECEIPT\n");

    int total = 0;
    for (size_t i = 0; i < count; i++) {
        int line_cents = items[i].qty * items[i].cents;
        total += line_cents;
        append(&w, "%2d x %-12s ", items[i].qty, items[i].name);
        append_money(&w, line_cents);
    }
    append(&w, "TOTAL             ");
    append_money(&w, total);
}
