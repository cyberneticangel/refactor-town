export function cartSummary(items) {
  const inStock = items.filter((item) => item.inStock);

  const total = inStock.reduce((sum, item) => sum + item.price * item.qty, 0);
  const count = inStock.reduce((sum, item) => sum + item.qty, 0);
  const names = inStock.map((item) => item.name.toUpperCase());

  return { total, count, names };
}
