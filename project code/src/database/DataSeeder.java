package database;

import model.FoodItem;
import model.PackagedItem;
import model.PerishableItem;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Vector;

/**
 * DataSeeder - Populates realistic Food Bank dummy data
 * 
 * Generates items across all priority brackets:
 * - Expired items (quarantined)
 * - Critical / Urgent items (0-2 days left, 100% subsidy)
 * - High priority items (3-7 days left, 50% subsidy)
 * - Medium priority items (8-25 days left)
 * - Low priority packaged goods (>30 days left)
 */
public class DataSeeder {

    private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd");

    public static void seedIfEmpty() {
        FoodBankDAO dao = new FoodBankDAO();
        try {
            Vector<FoodItem> existing = dao.getAllItems();
            if (existing != null && existing.size() > 0) {
                System.out.println("[DataSeeder] Database already contains " + existing.size() + " items. Skipping seeding.");
                return;
            }

            System.out.println("[DataSeeder] Seeding realistic sample food bank items...");
            Calendar cal = Calendar.getInstance();

            // 1. Expired Item (Received 10 days ago, Expired 2 days ago)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, -10);
            String received10DaysAgo = SDF.format(cal.getTime());

            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, -2);
            String expiredDate = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1001", "Greek Yogurt (Pack of 4)", "Dairy", 15, "Packs", 
                                          received10DaysAgo, expiredDate, 40.0, 4.0));

            // 2. Urgent Item (Expires today: D = 0)
            cal.setTime(new Date());
            String expiresToday = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1002", "Artisan Sandwich Bread", "Bakery", 25, "Loaves", 
                                          SDF.format(new Date()), expiresToday, 25.0, 20.0));

            // 3. Urgent Item (Expires tomorrow: D = 1)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 1);
            String expiresTomorrow = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1003", "Fresh Whole Milk 1L", "Dairy", 30, "Liters", 
                                          SDF.format(new Date()), expiresTomorrow, 35.0, 4.0));

            // 4. Urgent Item (Expires in 2 days: D = 2)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 2);
            String expires2Days = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1004", "Organic Ripe Strawberries", "Produce", 18, "kg", 
                                          SDF.format(new Date()), expires2Days, 50.0, 3.0));

            // 5. High Priority Item (Expires in 4 days: D = 4)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 4);
            String expires4Days = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1005", "Baby Spinach & Mixed Greens", "Produce", 20, "Bags", 
                                          SDF.format(new Date()), expires4Days, 20.0, 5.0));

            // 6. High Priority Item (Expires in 6 days: D = 6)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 6);
            String expires6Days = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1006", "Cottage Cheese 500g", "Dairy", 22, "Tubs", 
                                          SDF.format(new Date()), expires6Days, 45.0, 4.0));

            // 7. Medium Priority Item (Expires in 12 days: D = 12)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 12);
            String expires12Days = SDF.format(cal.getTime());
            dao.addItem(new PerishableItem("FD-1007", "Farm Fresh Crisp Apples", "Produce", 60, "kg", 
                                          SDF.format(new Date()), expires12Days, 30.0, 10.0));

            // 8. Medium Priority Item (Expires in 20 days: D = 20)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 20);
            String expires20Days = SDF.format(cal.getTime());
            dao.addItem(new PackagedItem("FD-1008", "Whole Wheat Pasta 500g", "Grains", 45, "Packets", 
                                        SDF.format(new Date()), expires20Days, 25.0, "BATCH-PASTA-902"));

            // 9. Low Priority Item (Expires in 60 days)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 60);
            String expires60Days = SDF.format(cal.getTime());
            dao.addItem(new PackagedItem("FD-1009", "Canned Red Kidney Beans", "Canned Goods", 80, "Cans", 
                                        SDF.format(new Date()), expires60Days, 28.0, "BATCH-BEAN-110"));

            // 10. Low Priority Item (Expires in 180 days)
            cal.setTime(new Date());
            cal.add(Calendar.DAY_OF_YEAR, 180);
            String expires180Days = SDF.format(cal.getTime());
            dao.addItem(new PackagedItem("FD-1010", "Long Grain White Basmati Rice", "Grains", 100, "kg", 
                                        SDF.format(new Date()), expires180Days, 45.0, "BATCH-RICE-2024"));

            System.out.println("[DataSeeder] Successfully seeded 10 diverse sample food bank items.");

            // Seed initial distribution transactions
            dao.recordDistribution(new model.DistributionRecord(
                "TXN-SEED-01", "FD-1002", "Artisan Sandwich Bread", "St. Jude Community Shelter",
                5.0, "Loaves", 25.0, 100.0, 0.0, 0.0, SDF.format(new Date()) + " 10:15:00"
            ));
            dao.recordDistribution(new model.DistributionRecord(
                "TXN-SEED-02", "FD-1006", "Cottage Cheese 500g", "City Harvest Kitchen",
                4.0, "Tubs", 45.0, 50.0, 22.5, 90.0, SDF.format(new Date()) + " 11:30:00"
            ));
            System.out.println("[DataSeeder] Seeded sample distribution transactions.");

        } catch (Exception e) {
            System.out.println("[DataSeeder] Error during data seeding: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        DatabaseManager.getInstance();
        seedIfEmpty();
    }
}
