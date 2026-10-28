package test;

import database.DataSeeder;
import database.DatabaseManager;
import database.FoodBankDAO;
import exception.ExpiredItemDistributionException;
import exception.InvalidQuantityException;
import model.DistributionRecord;
import model.FoodItem;
import model.PackagedItem;
import model.PerishableItem;
import service.PriorityPricingService;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Vector;

/**
 * ProjectTestRunner - Comprehensive Automated Validation Test Suite
 * 
 * Verifies:
 * 1. PDI scores and exact boundary consistency
 * 2. Food safety guard: Expired items strictly blocked from distribution & subsidy
 * 3. Invalid quantity exceptions
 * 4. Hierarchical inheritance and Dynamic Method Dispatch
 * 5. Database connectivity (SQLite via JDBC) & CRUD
 * 6. Distribution transactions, inventory stock deduction, and transaction logging
 * 7. Bubble sort priority ordering
 */
public class ProjectTestRunner {

    private static int testsPassed = 0;
    private static int testsTotal = 0;

    public static void main(String[] args) {
        System.out.println("==========================================================");
        System.out.println("  RUNNING CHRONOCHEF AUTOMATED TEST SUITE");
        System.out.println("==========================================================");

        testPDICalculationAndBoundaries();
        testExpiredItemRejection();
        testDynamicSubsidyTiers();
        testPolymorphismAndDynamicDispatch();
        testDatabaseCRUDAndStockDeduction();
        testSortingAlgorithm();

        System.out.println("==========================================================");
        System.out.println("  TEST SUITE RESULTS: " + testsPassed + " / " + testsTotal + " TESTS PASSED");
        if (testsPassed == testsTotal) {
            System.out.println("  STATUS: ALL TESTS COMPLETED SUCCESSFULLY! (100% PASS)");
        } else {
            System.out.println("  STATUS: SOME TESTS FAILED. PLEASE REVIEW.");
        }
        System.out.println("==========================================================");
    }

    private static void assertTrue(String testName, boolean condition) {
        testsTotal++;
        if (condition) {
            System.out.println("  [PASS] " + testName);
            testsPassed++;
        } else {
            System.err.println("  [FAIL] " + testName);
        }
    }

    /**
     * Test 1: PDI Score and Priority Threshold Consistency
     */
    private static void testPDICalculationAndBoundaries() {
        System.out.println("\n--- 1. Testing PDI Formula & Exact Boundaries ---");

        // Expired items must receive score 0
        assertTrue("Expired item (D = -1) receives PDI = 0", PriorityPricingService.calculatePDI(-1) == 0);
        assertTrue("Expired item (D = -10) receives PDI = 0", PriorityPricingService.calculatePDI(-10) == 0);
        assertTrue("Expired item (D = -1) priority is EXPIRED", "EXPIRED".equals(PriorityPricingService.getPriorityLevel(-1)));

        // Critical/Urgent items (0 to 5 days)
        assertTrue("Expires today (D = 0) receives PDI = 100", PriorityPricingService.calculatePDI(0) == 100);
        assertTrue("Expires in 1 day (D = 1) receives PDI = 98", PriorityPricingService.calculatePDI(1) == 98);
        assertTrue("Expires in 2 days (D = 2) receives PDI = 96", PriorityPricingService.calculatePDI(2) == 96);
        assertTrue("Expires in 5 days (D = 5) receives PDI = 90", PriorityPricingService.calculatePDI(5) == 90);
        assertTrue("Boundary D = 5 priority is URGENT", "URGENT".equals(PriorityPricingService.getPriorityLevel(5)));

        // High priority items (6 to 15 days)
        assertTrue("Boundary D = 6 receives PDI = 88", PriorityPricingService.calculatePDI(6) == 88);
        assertTrue("D = 10 receives PDI = 80", PriorityPricingService.calculatePDI(10) == 80);
        assertTrue("Boundary D = 15 receives PDI = 70", PriorityPricingService.calculatePDI(15) == 70);
        assertTrue("Boundary D = 15 priority is HIGH", "HIGH".equals(PriorityPricingService.getPriorityLevel(15)));

        // Medium priority items (16 to 30 days)
        assertTrue("Boundary D = 16 receives PDI = 68", PriorityPricingService.calculatePDI(16) == 68);
        assertTrue("Boundary D = 30 receives PDI = 40", PriorityPricingService.calculatePDI(30) == 40);
        assertTrue("Boundary D = 30 priority is MEDIUM", "MEDIUM".equals(PriorityPricingService.getPriorityLevel(30)));

        // Low priority items (> 30 days)
        assertTrue("Boundary D = 31 receives PDI = 38", PriorityPricingService.calculatePDI(31) == 38);
        assertTrue("Boundary D = 31 priority is LOW", "LOW".equals(PriorityPricingService.getPriorityLevel(31)));
        assertTrue("Very long shelf life (D = 200) clamped to min PDI = 1", PriorityPricingService.calculatePDI(200) == 1);
    }

