# ChronoChef: Project Development Session Summary
**Project Title**: ChronoChef — Smart Dynamic Pricing & Expiry Tracker for Food Banks  
**Course**: PBCST304 — Object-Oriented Programming (Semester S3)  
**Technology Stack**: Java Swing, JDBC, SQLite, Event Delegation Model  
**Date**: October 20, 2026  

---

## 1. Project Background & Abstract

ChronoChef is a Java-based desktop food inventory management and distribution application tailored specifically for food banks and community shelters.

### Core Objectives:
1. **Inventory & Shelf-Life Tracking**: Record food donations with item category, type (perishable vs packaged), quantity, received date, expiry date, and storage requirements.
2. **Priority Distribution Index (PDI)**: Automatically evaluate items based on time remaining before expiration, assigning deterministic priority levels (URGENT, HIGH, MEDIUM, LOW, EXPIRED).
3. **Food Safety Enforcement**: Block expired items from distribution and subsidy calculation.
4. **Dynamic Food-Bank Pricing / Subsidies**: Apply transparent, rule-based subsidies (up to 100% free distribution) for near-expiry stock to clear inventory before spoilage.
5. **Distribution Transactions & Receipts**: Deduct stock safely, prevent negative inventory, and generate itemized distribution receipts.
6. **Analytics & Impact Reporting**: Aggregate stock statistics, urgent item alerts, total food waste prevented, and community subsidies granted.

---

## 2. College Syllabus & Notes Mapping (PBCST304)

The entire codebase strictly follows the concepts, coding styles, and techniques covered in the college notes (`notes/` directory):

| Syllabus Module | Concepts Taught in Notes | Implementation in ChronoChef |
| :--- | :--- | :--- |
| **Module 1** | Primitive types, Wrapper classes, Arrays, `Vector` class, control statements (`if`, `for`, `while`), simple class structure, `main()` method. | • `FoodItem` entity with primitive types & wrappers.<br>• `Vector<FoodItem>` used as backing store for `DefaultTableModel`.<br>• Classic Bubble Sort algorithm for priority sorting. |
| **Module 2** | Encapsulation, constructors, constructor overloading, `this` keyword, Hierarchical Inheritance (`extends`), `super` keyword, method overloading, method overriding, Dynamic Method Dispatch. | • `FoodItem` private fields with getters/setters.<br>• Overloaded constructors using `this.` to resolve variable hiding.<br>• `FoodItem` superclass extended by `PerishableItem` and `PackagedItem`.<br>• Overloaded search methods in `FoodBankDAO`.<br>• Overridden `getStorageInstructions()` dispatched at runtime. |
| **Module 3** | Packages, CLASSPATH, Interfaces, Exception Handling (`try`, `catch`, `finally`, `throw`, `throws`), built-in exceptions, custom exceptions, Singleton design pattern. | • Package organization (`model`, `database`, `service`, `ui`, `exception`).<br>• `InventoryOperations` interface.<br>• Custom checked exceptions: `InvalidQuantityException`, `ExpiredItemDistributionException`.<br>• `DatabaseManager` implemented as thread-safe Singleton. |
| **Module 4** | Swing fundamentals, MVC architecture, components (`JFrame`, `JPanel`, `JLabel`, `JTextField`, `JButton`, `JTable`, `JComboBox`, `JTextArea`), layout managers (`CardLayout`, `BorderLayout`, `GridLayout`, `FlowLayout`), Delegation Event Model (`ActionListener`, `ActionEvent`), JDBC database operations. | • Complete MVC design.<br>• 5 views hosted in a single `JFrame` switched via `CardLayout`.<br>• Event handling with `ActionListener` and `actionPerformed()`.<br>• Standard JDBC SQLite database queries (`PreparedStatement`, `ResultSet`, CRUD). |

---

## 3. Core Algorithms & Mathematical Formulas

### A. Days Remaining Calculation ($D$)
$$\text{Days Remaining } (D) = \frac{\text{Expiry Date (in ms)} - \text{Current Date (in ms)}}{1000 \times 60 \times 60 \times 24}$$
*(Computed using standard `java.util.Date` and `java.text.SimpleDateFormat`).*

