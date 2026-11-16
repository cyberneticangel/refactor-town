#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Status {
    Placed,
    Paid,
    Shipped,
    Delivered,
    Cancelled,
}

impl Status {
    fn next(self) -> Option<Status> {
        match self {
            Status::Placed => Some(Status::Paid),
            Status::Paid => Some(Status::Shipped),
            Status::Shipped => Some(Status::Delivered),
            Status::Delivered | Status::Cancelled => None,
        }
    }

    fn label(self) -> &'static str {
        match self {
            Status::Placed => "Order placed",
            Status::Paid => "Payment received",
            Status::Shipped => "On its way",
            Status::Delivered => "Delivered",
            Status::Cancelled => "Cancelled",
        }
    }
}

pub struct Order {
    pub id: u32,
    status: Status,
}

impl Order {
    pub fn new(id: u32) -> Order {
        Order { id, status: Status::Placed }
    }

    /// Move to the next step: placed -> paid -> shipped -> delivered.
    /// Returns false if the order can't advance.
    pub fn advance(&mut self) -> bool {
        match self.status.next() {
            Some(next) => {
                self.status = next;
                true
            }
            None => false,
        }
    }

    /// Orders can be cancelled until they ship.
    pub fn cancel(&mut self) -> bool {
        let cancellable = matches!(self.status, Status::Placed | Status::Paid);
        if cancellable {
            self.status = Status::Cancelled;
        }
        cancellable
    }

    pub fn is_final(&self) -> bool {
        self.status.next().is_none()
    }

    pub fn label(&self) -> String {
        self.status.label().to_string()
    }
}