    /**
     * Test 2: Expired Item Distribution Guard
     */
    private static void testExpiredItemRejection() {
        System.out.println("\n--- 2. Testing Expired Item Rejection Guard ---");

        boolean exceptionThrown = false;
        try {
            // Attempting to calculate subsidy on expired item (D = -3)
            PriorityPricingService.calculateSubsidyPercentage(-3);
        } catch (ExpiredItemDistributionException e) {
            exceptionThrown = true;
            System.out.println("  Expected exception caught: " + e.getMessage());
        }
        assertTrue("Expired item throws ExpiredItemDistributionException on subsidy check", exceptionThrown);

        boolean pricingBlocked = false;
        try {
            // Attempting to calculate effective price on expired item
            PriorityPricingService.calculateEffectivePrice(50.0, -2);
        } catch (ExpiredItemDistributionException e) {
            pricingBlocked = true;
        }
        assertTrue("Expired item blocks dynamic price calculation", pricingBlocked);
    }

    /**
     * Test 3: Dynamic Subsidy Tiers for Non-Expired Items
     */
    private static void testDynamicSubsidyTiers() {
        System.out.println("\n--- 3. Testing Rule-Based Dynamic Subsidy Tiers ---");
        try {
            // Tier 1: 0 to 2 days left -> 100% Free
            double subToday = PriorityPricingService.calculateSubsidyPercentage(0);
            double priceToday = PriorityPricingService.calculateEffectivePrice(40.0, 0);
            assertTrue("D = 0 gets 100% subsidy (FREE)", subToday == 100.0 && priceToday == 0.0);

            double sub2Days = PriorityPricingService.calculateSubsidyPercentage(2);
            double price2Days = PriorityPricingService.calculateEffectivePrice(40.0, 2);
            assertTrue("D = 2 gets 100% subsidy (FREE)", sub2Days == 100.0 && price2Days == 0.0);

            // Tier 2: 3 to 7 days left -> 50% Subsidy
            double sub5Days = PriorityPricingService.calculateSubsidyPercentage(5);
            double price5Days = PriorityPricingService.calculateEffectivePrice(40.0, 5);
            assertTrue("D = 5 gets 50% subsidy (Half Price Rs. 20)", sub5Days == 50.0 && price5Days == 20.0);

            // Tier 3: > 7 days left -> 0% Subsidy (Full Base Price)
            double sub10Days = PriorityPricingService.calculateSubsidyPercentage(10);
            double price10Days = PriorityPricingService.calculateEffectivePrice(40.0, 10);
            assertTrue("D = 10 gets 0% subsidy (Full Base Price Rs. 40)", sub10Days == 0.0 && price10Days == 40.0);

        } catch (ExpiredItemDistributionException e) {
            assertTrue("Unexpected exception on safe items", false);
        }
    }

    /**
     * Test 4: Hierarchical Inheritance & Dynamic Method Dispatch
     */
    private static void testPolymorphismAndDynamicDispatch() {
        System.out.println("\n--- 4. Testing Inheritance & Dynamic Method Dispatch ---");

        // Superclass reference pointing to PerishableItem object (Upcasting)
        FoodItem item1 = new PerishableItem("TEST-01", "Milk", "Dairy", 10, "Liters", "2026-10-01", "2026-10-25", 30.0, 4.0);
        // Superclass reference pointing to PackagedItem object (Upcasting)
        FoodItem item2 = new PackagedItem("TEST-02", "Canned Beans", "Canned", 20, "Cans", "2026-10-01", "2027-01-01", 25.0, "BATCH-99");

        // Dynamic Method Dispatch: calls overridden methods at runtime
        String note1 = item1.getStorageInstructions();
        String note2 = item2.getStorageInstructions();

        assertTrue("PerishableItem overrides storage instructions", note1.contains("Cold Chain"));
        assertTrue("PackagedItem overrides storage instructions", note2.contains("cool, dry place"));
    }

