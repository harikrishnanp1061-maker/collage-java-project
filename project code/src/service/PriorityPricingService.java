package service;

import exception.ExpiredItemDistributionException;
import exception.InvalidQuantityException;
import model.FoodItem;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Vector;

/**
 * PriorityPricingService - Core Business Logic for ChronoChef
 * 
 * Implements:
 * 1. Days Remaining Calculation
 * 2. Deterministic Priority Distribution Index (PDI)
 * 3. Priority Level Classification
 * 4. Rule-Based Dynamic Subsidies (Guarded against expired items)
 * 5. Priority Sorting via Classic Bubble Sort (Module 1 Arrays & Loops)
 */
public class PriorityPricingService {

    private static final SimpleDateFormat DATE_FORMAT = new SimpleDateFormat("yyyy-MM-dd");

    /**
     * Calculate days remaining between current date and target expiry date.
     * Uses Module 3 Exception Handling for ParseException.
     */
    public static int calculateDaysRemaining(String expiryDateStr) {
        try {
            DATE_FORMAT.setLenient(false);
            Date expiryDate = DATE_FORMAT.parse(expiryDateStr.trim());
            
            // Normalize today's date to midnight for clean integer day difference
            Date today = new Date();
            String todayStr = DATE_FORMAT.format(today);
            Date normalizedToday = DATE_FORMAT.parse(todayStr);

            long diffInMillis = expiryDate.getTime() - normalizedToday.getTime();
            return (int) (diffInMillis / (1000 * 60 * 60 * 24));

        } catch (ParseException e) {
            System.out.println("[PriorityPricingService] Date parsing error for: " + expiryDateStr);
            return 0;
        }
    }

    /**
     * Priority Distribution Index (PDI) Calculation
     * 
     * Verified Rules:
     * - If D < 0 (Expired): PDI = 0 (Quarantined)
     * - If D >= 0 (Safe): PDI = Math.max(1, 100 - (D * 2)) [Bounded between 1 and 100]
     */
    public static int calculatePDI(int daysRemaining) {
        if (daysRemaining < 0) {
            return 0; // Expired
        }
        int score = 100 - (daysRemaining * 2);
        return Math.max(1, Math.min(100, score));
    }

    /**
     * Determine Priority Level String from Days Remaining
     */
    public static String getPriorityLevel(int daysRemaining) {
        if (daysRemaining < 0) {
            return "EXPIRED";
        } else if (daysRemaining <= 5) {
            return "URGENT";
        } else if (daysRemaining <= 15) {
            return "HIGH";
        } else if (daysRemaining <= 30) {
            return "MEDIUM";
        } else {
            return "LOW";
        }
    }

    /**
     * Determine Food Safety Status String
     */
    public static String getStatusString(int daysRemaining) {
        if (daysRemaining < 0) {
            return "EXPIRED (Quarantined)";
        } else if (daysRemaining <= 5) {
            return "Critical Shelf Life";
        } else if (daysRemaining <= 15) {
            return "Approaching Expiry";
        } else {
            return "Safe to Distribute";
        }
    }

    /**
     * Calculate Food Bank Dynamic Subsidy Percentage
     * 
     * CRITICAL SAFETY RULE:
     * - Throws ExpiredItemDistributionException if D < 0.
     * - Expired items are strictly blocked BEFORE any subsidy or pricing calculation.
     */
    public static double calculateSubsidyPercentage(int daysRemaining) throws ExpiredItemDistributionException {
        if (daysRemaining < 0) {
            throw new ExpiredItemDistributionException(
                "Food Safety Violation: Item is expired (" + Math.abs(daysRemaining) + 
                " days past expiry). Subsidies and distribution are strictly prohibited."
            );
        }

        if (daysRemaining <= 2) {
            return 100.0; // 100% Subsidy / Completely Free (Clear immediately)
        } else if (daysRemaining <= 7) {
            return 50.0;  // 50% Subsidy (Heavily subsidized for prompt pickup)
        } else {
            return 0.0;   // 0% Subsidy (Standard nominal base price)
        }
    }

    /**
     * Calculate Effective Price after Food Bank Subsidy
     */
    public static double calculateEffectivePrice(double basePrice, int daysRemaining) throws ExpiredItemDistributionException {
        double subsidyPercent = calculateSubsidyPercentage(daysRemaining);
        double discount = (subsidyPercent / 100.0) * basePrice;
        double effective = basePrice - discount;
        return Math.max(0.0, effective);
    }

    /**
     * Sorts inventory items by PDI score in descending order (highest urgency first).
     * 
     * Syllabus Mapping:
     * - Module 1: Control Statements (Iteration: nested for loops, Selection: if)
     * - Implements textbook Bubble Sort algorithm.
     */
    public static void sortByUrgencyDescending(Vector<FoodItem> items) {
        int n = items.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                int daysJ = calculateDaysRemaining(items.get(j).getExpiryDate());
                int pdiJ = calculatePDI(daysJ);

                int daysNext = calculateDaysRemaining(items.get(j + 1).getExpiryDate());
                int pdiNext = calculatePDI(daysNext);

                // For descending order: if previous score is smaller than next score, swap
                if (pdiJ < pdiNext) {
                    FoodItem temp = items.get(j);
                    items.set(j, items.get(j + 1));
                    items.set(j + 1, temp);
                }
            }
        }
    }
}
