export function area(shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius * shape.radius;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle": {
      const s = (shape.a + shape.b + shape.c) / 2;
      return Math.sqrt(s * (s - shape.a) * (s - shape.b) * (s - shape.c));
    }
    default:
      throw new Error("unknown shape: " + shape.kind);
  }
}

export function perimeter(shape) {
  switch (shape.kind) {
    case "circle":
      return 2 * Math.PI * shape.radius;
    case "rectangle":
      return 2 * (shape.width + shape.height);
    case "triangle":
      return shape.a + shape.b + shape.c;
    default:
      throw new Error("unknown shape: " + shape.kind);
  }
}

export function describe(shape) {
  switch (shape.kind) {
    case "circle":
    case "rectangle":
    case "triangle":
      return shape.kind + ": area " + area(shape).toFixed(2) + ", perimeter " + perimeter(shape).toFixed(2);
    default:
      throw new Error("unknown shape: " + shape.kind);
  }
}
