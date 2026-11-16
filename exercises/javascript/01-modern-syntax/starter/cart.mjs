export function cartSummary(items) {
  var total = 0;
  var count = 0;
  var names = [];
  for (var i = 0; i < items.length; i++) {
    if (items[i].inStock == true) {
      total = total + items[i].price * items[i].qty;
      count = count + items[i].qty;
      names.push(items[i].name.toUpperCase());
    }
  }
  return { total: total, count: count, names: names };
}
