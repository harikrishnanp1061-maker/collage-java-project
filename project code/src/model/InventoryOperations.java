package model;

import java.util.Vector;

/**
 * InventoryOperations - Interface for core Food Bank Inventory & Distribution
 * 
 * College Syllabus Mapping:
 * - Module 3: Interfaces (Defining an interface, abstract methods, contracts)
 * - Module 3: Accessing implementations through interface references (Polymorphism)
 * - Module 1: Vector class (Standard Java collections permitted by syllabus)
 */
public interface InventoryOperations {

    // Add new food item to inventory
    boolean addItem(FoodItem item) throws Exception;

    // Update existing food item details
    boolean updateItem(FoodItem item) throws Exception;

    // Restock incoming quantity for an existing item
    boolean restockItem(String itemId, double additionalQuantity) throws Exception;

    // Remove an item (damaged/written-off) from inventory
    boolean deleteItem(String itemId) throws Exception;

    // Retrieve a specific item by its unique ID
    FoodItem getItemById(String itemId) throws Exception;

    // Retrieve all active inventory items (using Vector as per Module 1 syllabus)
    Vector<FoodItem> getAllItems() throws Exception;

    // Search items by name (Method Overloading)
    Vector<FoodItem> searchItems(String name) throws Exception;

    // Search items by category and maximum days remaining (Method Overloading)
    Vector<FoodItem> searchItems(String category, int maxDays) throws Exception;

    // Record a completed distribution transaction
    boolean recordDistribution(DistributionRecord record) throws Exception;

    // Retrieve full distribution history
    Vector<DistributionRecord> getAllDistributions() throws Exception;
}
