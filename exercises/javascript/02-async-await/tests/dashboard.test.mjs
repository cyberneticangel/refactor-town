import { test } from "node:test";
import assert from "node:assert/strict";
import { loadDashboard } from "./dashboard.mjs";

test("loads a user's dashboard with lines in order", async () => {
  const d = await loadDashboard(1);
  assert.deepEqual(d, {
    name: "Ada",
    lines: [
      { title: "Keyboard", qty: 2, cost: 100 },
      { title: "Monitor", qty: 1, cost: 180 },
    ],
    total: 280,
  });
});

test("order is stable across many runs (random API latency)", async () => {
  for (let i = 0; i < 10; i++) {
    const d = await loadDashboard(1);
    assert.deepEqual(d.lines.map((l) => l.title), ["Keyboard", "Monitor"]);
  }
});

test("user with no orders", async () => {
  assert.deepEqual(await loadDashboard(2), { name: "Alan", lines: [], total: 0 });
});

test("unknown user rejects with the API error", async () => {
  await assert.rejects(loadDashboard(99), /no user 99/);
});

test("returns a promise", () => {
  const p = loadDashboard(1);
  assert.ok(p instanceof Promise);
  return p;
});
