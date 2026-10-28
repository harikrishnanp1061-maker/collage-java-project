package exception;

/**
 * Custom Checked Exception: ExpiredItemDistributionException
 * 
 * College Syllabus Mapping:
 * - Module 3: Exception Handling -> Custom Exceptions (extending java.lang.Exception)
 * - Checked Exception: Ensures critical business and food safety rules cannot be bypassed
 * 
 * Used when attempting to distribute food items that have passed their expiry date.
 * Strictly thrown BEFORE any subsidy, pricing, or stock deduction logic.
 */
public class ExpiredItemDistributionException extends Exception {

    // Default constructor
    public ExpiredItemDistributionException() {
        super("Food Safety Violation: Expired items cannot be distributed.");
    }

    // Parameterized constructor accepting custom error message
    public ExpiredItemDistributionException(String message) {
        super(message);
    }
}
