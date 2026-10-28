package model;

/**
 * PerishableItem - Subclass representing fresh produce, dairy, bakery, etc.
 * 
 * College Syllabus Mapping:
 * - Module 2: Inheritance (Super Class and Sub Class, extends keyword)
 * - Module 2: The 'super' keyword (calling superclass constructor)
 * - Module 2: Method Overriding (@Override) and Dynamic Method Dispatch
 */
public class PerishableItem extends FoodItem {

    // Additional specific member variable
    private double storageTemperature; // in Celsius

    // Default constructor
    public PerishableItem() {
        super();
        this.storageTemperature = 4.0; // Default cold refrigeration
    }

    // Parameterized constructor calling super(...)
    public PerishableItem(String itemId, String name, String category, double quantity, 
                          String unit, String dateReceived, String expiryDate, 
                          double basePrice, double storageTemperature) {
        // Explicitly invokes superclass constructor (Module 2)
        super(itemId, name, category, "PERISHABLE", quantity, unit, dateReceived, expiryDate, basePrice);
        this.storageTemperature = storageTemperature;
    }

    // Getter and Setter for storageTemperature
    public double getStorageTemperature() {
        return this.storageTemperature;
    }

    public void setStorageTemperature(double storageTemperature) {
        this.storageTemperature = storageTemperature;
    }

    /**
     * Method Overriding: Overrides FoodItem.getStorageInstructions()
     * Demonstrates Run-time Polymorphism (Dynamic Method Dispatch)
     */
    @Override
    public String getStorageInstructions() {
        return "Perishable: Store at or below " + storageTemperature + "°C (Cold Chain Required).";
    }

    /**
     * Method Overriding: Overrides FoodItem.getItemClassification()
     */
    @Override
    public String getItemClassification() {
        return "Perishable (Requires Refrigeration/Prompt Distribution)";
    }
}
