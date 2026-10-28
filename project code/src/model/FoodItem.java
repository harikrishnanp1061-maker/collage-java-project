package model;

/**
 * FoodItem - Base Entity Class for ChronoChef Inventory System
 * 
 * College Syllabus Mapping:
 * - Module 1: Classes, Instance Variables, Methods, Primitive & Wrapper types
 * - Module 1 & 2: Encapsulation (Private fields with public getters/setters)
 * - Module 2: Constructors, Constructor Overloading, and 'this' keyword
 * - Module 2: Method Overriding and Dynamic Method Dispatch foundation
 */
public class FoodItem {

    // Private fields enforcing Encapsulation (Data Hiding)
    private String itemId;
    private String name;
    private String category;
    private String itemType;       // "PERISHABLE" or "PACKAGED"
    private double quantity;
    private String unit;           // "kg", "Liters", "Packets", "Cans", "Boxes"
    private String dateReceived;   // "YYYY-MM-DD"
    private String expiryDate;     // "YYYY-MM-DD"
    private double basePrice;      // Nominal standard value per unit

    // Default Constructor (Initializes default safe values)
    public FoodItem() {
        this.itemId = "N/A";
        this.name = "Unnamed Item";
        this.category = "General";
        this.itemType = "PERISHABLE";
        this.quantity = 0.0;
        this.unit = "Units";
        this.dateReceived = "2026-01-01";
        this.expiryDate = "2026-01-01";
        this.basePrice = 0.0;
    }

    // Parameterized Constructor 1 (Core attributes without price)
    public FoodItem(String itemId, String name, String category, String itemType, 
                    double quantity, String unit, String dateReceived, String expiryDate) {
        this.itemId = itemId;
        this.name = name;
        this.category = category;
        this.itemType = itemType;
        this.quantity = quantity;
        this.unit = unit;
        this.dateReceived = dateReceived;
        this.expiryDate = expiryDate;
        this.basePrice = 0.0;
    }

    // Overloaded Parameterized Constructor 2 (Full attributes including basePrice)
    public FoodItem(String itemId, String name, String category, String itemType, 
                    double quantity, String unit, String dateReceived, String expiryDate, double basePrice) {
        // Constructor chaining or direct initialization using 'this' keyword
        this.itemId = itemId;
        this.name = name;
        this.category = category;
        this.itemType = itemType;
        this.quantity = quantity;
        this.unit = unit;
        this.dateReceived = dateReceived;
        this.expiryDate = expiryDate;
        this.basePrice = basePrice;
    }

    // --- Getters and Setters (Encapsulation) ---

    public String getItemId() {
        return this.itemId;
    }

    public void setItemId(String itemId) {
        this.itemId = itemId;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getCategory() {
        return this.category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getItemType() {
        return this.itemType;
    }

    public void setItemType(String itemType) {
        this.itemType = itemType;
    }

    public double getQuantity() {
        return this.quantity;
    }

    public void setQuantity(double quantity) {
        if (quantity >= 0.0) {
            this.quantity = quantity;
        } else {
            this.quantity = 0.0;
        }
    }

    public String getUnit() {
        return this.unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }

    public String getDateReceived() {
        return this.dateReceived;
    }

    public void setDateReceived(String dateReceived) {
        this.dateReceived = dateReceived;
    }

    public String getExpiryDate() {
        return this.expiryDate;
    }

    public void setExpiryDate(String expiryDate) {
        this.expiryDate = expiryDate;
    }

    public double getBasePrice() {
        return this.basePrice;
    }

    public void setBasePrice(double basePrice) {
        if (basePrice >= 0.0) {
            this.basePrice = basePrice;
        } else {
            this.basePrice = 0.0;
        }
    }

    /**
     * Polymorphic method to be overridden in subclasses
     * (Demonstrates Dynamic Method Dispatch)
     */
    public String getStorageInstructions() {
        return "Standard food storage guidelines apply.";
    }

    /**
     * Polymorphic method to classify item
     */
    public String getItemClassification() {
        return "General Food Inventory";
    }

    // Method to display item details to console/log
    public void displayDetails() {
        System.out.println("Item ID: " + itemId + " | Name: " + name + " | Category: " + category +
                           " | Qty: " + quantity + " " + unit + " | Expiry: " + expiryDate +
                           " | Base Price: " + basePrice);
    }
}