### B. Priority Distribution Index (PDI)
$$\text{PDI Score} = 
\begin{cases} 
0 & \text{if } D < 0 \quad (\textbf{EXPIRED - QUARANTINED}) \\
\max\big(1, \; 100 - (D \times 2)\big) & \text{if } D \ge 0 \quad (\textbf{SAFE TO DISTRIBUTE})
\end{cases}$$

#### Exact Thresholds & Brackets:
* **Expired** ($D < 0$): $\text{PDI} = 0 \rightarrow$ **EXPIRED** (Distribution Strictly Blocked).
* **Critical** ($0 \le D \le 5$ days): $\text{PDI} \in [90, 100] \rightarrow$ **URGENT** (100% Free / Immediate clearance).
* **High** ($6 \le D \le 15$ days): $\text{PDI} \in [70, 88] \rightarrow$ **HIGH** (50% Subsidy).
* **Medium** ($16 \le D \le 30$ days): $\text{PDI} \in [40, 68] \rightarrow$ **MEDIUM** (Normal stock rotation).
* **Low** ($D > 30$ days): $\text{PDI} \in [1, 38] \rightarrow$ **LOW** (Long shelf-life dry goods).

### C. Rule-Based Dynamic Subsidy
* $D \le 2$ days: **100% Subsidy (FREE - ₹0.00)** $\rightarrow$ Zero Waste incentive.
* $3 \le D \le 7$ days: **50% Subsidy (Half Price)** $\rightarrow$ Accelerated pickup.
* $D > 7$ days: **0% Subsidy (Full Base Price)** $\rightarrow$ Standard nominal price.

### D. Priority Sorting (Textbook College DSA)
* Implemented using a classic **Bubble Sort** algorithm directly on `Vector<FoodItem>` in descending order of `pdiScore`.

---

## 4. Software Architecture & The 5 Interfaces

All interfaces are hosted in [`MainFrame.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/MainFrame.java) using `CardLayout`:

1. **Module A — Data Input Interface ([`InputPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/InputPanel.java))**:
   - Register items with validation (empty fields check, positive numbers, `YYYY-MM-DD` date pattern).
2. **Module B — Inventory Reading & Expiry Tracker ([`InventoryPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/InventoryPanel.java))**:
   - Live table with search, priority filters, urgency color badges, and PDI sorting.
3. **Module C — Inventory Management ([`ManagementPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/ManagementPanel.java))**:
   - Select item to edit details, restock incoming donations, or write off damaged stock.
4. **Module D — Distribution & Dynamic Subsidy Billing ([`DistributionPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/DistributionPanel.java))**:
   - Issue food to shelters, block expired goods, calculate dynamic subsidy, update stock, and generate itemized distribution receipts.
5. **Module E — Analysis & Reporting ([`AnalyticsPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/AnalyticsPanel.java))**:
   - 6 aggregated metric cards and recent transaction history table.

---

## 5. Complete Source Code Files

1. [`src/Main.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/Main.java) — Program entry point, database initialization, and GUI launch.
2. [`src/model/FoodItem.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/model/FoodItem.java) — Base entity class with private fields and getters/setters.
3. [`src/model/PerishableItem.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/model/PerishableItem.java) — Subclass for cold chain goods.
4. [`src/model/PackagedItem.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/model/PackagedItem.java) — Subclass for dry/canned goods.
5. [`src/model/DistributionRecord.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/model/DistributionRecord.java) — Entity for transactions.
6. [`src/model/InventoryOperations.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/model/InventoryOperations.java) — Interface defining inventory contracts.
7. [`src/exception/InvalidQuantityException.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/exception/InvalidQuantityException.java) — Custom exception for quantity errors.
8. [`src/exception/ExpiredItemDistributionException.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/exception/ExpiredItemDistributionException.java) — Custom exception for expired item food safety violation.
9. [`src/database/DatabaseManager.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/database/DatabaseManager.java) — Thread-safe Singleton connection manager.
10. [`src/database/FoodBankDAO.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/database/FoodBankDAO.java) — JDBC DAO implementing `InventoryOperations`.
11. [`src/database/DataSeeder.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/database/DataSeeder.java) — Pre-populates 10 realistic dummy items and sample transactions.
12. [`src/service/PriorityPricingService.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/service/PriorityPricingService.java) — Core business logic, PDI formula, subsidy rules, and Bubble Sort.
13. [`src/ui/MainFrame.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/MainFrame.java) — Top JFrame window with navigation and `CardLayout`.
14. [`src/ui/InputPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/InputPanel.java) — Data input interface panel.
15. [`src/ui/InventoryPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/InventoryPanel.java) — Inventory reading and expiry tracker panel.
16. [`src/ui/ManagementPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/ManagementPanel.java) — Inventory management & restocking panel.
17. [`src/ui/DistributionPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/DistributionPanel.java) — Distribution & dynamic subsidy billing panel.
18. [`src/ui/AnalyticsPanel.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/ui/AnalyticsPanel.java) — Analytics & overview report panel.
19. [`src/test/ProjectTestRunner.java`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/src/test/ProjectTestRunner.java) — 35-point automated verification test suite.

