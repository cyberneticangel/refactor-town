pub struct Order {
    pub id: u32,
    status: String,
}

impl Order {
    pub fn new(id: u32) -> Order {
        Order { id: id, status: String::from("placed") }
    }

    /// Move to the next step: placed -> paid -> shipped -> delivered.
    /// Returns false if the order can't advance.
    pub fn advance(&mut self) -> bool {
        if self.status == "placed" {
            self.status = String::from("paid");
            return true;
        } else if self.status == "paid" {
            self.status = String::from("shipped");
            return true;
        } else if self.status == "shipped" {
            self.status = String::from("delivered");
            return true;
        }
        return false;
    }

    /// Orders can be cancelled until they ship.
    pub fn cancel(&mut self) -> bool {
        if self.status == "placed" || self.status == "paid" {
            self.status = String::from("cancelled");
            return true;
        }
        return false;
    }

    pub fn is_final(&self) -> bool {
        self.status == "delivered" || self.status == "cancelled"
    }

    pub fn label(&self) -> String {
        if self.status == "placed" {
            return String::from("Order placed");
        } else if self.status == "paid" {
            return String::from("Payment received");
        } else if self.status == "shipped" {
            return String::from("On its way");
        } else if self.status == "delivered" {
            return String::from("Delivered");
        } else if self.status == "cancelled" {
            return String::from("Cancelled");
        }
        return String::from("Unknown");
    }
}
