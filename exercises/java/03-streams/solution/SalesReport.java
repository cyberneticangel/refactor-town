import java.util.*;
import java.util.stream.Collectors;

public class SalesReport {
    /** Total amount per region, regions in alphabetical order. */
    public static Map<String, Double> totalByRegion(List<Sale> sales) {
        return sales.stream()
                .collect(Collectors.groupingBy(Sale::region, TreeMap::new, Collectors.summingDouble(Sale::amount)));
    }

    /** The n products with the highest total sales; ties broken alphabetically. */
    public static List<String> topProducts(List<Sale> sales, int n) {
        Map<String, Double> totals = sales.stream()
                .collect(Collectors.groupingBy(Sale::product, Collectors.summingDouble(Sale::amount)));
        return totals.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed()
                        .thenComparing(Map.Entry.comparingByKey()))
                .limit(n)
                .map(Map.Entry::getKey)
                .toList();
    }

    /** Average amount of sales strictly above the threshold, or 0 if there are none. */
    public static double averageAbove(List<Sale> sales, double threshold) {
        return sales.stream()
                .mapToDouble(Sale::amount)
                .filter(amount -> amount > threshold)
                .average()
                .orElse(0);
    }

    /** Regions (alphabetical) where the given product sold at least once. */
    public static List<String> regionsSelling(List<Sale> sales, String product) {
        return sales.stream()
                .filter(sale -> sale.product().equals(product))
                .map(Sale::region)
                .distinct()
                .sorted()
                .toList();
    }
}
