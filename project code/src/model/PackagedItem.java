package model;

/**
 * PackagedItem - Subclass representing canned goods, dry grains, sealed boxes, etc.
 * 
 * College Syllabus Mapping:
 * - Module 2: Inheritance (Hierarchical Inheritance, extends keyword)
 * - Module 2: The 'super' keyword (calling superclass constructor)
 * - Module 2: Method Overriding and Dynamic Method Dispatch
 */
public class PackagedItem extends FoodItem {

    // Additional specific member variable
    private String batchNumber;

    // Default constructor
    public PackagedItem() {
        super();
        this.batchNumber = "BATCH-DEFAULT";
    }

    // Parameterized constructor calling super(...)
    public PackagedItem(String itemId, String name, String category, double quantity, 
                        String unit, String dateReceived, String expiryDate, 
                        double basePrice, String batchNumber) {
        // Explicitly invokes superclass constructor
        super(itemId, name, category, "PACKAGED", quantity, unit, dateReceived, expiryDate, basePrice);
        this.batchNumber = batchNumber;
    }

    // Getter and Setter for batchNumber
    public String getBatchNumber() {
        return this.batchNumber;
    }

    public void setBatchNumber(String batchNumber) {
        this.batchNumber = batchNumber;
    }

    /**
     * Method Overriding: Overrides FoodItem.getStorageInstructions()
     */
    @Override
    public String getStorageInstructions() {
        return "Packaged [Batch: " + batchNumber + "]: Store in a cool, dry place away from direct sunlight.";
    }

    /**
     * Method Overriding: Overrides FoodItem.getItemClassification()
     */
    @Override
    public String getItemClassification() {
        return "Packaged (Dry Shelf-Stable Goods)";
    }
}
