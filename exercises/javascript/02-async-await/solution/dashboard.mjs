import { promisify } from "node:util";
import { getUser, getOrders, getProduct } from "./api.mjs";

const fetchUser = promisify(getUser);
const fetchOrders = promisify(getOrders);
const fetchProduct = promisify(getProduct);

export async function loadDashboard(userId) {
  const user = await fetchUser(userId);
  const orders = await fetchOrders(user.id);
  const products = await Promise.all(orders.map((order) => fetchProduct(order.productId)));

  const lines = orders.map((order, i) => ({
    title: products[i].title,
    qty: order.qty,
    cost: products[i].price * order.qty,
  }));
  const total = lines.reduce((sum, line) => sum + line.cost, 0);

  return { name: user.name, lines, total };
}
