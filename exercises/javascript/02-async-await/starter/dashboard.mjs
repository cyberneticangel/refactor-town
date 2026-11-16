import { getUser, getOrders, getProduct } from "./api.mjs";

export function loadDashboard(userId) {
  return new Promise(function (resolve, reject) {
    getUser(userId, function (err, user) {
      if (err) {
        reject(err);
        return;
      }
      getOrders(user.id, function (err, orders) {
        if (err) {
          reject(err);
          return;
        }
        if (orders.length === 0) {
          resolve({ name: user.name, lines: [], total: 0 });
          return;
        }
        var lines = [];
        var pending = orders.length;
        var failed = false;
        orders.forEach(function (order, index) {
          getProduct(order.productId, function (err, product) {
            if (failed) {
              return;
            }
            if (err) {
              failed = true;
              reject(err);
              return;
            }
            lines[index] = {
              title: product.title,
              qty: order.qty,
              cost: product.price * order.qty,
            };
            pending = pending - 1;
            if (pending === 0) {
              var total = 0;
              for (var i = 0; i < lines.length; i++) {
                total = total + lines[i].cost;
              }
              resolve({ name: user.name, lines: lines, total: total });
            }
          });
        });
      });
    });
  });
}
