const SHAPES = {
  circle: {
    area: ({ radius }) => Math.PI * radius ** 2,
    perimeter: ({ radius }) => 2 * Math.PI * radius,
  },
  rectangle: {
    area: ({ width, height }) => width * height,
    perimeter: ({ width, height }) => 2 * (width + height),
  },
  triangle: {
    // Heron's formula
    area: ({ a, b, c }) => {
      const s = (a + b + c) / 2;
      return Math.sqrt(s * (s - a) * (s - b) * (s - c));
    },
    perimeter: ({ a, b, c }) => a + b + c,
  },
};

function behaviourFor(shape) {
  if (!Object.hasOwn(SHAPES, shape.kind)) {
    throw new Error(`unknown shape: ${shape.kind}`);
  }
  return SHAPES[shape.kind];
}

export const area = (shape) => behaviourFor(shape).area(shape);
export const perimeter = (shape) => behaviourFor(shape).perimeter(shape);

export function describe(shape) {
  return `${shape.kind}: area ${area(shape).toFixed(2)}, perimeter ${perimeter(shape).toFixed(2)}`;
}
