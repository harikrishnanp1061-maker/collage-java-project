package model;

/**
 * DistributionRecord - Represents a completed food distribution transaction
 * 
 * College Syllabus Mapping:
 * - Module 1: Class and Objects, Constructors
 * - Module 1 & 2: Encapsulation (Private fields with public getters/setters)
 * - Module 2: The 'this' keyword
 */
public class DistributionRecord {

    private String transactionId;
    private String itemId;
    private String itemName;
    private String recipientName;
    private double distributedQuantity;
    private String unit;
    private double basePrice;
    private double discountPercent; // e.g. 100.0, 50.0, 0.0
    private double effectivePrice;   // after subsidy
    private double totalValue;      // distributedQuantity * effectivePrice
    private String transactionDate; // "YYYY-MM-DD HH:MM:SS"

    // Default constructor
    public DistributionRecord() {
        this.transactionId = "TXN-000";
        this.itemId = "";
        this.itemName = "";
        this.recipientName = "";
        this.distributedQuantity = 0.0;
        this.unit = "Units";
        this.basePrice = 0.0;
        this.discountPercent = 0.0;
        this.effectivePrice = 0.0;
        this.totalValue = 0.0;
        this.transactionDate = "";
    }

    // Parameterized constructor
    public DistributionRecord(String transactionId, String itemId, String itemName, 
                              String recipientName, double distributedQuantity, String unit, 
                              double basePrice, double discountPercent, double effectivePrice, 
                              double totalValue, String transactionDate) {
        this.transactionId = transactionId;
        this.itemId = itemId;
        this.itemName = itemName;
        this.recipientName = recipientName;
        this.distributedQuantity = distributedQuantity;
        this.unit = unit;
        this.basePrice = basePrice;
        this.discountPercent = discountPercent;
        this.effectivePrice = effectivePrice;
        this.totalValue = totalValue;
        this.transactionDate = transactionDate;
    }

    // --- Getters and Setters ---

    public String getTransactionId() {
        return this.transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }

    public String getItemId() {
        return this.itemId;
    }

    public void setItemId(String itemId) {
        this.itemId = itemId;
    }

    public String getItemName() {
        return this.itemName;
    }

    public void setItemName(String itemName) {
        this.itemName = itemName;
    }

    public String getRecipientName() {
        return this.recipientName;
    }

    public void setRecipientName(String recipientName) {
        this.recipientName = recipientName;
    }

    public double getDistributedQuantity() {
        return this.distributedQuantity;
    }

    public void setDistributedQuantity(double distributedQuantity) {
        this.distributedQuantity = distributedQuantity;
    }

    public String getUnit() {
        return this.unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }

    public double getBasePrice() {
        return this.basePrice;
    }

    public void setBasePrice(double basePrice) {
        this.basePrice = basePrice;
    }

    public double getDiscountPercent() {
        return this.discountPercent;
    }

    public void setDiscountPercent(double discountPercent) {
        this.discountPercent = discountPercent;
    }

    public double getEffectivePrice() {
        return this.effectivePrice;
    }

    public void setEffectivePrice(double effectivePrice) {
        this.effectivePrice = effectivePrice;
    }

    public double getTotalValue() {
        return this.totalValue;
    }

    public void setTotalValue(double totalValue) {
        this.totalValue = totalValue;
    }

    public String getTransactionDate() {
        return this.transactionDate;
    }

    public void setTransactionDate(String transactionDate) {
        this.transactionDate = transactionDate;
    }

    // Summary display
    public void displaySummary() {
        System.out.println("Receipt #" + transactionId + " | " + itemName + " to " + recipientName + 
                           " | Qty: " + distributedQuantity + " " + unit + 
                           " | Subsidy: " + discountPercent + "% | Total: Rs." + totalValue);
    }
}