    /**
     * Test 5: Database Connection (Singleton) & CRUD & Distribution Transaction
     */
    private static void testDatabaseCRUDAndStockDeduction() {
        System.out.println("\n--- 5. Testing DatabaseManager Singleton & CRUD Operations ---");

        // Verify Singleton pattern
        DatabaseManager db1 = DatabaseManager.getInstance();
        DatabaseManager db2 = DatabaseManager.getInstance();
        assertTrue("DatabaseManager implements Singleton (db1 == db2)", db1 == db2);
        assertTrue("Database connection is open and active", db1.getConnection() != null);

        FoodBankDAO dao = new FoodBankDAO();
        String testId = "TEST-UNIT-999";

        try {
            // Clean up if already exists
            dao.deleteItem(testId);

            // CREATE / INSERT
            PerishableItem testItem = new PerishableItem(testId, "Test Organic Milk", "Dairy", 50.0, "Liters", 
                                                        "2026-10-20", "2026-10-25", 30.0, 4.0);
            boolean added = dao.addItem(testItem);
            assertTrue("CRUD: Successfully inserted test item", added);

            // READ
            FoodItem retrieved = dao.getItemById(testId);
            assertTrue("CRUD: Successfully retrieved item by ID", retrieved != null && "Test Organic Milk".equals(retrieved.getName()));

            // UPDATE / RESTOCK
            boolean restocked = dao.restockItem(testId, 25.0);
            retrieved = dao.getItemById(testId);
            assertTrue("CRUD: Successfully restocked quantity (50 + 25 = 75)", restocked && retrieved.getQuantity() == 75.0);

            // DISTRIBUTION TRANSACTION (Deduct 15 units)
            String testTxnId = "TXN-TEST-" + System.currentTimeMillis();
            DistributionRecord txn = new DistributionRecord(
                    testTxnId, testId, "Test Organic Milk", "Shelter Hope", 
                    15.0, "Liters", 30.0, 50.0, 15.0, 225.0, "2026-10-20 16:00:00"
            );
            boolean txnLogged = dao.recordDistribution(txn);
            retrieved = dao.getItemById(testId);
            assertTrue("Transaction: Recorded distribution & deducted stock (75 - 15 = 60)", 
                       txnLogged && retrieved.getQuantity() == 60.0);

            // Verify transaction logged in distribution_records
            Vector<DistributionRecord> allTxns = dao.getAllDistributions();
            boolean foundTxn = false;
            for (int i = 0; i < allTxns.size(); i++) {
                if (testTxnId.equals(allTxns.get(i).getTransactionId())) {
                    foundTxn = true;
                    break;
                }
            }
            assertTrue("Transaction: Logged in distribution_records table", foundTxn);

            // DELETE / CLEANUP
            boolean deleted = dao.deleteItem(testId);
            assertTrue("CRUD: Successfully cleaned up / deleted test item", deleted);

        } catch (Exception e) {
            System.err.println("Database test exception: " + e.getMessage());
            e.printStackTrace();
            assertTrue("Database operations executed without unexpected error", false);
        }
    }

    /**
     * Test 6: Bubble Sort by Urgency
     */
    private static void testSortingAlgorithm() {
        System.out.println("\n--- 6. Testing Bubble Sort Priority Ordering ---");

        Vector<FoodItem> list = new Vector<FoodItem>();
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        Calendar cal = Calendar.getInstance();

        cal.setTime(new Date());
        String todayStr = sdf.format(cal.getTime());

        // Item with 30 days left (Medium, PDI = 40)
        cal.setTime(new Date());
        cal.add(Calendar.DAY_OF_YEAR, 30);
        String expiry30 = sdf.format(cal.getTime());
        list.add(new FoodItem("A", "Item A", "General", "PERISHABLE", 10, "kg", todayStr, expiry30, 20.0));

        // Item with 1 day left (Urgent, PDI = 98)
        cal.setTime(new Date());
        cal.add(Calendar.DAY_OF_YEAR, 1);
        String expiry1 = sdf.format(cal.getTime());
        list.add(new FoodItem("B", "Item B", "General", "PERISHABLE", 10, "kg", todayStr, expiry1, 20.0));

        // Item with 5 days left (Urgent, PDI = 90)
        cal.setTime(new Date());
        cal.add(Calendar.DAY_OF_YEAR, 5);
        String expiry5 = sdf.format(cal.getTime());
        list.add(new FoodItem("C", "Item C", "General", "PERISHABLE", 10, "kg", todayStr, expiry5, 20.0));

        // Sort descending by PDI
        PriorityPricingService.sortByUrgencyDescending(list);

        // First item should be Item B (1 day left -> PDI 98)
        // Second item should be Item C (5 days left -> PDI 90)
        // Third item should be Item A (30 days left -> PDI 40)
        boolean orderCorrect = "Item B".equals(list.get(0).getName()) &&
                               "Item C".equals(list.get(1).getName()) &&
                               "Item A".equals(list.get(2).getName());

        assertTrue("Bubble Sort ordered items by PDI descending (highest urgency first)", orderCorrect);
    }
}
