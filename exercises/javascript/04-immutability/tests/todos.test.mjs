import { test } from "node:test";
import assert from "node:assert/strict";
import { reducer, initialState } from "./todos.mjs";

function run(...actions) {
  return actions.reduce(reducer, structuredClone(initialState));
}

test("add assigns increasing ids", () => {
  const s = run({ type: "add", text: "milk" }, { type: "add", text: "eggs" });
  assert.deepEqual(s, {
    todos: [
      { id: 1, text: "milk", done: false },
      { id: 2, text: "eggs", done: false },
    ],
    nextId: 3,
  });
});

test("toggle flips one todo", () => {
  const s = run({ type: "add", text: "a" }, { type: "add", text: "b" }, { type: "toggle", id: 2 });
  assert.deepEqual(s.todos.map((t) => t.done), [false, true]);
});

test("remove and clearDone", () => {
  const s = run(
    { type: "add", text: "a" }, { type: "add", text: "b" }, { type: "add", text: "c" },
    { type: "toggle", id: 1 }, { type: "toggle", id: 3 }, { type: "remove", id: 2 },
  );
  assert.deepEqual(s.todos.map((t) => t.text), ["a", "c"]);
  assert.deepEqual(reducer(s, { type: "clearDone" }).todos, []);
});

test("unknown actions return the same state", () => {
  const s = run({ type: "add", text: "a" });
  assert.equal(reducer(s, { type: "nope" }), s);
});

test("does not mutate the previous state (add)", () => {
  const before = run({ type: "add", text: "a" });
  const snapshot = structuredClone(before);
  const after = reducer(before, { type: "add", text: "b" });
  assert.deepEqual(before, snapshot);
  assert.notEqual(after, before);
});

test("does not mutate the previous state (toggle/remove/clearDone)", () => {
  const before = run({ type: "add", text: "a" }, { type: "add", text: "b" }, { type: "toggle", id: 1 });
  const snapshot = structuredClone(before);
  reducer(before, { type: "toggle", id: 2 });
  reducer(before, { type: "remove", id: 1 });
  reducer(before, { type: "clearDone" });
  assert.deepEqual(before, snapshot);
});

test("undo works by keeping old states", () => {
  const history = [structuredClone(initialState)];
  const actions = [{ type: "add", text: "write tests" }, { type: "toggle", id: 1 }, { type: "remove", id: 1 }];
  for (const action of actions) history.push(reducer(history.at(-1), action));
  assert.deepEqual(history.map((s) => s.todos.length), [0, 1, 1, 0]);
  assert.equal(history[1].todos[0].done, false);
  assert.equal(history[2].todos[0].done, true);
});