---

## 6. Pre-Populated Realistic Sample Data

The database [`chronochef.db`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/chronochef.db) is initialized with 10 diverse records:

1. `FD-1001`: **Greek Yogurt** — *Expired 2 days ago* $\rightarrow$ **EXPIRED / Quarantined** (Distribution Blocked).
2. `FD-1002`: **Artisan Sandwich Bread** — *Expires Today ($D=0$)* $\rightarrow$ **URGENT** (PDI: 100, 100% Free).
3. `FD-1003`: **Fresh Whole Milk 1L** — *Expires Tomorrow ($D=1$)* $\rightarrow$ **URGENT** (PDI: 98, 100% Free).
4. `FD-1004`: **Organic Ripe Strawberries** — *Expires in 2 days ($D=2$)* $\rightarrow$ **URGENT** (PDI: 96, 100% Free).
5. `FD-1005`: **Baby Spinach & Greens** — *Expires in 4 days ($D=4$)* $\rightarrow$ **URGENT** (PDI: 92, 50% Off).
6. `FD-1006`: **Cottage Cheese 500g** — *Expires in 6 days ($D=6$)* $\rightarrow$ **HIGH** (PDI: 88, 50% Off).
7. `FD-1007`: **Farm Fresh Apples** — *Expires in 12 days ($D=12$)* $\rightarrow$ **HIGH** (PDI: 76, Base Price).
8. `FD-1008`: **Whole Wheat Pasta** — *Expires in 20 days ($D=20$)* $\rightarrow$ **MEDIUM** (PDI: 60, Base Price).
9. `FD-1009`: **Canned Kidney Beans** — *Expires in 60 days ($D=60$)* $\rightarrow$ **LOW** (PDI: 1, Base Price).
10. `FD-1010`: **White Basmati Rice 5kg** — *Expires in 180 days ($D=180$)* $\rightarrow$ **LOW** (PDI: 1, Base Price).

---

## 7. Automated Test Suite Results

