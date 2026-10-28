package database;

import model.DistributionRecord;
import model.FoodItem;
import model.InventoryOperations;
import model.PackagedItem;
import model.PerishableItem;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Vector;

/**
 * FoodBankDAO - Data Access Object implementing InventoryOperations
 * 
 * College Syllabus Mapping:
 * - Module 3: Interfaces (Implementing an interface)
 * - Module 4: Developing Database Applications using JDBC
 *   - CRUD Operations (Create, Read, Update, Delete)
 *   - PreparedStatement for parameterized queries
 *   - ResultSet iteration and data extraction
 *   - Safe resource management with try-catch-finally
 * - Module 2: Polymorphism (Returning subclasses PerishableItem and PackagedItem
 *   as superclass FoodItem references)
 */
public class FoodBankDAO implements InventoryOperations {

    // Obtain the single database connection instance via Singleton
    private Connection getConnection() {
        return DatabaseManager.getInstance().getConnection();
    }

    /**
     * Create / Insert new Food Item into the database
     */
    @Override
    public boolean addItem(FoodItem item) throws SQLException {
        String sql = "INSERT INTO food_items (item_id, name, category, item_type, quantity, unit, " +
                     "date_received, expiry_date, base_price, storage_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        PreparedStatement pstmt = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            pstmt.setString(1, item.getItemId());
            pstmt.setString(2, item.getName());
            pstmt.setString(3, item.getCategory());
            pstmt.setString(4, item.getItemType());
            pstmt.setDouble(5, item.getQuantity());
            pstmt.setString(6, item.getUnit());
            pstmt.setString(7, item.getDateReceived());
            pstmt.setString(8, item.getExpiryDate());
            pstmt.setDouble(9, item.getBasePrice());

            // Extract specific storage info based on subtype
            String extraInfo = "";
            if (item instanceof PerishableItem) {
                extraInfo = String.valueOf(((PerishableItem) item).getStorageTemperature());
            } else if (item instanceof PackagedItem) {
                extraInfo = ((PackagedItem) item).getBatchNumber();
            }
            pstmt.setString(10, extraInfo);

            int rows = pstmt.executeUpdate();
            return rows > 0;

        } finally {
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Update existing food item details
     */
    @Override
    public boolean updateItem(FoodItem item) throws SQLException {
        String sql = "UPDATE food_items SET name = ?, category = ?, item_type = ?, quantity = ?, " +
                     "unit = ?, date_received = ?, expiry_date = ?, base_price = ?, storage_info = ? " +
                     "WHERE item_id = ?";

        PreparedStatement pstmt = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            pstmt.setString(1, item.getName());
            pstmt.setString(2, item.getCategory());
            pstmt.setString(3, item.getItemType());
            pstmt.setDouble(4, item.getQuantity());
            pstmt.setString(5, item.getUnit());
            pstmt.setString(6, item.getDateReceived());
            pstmt.setString(7, item.getExpiryDate());
            pstmt.setDouble(8, item.getBasePrice());

            String extraInfo = "";
            if (item instanceof PerishableItem) {
                extraInfo = String.valueOf(((PerishableItem) item).getStorageTemperature());
            } else if (item instanceof PackagedItem) {
                extraInfo = ((PackagedItem) item).getBatchNumber();
            }
            pstmt.setString(9, extraInfo);
            pstmt.setString(10, item.getItemId());

            int rows = pstmt.executeUpdate();
            return rows > 0;

        } finally {
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Restock incoming stock quantity for an item
     */
    @Override
    public boolean restockItem(String itemId, double additionalQuantity) throws SQLException {
        String sql = "UPDATE food_items SET quantity = quantity + ? WHERE item_id = ?";

        PreparedStatement pstmt = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            pstmt.setDouble(1, additionalQuantity);
            pstmt.setString(2, itemId);

            int rows = pstmt.executeUpdate();
            return rows > 0;

        } finally {
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Delete an item (damaged, discarded, or written off)
     */
    @Override
    public boolean deleteItem(String itemId) throws SQLException {
        String sql = "DELETE FROM food_items WHERE item_id = ?";

        PreparedStatement pstmt = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            pstmt.setString(1, itemId);

            int rows = pstmt.executeUpdate();
            return rows > 0;

        } finally {
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Retrieve single food item by ID
     */
    @Override
    public FoodItem getItemById(String itemId) throws SQLException {
        String sql = "SELECT * FROM food_items WHERE item_id = ?";

        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            pstmt.setString(1, itemId);
            rs = pstmt.executeQuery();

            if (rs.next()) {
                return mapResultSetToFoodItem(rs);
            }
            return null;

        } finally {
            if (rs != null) rs.close();
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Retrieve all food items currently in database
     */
    @Override
    public Vector<FoodItem> getAllItems() throws SQLException {
        Vector<FoodItem> list = new Vector<FoodItem>();
        String sql = "SELECT * FROM food_items ORDER BY expiry_date ASC";

        Statement stmt = null;
        ResultSet rs = null;
        try {
            stmt = getConnection().createStatement();
            rs = stmt.executeQuery(sql);

            while (rs.next()) {
                list.add(mapResultSetToFoodItem(rs));
            }
            return list;

        } finally {
            if (rs != null) rs.close();
            if (stmt != null) stmt.close();
        }
    }

    /**
     * Method Overloading 1: Search items by name keyword
     */
    @Override
    public Vector<FoodItem> searchItems(String name) throws SQLException {
        Vector<FoodItem> list = new Vector<FoodItem>();
        String sql = "SELECT * FROM food_items WHERE LOWER(name) LIKE ? ORDER BY expiry_date ASC";

        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            pstmt.setString(1, "%" + name.toLowerCase() + "%");
            rs = pstmt.executeQuery();

            while (rs.next()) {
                list.add(mapResultSetToFoodItem(rs));
            }
            return list;

        } finally {
            if (rs != null) rs.close();
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Method Overloading 2: Search items by category
     */
    @Override
    public Vector<FoodItem> searchItems(String category, int maxDays) throws SQLException {
        Vector<FoodItem> list = new Vector<FoodItem>();
        String sql;
        if (category == null || category.equalsIgnoreCase("All")) {
            sql = "SELECT * FROM food_items ORDER BY expiry_date ASC";
        } else {
            sql = "SELECT * FROM food_items WHERE LOWER(category) = ? ORDER BY expiry_date ASC";
        }

        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            pstmt = getConnection().prepareStatement(sql);
            if (category != null && !category.equalsIgnoreCase("All")) {
                pstmt.setString(1, category.toLowerCase());
            }
            rs = pstmt.executeQuery();

            while (rs.next()) {
                list.add(mapResultSetToFoodItem(rs));
            }
            return list;

        } finally {
            if (rs != null) rs.close();
            if (pstmt != null) pstmt.close();
        }
    }

    /**
     * Record a food distribution transaction and deduct quantity safely
     */
    @Override
    public boolean recordDistribution(DistributionRecord record) throws SQLException {
        Connection conn = getConnection();
        PreparedStatement pstmtRecord = null;
        PreparedStatement pstmtDeduct = null;

        try {
            // Step 1: Insert distribution transaction record
            String sqlRecord = "INSERT INTO distribution_records (trans_id, item_id, item_name, recipient_name, " +
                    "distributed_qty, unit, base_price, discount_percent, effective_price, total_value, trans_date) " +
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

            pstmtRecord = conn.prepareStatement(sqlRecord);
            pstmtRecord.setString(1, record.getTransactionId());
            pstmtRecord.setString(2, record.getItemId());
            pstmtRecord.setString(3, record.getItemName());
            pstmtRecord.setString(4, record.getRecipientName());
            pstmtRecord.setDouble(5, record.getDistributedQuantity());
            pstmtRecord.setString(6, record.getUnit());
            pstmtRecord.setDouble(7, record.getBasePrice());
            pstmtRecord.setDouble(8, record.getDiscountPercent());
            pstmtRecord.setDouble(9, record.getEffectivePrice());
            pstmtRecord.setDouble(10, record.getTotalValue());
            pstmtRecord.setString(11, record.getTransactionDate());

            pstmtRecord.executeUpdate();

            // Step 2: Deduct quantity from inventory
            String sqlDeduct = "UPDATE food_items SET quantity = quantity - ? WHERE item_id = ?";
            pstmtDeduct = conn.prepareStatement(sqlDeduct);
            pstmtDeduct.setDouble(1, record.getDistributedQuantity());
            pstmtDeduct.setString(2, record.getItemId());

            pstmtDeduct.executeUpdate();

            return true;

        } finally {
            if (pstmtRecord != null) pstmtRecord.close();
            if (pstmtDeduct != null) pstmtDeduct.close();
        }
    }

    /**
     * Retrieve all past distribution transactions
     */
    @Override
    public Vector<DistributionRecord> getAllDistributions() throws SQLException {
        Vector<DistributionRecord> list = new Vector<DistributionRecord>();
        String sql = "SELECT * FROM distribution_records ORDER BY trans_date DESC";

        Statement stmt = null;
        ResultSet rs = null;
        try {
            stmt = getConnection().createStatement();
            rs = stmt.executeQuery(sql);

            while (rs.next()) {
                DistributionRecord rec = new DistributionRecord(
                        rs.getString("trans_id"),
                        rs.getString("item_id"),
                        rs.getString("item_name"),
                        rs.getString("recipient_name"),
                        rs.getDouble("distributed_qty"),
                        rs.getString("unit"),
                        rs.getDouble("base_price"),
                        rs.getDouble("discount_percent"),
                        rs.getDouble("effective_price"),
                        rs.getDouble("total_value"),
                        rs.getString("trans_date")
                );
                list.add(rec);
            }
            return list;

        } finally {
            if (rs != null) rs.close();
            if (stmt != null) stmt.close();
        }
    }

    /**
     * Helper method to map SQL ResultSet row to FoodItem (or Subclass)
     * Demonstrates Polymorphism and Dynamic Method Dispatch
     */
    private FoodItem mapResultSetToFoodItem(ResultSet rs) throws SQLException {
        String id = rs.getString("item_id");
        String name = rs.getString("name");
        String category = rs.getString("category");
        String itemType = rs.getString("item_type");
        double qty = rs.getDouble("quantity");
        String unit = rs.getString("unit");
        String recDate = rs.getString("date_received");
        String expDate = rs.getString("expiry_date");
        double price = rs.getDouble("base_price");
        String storageInfo = rs.getString("storage_info");

        if (itemType != null && itemType.equalsIgnoreCase("PERISHABLE")) {
            double temp = 4.0;
            try {
                if (storageInfo != null && !storageInfo.isEmpty()) {
                    temp = Double.parseDouble(storageInfo);
                }
            } catch (NumberFormatException e) {
                temp = 4.0;
            }
            return new PerishableItem(id, name, category, qty, unit, recDate, expDate, price, temp);

        } else if (itemType != null && itemType.equalsIgnoreCase("PACKAGED")) {
            String batch = (storageInfo != null && !storageInfo.isEmpty()) ? storageInfo : "BATCH-GEN";
            return new PackagedItem(id, name, category, qty, unit, recDate, expDate, price, batch);

        } else {
            return new FoodItem(id, name, category, itemType, qty, unit, recDate, expDate, price);
        }
    }
}
