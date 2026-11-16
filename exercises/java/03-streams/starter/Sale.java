public class Sale {
    private String region;
    private String product;
    private double amount;

    public Sale(String region, String product, double amount) {
        this.region = region;
        this.product = product;
        this.amount = amount;
    }

    public String getRegion() {
        return region;
    }

    public String getProduct() {
        return product;
    }

    public double getAmount() {
        return amount;
    }
}