Command:
```cmd
run_tests.bat
```
Output:
```
==========================================================
  RUNNING CHRONOCHEF AUTOMATED TEST SUITE
==========================================================

--- 1. Testing PDI Formula & Exact Boundaries ---
  [PASS] Expired item (D = -1) receives PDI = 0
  [PASS] Expired item (D = -10) receives PDI = 0
  [PASS] Expired item (D = -1) priority is EXPIRED
  [PASS] Expires today (D = 0) receives PDI = 100
  [PASS] Expires in 1 day (D = 1) receives PDI = 98
  [PASS] Expires in 2 days (D = 2) receives PDI = 96
  [PASS] Expires in 5 days (D = 5) receives PDI = 90
  [PASS] Boundary D = 5 priority is URGENT
  [PASS] Boundary D = 6 receives PDI = 88
  [PASS] D = 10 receives PDI = 80
  [PASS] Boundary D = 15 receives PDI = 70
  [PASS] Boundary D = 15 priority is HIGH
  [PASS] Boundary D = 16 receives PDI = 68
  [PASS] Boundary D = 30 receives PDI = 40
  [PASS] Boundary D = 30 priority is MEDIUM
  [PASS] Boundary D = 31 receives PDI = 38
  [PASS] Boundary D = 31 priority is LOW
  [PASS] Very long shelf life (D = 200) clamped to min PDI = 1

--- 2. Testing Expired Item Rejection Guard ---
  Expected exception caught: Food Safety Violation: Item is expired (3 days past expiry). Subsidies and distribution are strictly prohibited.
  [PASS] Expired item throws ExpiredItemDistributionException on subsidy check
  [PASS] Expired item blocks dynamic price calculation

--- 3. Testing Rule-Based Dynamic Subsidy Tiers ---
  [PASS] D = 0 gets 100% subsidy (FREE)
  [PASS] D = 2 gets 100% subsidy (FREE)
  [PASS] D = 5 gets 50% subsidy (Half Price Rs. 20)
  [PASS] D = 10 gets 0% subsidy (Full Base Price Rs. 40)

--- 4. Testing Inheritance & Dynamic Method Dispatch ---
  [PASS] PerishableItem overrides storage instructions
  [PASS] PackagedItem overrides storage instructions

--- 5. Testing DatabaseManager Singleton & CRUD Operations ---
  [PASS] DatabaseManager implements Singleton (db1 == db2)
  [PASS] Database connection is open and active
  [PASS] CRUD: Successfully inserted test item
  [PASS] CRUD: Successfully retrieved item by ID
  [PASS] CRUD: Successfully restocked quantity (50 + 25 = 75)
  [PASS] Transaction: Recorded distribution & deducted stock (75 - 15 = 60)
  [PASS] Transaction: Logged in distribution_records table
  [PASS] CRUD: Successfully cleaned up / deleted test item

--- 6. Testing Bubble Sort Priority Ordering ---
  [PASS] Bubble Sort ordered items by PDI descending (highest urgency first)
==========================================================
  TEST SUITE RESULTS: 35 / 35 TESTS PASSED
  STATUS: ALL TESTS COMPLETED SUCCESSFULLY! (100% PASS)
==========================================================
```

---

## 8. How to Run the Application

* **Launch the GUI Application**: Double-click [`run.bat`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/run.bat)  
  *(Or execute `run.bat` in command line)*
* **Recompile All Source Code**: Double-click [`compile.bat`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/compile.bat)
* **Run Verification Tests**: Double-click [`run_tests.bat`](file:///c:/Users/Harikrishnan/Documents/collage/collage%20java%20project/run_tests.bat)

---

## 9. Professor Viva / Presentation Quick-Reference Guide

* **Q: "How does the system ensure data consistency across all screens?"**  
  > *"All 5 screens share the same model and database layer. When an item is added in Card 1, restocked in Card 3, or distributed in Card 4, the changes are committed immediately to `chronochef.db` via JDBC. `mainFrame.refreshAllViews()` immediately updates the data displayed in all views."*

* **Q: "Why did you use the Singleton pattern for DatabaseManager?"**  
  > *"As taught in Module 3, a Singleton ensures a class has only one instance and provides a global point of access. For an embedded SQLite database, sharing a single synchronized connection avoids connection leaks and file-locking conflicts."*

* **Q: "How does Dynamic Method Dispatch work in your project?"**  
  > *"When `getStorageInstructions()` is called on a superclass reference of type `FoodItem`, Java resolves the method call at runtime depending on whether the actual instance is a `PerishableItem` or a `PackagedItem`, demonstrating runtime polymorphism."*

* **Q: "How does your Priority Distribution Index (PDI) prevent food waste?"**  
  > *"PDI uses the formula $\text{PDI} = 100 - (D \times 2)$. Items nearing expiry have fewer days remaining ($D$), giving them higher PDI scores ($90 - 100$) and classifying them as URGENT. Items with $\le 2$ days left receive a 100% subsidy (free distribution) to encourage immediate pickup before spoiling."*

* **Q: "How are expired items handled?"**  
  > *"Expired items ($D < 0$) receive a PDI score of 0 and are quarantined. The system throws a custom checked exception (`ExpiredItemDistributionException`) before any pricing or subsidy calculation can occur, ensuring unsafe food is never distributed."*
