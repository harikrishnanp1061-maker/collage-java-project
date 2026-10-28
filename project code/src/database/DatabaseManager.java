package database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * DatabaseManager - Local SQLite Database Connection Provider
 * 
 * College Syllabus Mapping:
 * - Module 3: Singleton Design Pattern (private constructor, static instance, static getInstance())
 * - Module 4: Developing Database Applications using JDBC
 *   - JDBC Steps: Driver Loading, Connection Establishment, Statement Creation, Query Execution
 *   - Error Handling: Checked SQLException handling with try-catch-finally
 */
public class DatabaseManager {

    // 1. Static reference to the single instance of DatabaseManager (Singleton)
    private static DatabaseManager instance = null;

    // JDBC Connection object
    private Connection connection = null;

    // SQLite Database File URL
    private static final String DB_URL = "jdbc:sqlite:chronochef.db";

    // 2. Private Constructor: Prevents instantiation from any other class
    private DatabaseManager() {
        try {
            // Step 1: Load SQLite JDBC Driver
            Class.forName("org.sqlite.JDBC");

            // Step 2: Establish the Connection
            this.connection = DriverManager.getConnection(DB_URL);
            System.out.println("[DatabaseManager] Connected to SQLite database: chronochef.db");

            // Step 3: Initialize Database Tables
            createTables();

        } catch (ClassNotFoundException e) {
            System.out.println("[DatabaseManager] Error: SQLite JDBC Driver not found in classpath.");
            e.printStackTrace();
        } catch (SQLException e) {
            System.out.println("[DatabaseManager] SQL Error during database initialization.");
            e.printStackTrace();
        }
    }

    // 3. Static synchronized method to provide global access point to the Singleton
    public static synchronized DatabaseManager getInstance() {
        if (instance == null) {
            instance = new DatabaseManager();
        }
        return instance;
    }

    // Method to get active JDBC Connection
    public Connection getConnection() {
        try {
            if (this.connection == null || this.connection.isClosed()) {
                this.connection = DriverManager.getConnection(DB_URL);
            }
        } catch (SQLException e) {
            System.out.println("[DatabaseManager] Error reconnecting to database: " + e.getMessage());
        }
        return this.connection;
    }

    /**
     * Create required SQL tables if they do not exist
     * Demonstrates Module 4: Executing basic SQL Queries (DDL)
     */
    private void createTables() {
        Statement stmt = null;
        try {
            stmt = this.connection.createStatement();

            // Table 1: Food Items Inventory
            String sqlFoodItems = "CREATE TABLE IF NOT EXISTS food_items (" +
                    "item_id VARCHAR(20) PRIMARY KEY, " +
                    "name VARCHAR(100) NOT NULL, " +
                    "category VARCHAR(50) NOT NULL, " +
                    "item_type VARCHAR(20) NOT NULL, " +
                    "quantity DOUBLE NOT NULL, " +
                    "unit VARCHAR(20) NOT NULL, " +
                    "date_received VARCHAR(10) NOT NULL, " +
                    "expiry_date VARCHAR(10) NOT NULL, " +
                    "base_price DOUBLE NOT NULL, " +
                    "storage_info VARCHAR(100)" +
                    ");";
            stmt.executeUpdate(sqlFoodItems);

            // Table 2: Distribution Transactions Log
            String sqlDistributions = "CREATE TABLE IF NOT EXISTS distribution_records (" +
                    "trans_id VARCHAR(20) PRIMARY KEY, " +
                    "item_id VARCHAR(20) NOT NULL, " +
                    "item_name VARCHAR(100) NOT NULL, " +
                    "recipient_name VARCHAR(100) NOT NULL, " +
                    "distributed_qty DOUBLE NOT NULL, " +
                    "unit VARCHAR(20) NOT NULL, " +
                    "base_price DOUBLE NOT NULL, " +
                    "discount_percent DOUBLE NOT NULL, " +
                    "effective_price DOUBLE NOT NULL, " +
                    "total_value DOUBLE NOT NULL, " +
                    "trans_date VARCHAR(20) NOT NULL" +
                    ");";
            stmt.executeUpdate(sqlDistributions);

            System.out.println("[DatabaseManager] Database tables verified/created successfully.");

        } catch (SQLException e) {
            System.out.println("[DatabaseManager] Error creating tables: " + e.getMessage());
        } finally {
            // Module 3: finally block used to free database resources safely
            try {
                if (stmt != null) stmt.close();
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
    }
}
