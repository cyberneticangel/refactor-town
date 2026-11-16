import java.util.*;

public class SalesReport {
    /** Total amount per region, regions in alphabetical order. */
    public static Map<String, Double> totalByRegion(List<Sale> sales) {
        Map<String, Double> totals = new TreeMap<>();
        for (Sale s : sales) {
            if (totals.containsKey(s.getRegion())) {
                totals.put(s.getRegion(), totals.get(s.getRegion()) + s.getAmount());
            } else {
                totals.put(s.getRegion(), s.getAmount());
            }
        }
        return totals;
    }

    /** The n products with the highest total sales; ties broken alphabetically. */
    public static List<String> topProducts(List<Sale> sales, int n) {
        Map<String, Double> totals = new HashMap<>();
        for (Sale s : sales) {
            Double current = totals.get(s.getProduct());
            if (current == null) {
                current = 0.0;
            }
            totals.put(s.getProduct(), current + s.getAmount());
        }
        List<Map.Entry<String, Double>> entries = new ArrayList<>(totals.entrySet());
        Collections.sort(entries, new Comparator<Map.Entry<String, Double>>() {
            @Override
            public int compare(Map.Entry<String, Double> a, Map.Entry<String, Double> b) {
                int byAmount = Double.compare(b.getValue(), a.getValue());
                if (byAmount != 0) {
                    return byAmount;
                }
                return a.getKey().compareTo(b.getKey());
            }
        });
        List<String> result = new ArrayList<>();
        for (int i = 0; i < entries.size() && i < n; i++) {
            result.add(entries.get(i).getKey());
        }
        return result;
    }

    /** Average amount of sales strictly above the threshold, or 0 if there are none. */
    public static double averageAbove(List<Sale> sales, double threshold) {
        double sum = 0;
        int count = 0;
        for (Sale s : sales) {
            if (s.getAmount() > threshold) {
                sum += s.getAmount();
                count++;
            }
        }
        if (count == 0) {
            return 0;
        }
        return sum / count;
    }

    /** Regions (alphabetical) where the given product sold at least once. */
    public static List<String> regionsSelling(List<Sale> sales, String product) {
        List<String> regions = new ArrayList<>();
        for (Sale s : sales) {
            if (s.getProduct().equals(product) && !regions.contains(s.getRegion())) {
                regions.add(s.getRegion());
            }
        }
        Collections.sort(regions);
        return regions;
    }
}
