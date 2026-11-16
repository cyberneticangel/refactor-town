import { test } from "node:test";
import assert from "node:assert/strict";
import { area, perimeter, describe } from "./shapes.mjs";

const close = (a, b) => assert.ok(Math.abs(a - b) < 1e-9, `${a} ≈ ${b}`);

test("circle", () => {
  close(area({ kind: "circle", radius: 2 }), 4 * Math.PI);
  close(perimeter({ kind: "circle", radius: 2 }), 4 * Math.PI);
});

test("rectangle", () => {
  assert.equal(area({ kind: "rectangle", width: 3, height: 4 }), 12);
  assert.equal(perimeter({ kind: "rectangle", width: 3, height: 4 }), 14);
});

test("triangle", () => {
  close(area({ kind: "triangle", a: 3, b: 4, c: 5 }), 6);
  assert.equal(perimeter({ kind: "triangle", a: 3, b: 4, c: 5 }), 12);
});

test("describe", () => {
  assert.equal(describe({ kind: "rectangle", width: 2, height: 5 }), "rectangle: area 10.00, perimeter 14.00");
  assert.equal(describe({ kind: "circle", radius: 1 }), "circle: area 3.14, perimeter 6.28");
});

test("unknown kinds throw", () => {
  for (const fn of [area, perimeter, describe]) {
    assert.throws(() => fn({ kind: "hexagon" }), /unknown shape: hexagon/);
    assert.throws(() => fn({ kind: "toString" }), /unknown shape: toString/);
  }
});
