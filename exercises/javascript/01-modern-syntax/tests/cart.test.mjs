import { test } from "node:test";
import assert from "node:assert/strict";
import { cartSummary } from "./cart.mjs";

const cart = [
  { name: "apple", price: 0.5, qty: 6, inStock: true },
  { name: "bread", price: 3.25, qty: 1, inStock: true },
  { name: "caviar", price: 99, qty: 1, inStock: false },
  { name: "milk", price: 1.2, qty: 2, inStock: true },
];

test("summarises in-stock items", () => {
  const s = cartSummary(cart);
  assert.ok(Math.abs(s.total - 8.65) < 1e-9);
  assert.equal(s.count, 9);
  assert.deepEqual(s.names, ["APPLE", "BREAD", "MILK"]);
});

test("empty cart", () => {
  assert.deepEqual(cartSummary([]), { total: 0, count: 0, names: [] });
});

test("nothing in stock", () => {
  assert.deepEqual(cartSummary([cart[2]]), { total: 0, count: 0, names: [] });
});

test("does not modify the input", () => {
  const copy = structuredClone(cart);
  cartSummary(cart);
  assert.deepEqual(cart, copy);
});

test("returns exactly total, count and names", () => {
  assert.deepEqual(Object.keys(cartSummary(cart)).sort(), ["count", "names", "total"]);
});
