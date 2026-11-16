export const initialState = { todos: [], nextId: 1 };

export function reducer(state, action) {
  switch (action.type) {
    case "add": {
      const todo = { id: state.nextId, text: action.text, done: false };
      return { ...state, todos: [...state.todos, todo], nextId: state.nextId + 1 };
    }
    case "toggle":
      return {
        ...state,
        todos: state.todos.map((t) => (t.id === action.id ? { ...t, done: !t.done } : t)),
      };
    case "remove":
      return { ...state, todos: state.todos.filter((t) => t.id !== action.id) };
    case "clearDone":
      return { ...state, todos: state.todos.filter((t) => !t.done) };
    default:
      return state;
  }
}
