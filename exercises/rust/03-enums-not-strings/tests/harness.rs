mod order;
use order::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn happy_path() {
        let mut o = Order::new(7);
        assert_eq!(o.id, 7);
        assert_eq!(o.label(), "Order placed");
        assert!(!o.is_final());
        let labels: Vec<String> = (0..3).map(|_| { assert!(o.advance()); o.label() }).collect();
        assert_eq!(labels, ["Payment received", "On its way", "Delivered"]);
        assert!(o.is_final());
        assert!(!o.advance());
        assert_eq!(o.label(), "Delivered");
    }

    #[test]
    fn cancel_before_shipping() {
        let mut o = Order::new(1);
        assert!(o.cancel());
        assert_eq!(o.label(), "Cancelled");
        assert!(o.is_final());
        assert!(!o.advance());
        assert!(!o.cancel());

        let mut paid = Order::new(2);
        paid.advance();
        assert!(paid.cancel());
    }

    #[test]
    fn cannot_cancel_after_shipping() {
        let mut o = Order::new(3);
        o.advance();
        o.advance();
        assert!(!o.cancel());
        assert_eq!(o.label(), "On its way");
        o.advance();
        assert!(!o.cancel());
        assert_eq!(o.label(), "Delivered");
    }
}
