export const initialState = { todos: [], nextId: 1 };

export function reducer(state, action) {
  switch (action.type) {
    case "add":
      state.todos.push({ id: state.nextId, text: action.text, done: false });
      state.nextId++;
      return state;

    case "toggle":
      for (let i = 0; i < state.todos.length; i++) {
        if (state.todos[i].id === action.id) {
          state.todos[i].done = !state.todos[i].done;
        }
      }
      return state;

    case "remove":
      for (let i = 0; i < state.todos.length; i++) {
        if (state.todos[i].id === action.id) {
          state.todos.splice(i, 1);
          break;
        }
      }
      return state;

    case "clearDone":
      for (let i = state.todos.length - 1; i >= 0; i--) {
        if (state.todos[i].done) {
          state.todos.splice(i, 1);
        }
      }
      return state;

    default:
      return state;
  }
}
