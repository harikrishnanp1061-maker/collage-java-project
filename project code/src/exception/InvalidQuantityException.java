package exception;

/**
 * Custom Checked Exception: InvalidQuantityException
 * 
 * College Syllabus Mapping:
 * - Module 3: Exception Handling -> Custom Exceptions (extending java.lang.Exception)
 * - Checked Exception: Enforces compile-time checking using try-catch or throws
 * 
 * Used when a user enters non-positive, zero, or excessive distribution quantities.
 */
public class InvalidQuantityException extends Exception {

    // Default constructor
    public InvalidQuantityException() {
        super("Invalid quantity entered. Quantity must be greater than zero.");
    }

    // Parameterized constructor accepting custom error message
    public InvalidQuantityException(String message) {
        super(message);
    }
}
