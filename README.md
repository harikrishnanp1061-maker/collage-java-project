# ChronoChef: Smart Dynamic Pricing & Expiry Tracker for Food Banks

**Course**: PBCST304 — Object-Oriented Programming (Semester S3 Project)  
**Technology Stack**: Pure Core Java (Swing GUI, JDBC, SQLite, Event Delegation)  
**Architecture**: Model-View-Controller (MVC) with Single-Window `CardLayout`

---

## 1. Quick Start & Execution

### To Run the Application:
Simply double-click `run.bat` or run in terminal:
```cmd
run.bat
```
*(Or manually: `java -cp "lib/*;bin" Main`)*

### To Recompile All Code:
Double-click `compile.bat` or run:
```cmd
compile.bat
```
*(Or manually: `javac -cp "lib/*;src" -d bin src/exception/*.java src/model/*.java src/database/*.java src/service/*.java src/ui/*.java src/test/*.java src/Main.java`)*

### To Run the Automated Verification Suite:
Double-click `run_tests.bat`:
```cmd
run_tests.bat
```

---

## 2. Implemented Modules & Interfaces

1. **Module A — Data Input Interface (`InputPanel.java`)**:
   - Register incoming food donations with Item ID, Name, Category, Item Type, Quantity, Unit, Received Date, Expiry Date, and Base Price.
   - Comprehensive validation (empty fields check, positive numbers, valid `YYYY-MM-DD` dates).

2. **Module B — Inventory Reading & Expiry Tracking (`InventoryPanel.java`)**:
   - Real-time searching by name and filtering by urgency (*All, Safe to Distribute, Urgent, High, Expired*).
   - Live calculation of **Days Remaining**, **PDI Score (0 to 100)**, and **Priority Classification**.
   - Custom priority color badges and text highlighting.
   - Urgency ordering using a textbook **Bubble Sort** algorithm.

3. **Module C — Inventory Management (`ManagementPanel.java`)**:
   - Edit existing item attributes (name, category, price, expiry date).
   - Restock incoming shipment quantities (`UPDATE quantity = quantity + addQty`).
   - Write-off / delete spoiled or damaged stock with confirmation dialogs.

4. **Module D — Distribution & Dynamic Subsidy Billing (`DistributionPanel.java`)**:
   - Issue food to beneficiaries and shelters with automated stock deduction.
   - **Food Safety Guard**: Strictly blocks expired items from distribution and pricing calculation via `ExpiredItemDistributionException`.
   - **Rule-Based Dynamic Subsidy Tier**:
     - $\le 2$ days: **100% Subsidy (FREE - Rs. 0.00)**
     - $3 - 7$ days: **50% Subsidy (Half Price)**
     - $> 7$ days: **0% Subsidy (Standard Nominal Base Price)**
   - Generates formatted, itemized **Distribution Receipts** in a monospaced view.

5. **Module E — Analysis & Reporting (`AnalyticsPanel.java`)**:
   - 6 aggregated metric cards: Total Items Tracked, Available Volume, Urgent Stock Count, Expired Count, Distributions Completed, Total Subsidized Value.
   - Complete transaction history table showing past distributions.

---

## 3. Strict Syllabus & College Notes Mapping (PBCST304)

| Syllabus Concept | Where Applied in ChronoChef | Course Note Reference |
| :--- | :--- | :--- |
| **Data Abstraction & Encapsulation** | `FoodItem.java`: Private attributes, public getters/setters, parameter validation. | Module 1 (Slides 124-127) |
| **Constructors & `this` keyword** | Default, parameterized, and chained constructors using `this.` to resolve variable hiding. | Module 2 (Slides 108-119) |
| **Hierarchical Inheritance** | Superclass `FoodItem` extended by `PerishableItem` and `PackagedItem` via `extends` and `super(...)`. | Module 2 (Slides 29-38) |
| **Method Overloading** | `FoodBankDAO.searchItems(String name)` vs `searchItems(String category, int maxDays)`. | Module 2 (Slides 6-12) |
| **Method Overriding & Dynamic Dispatch**| `getStorageInstructions()` and `getItemClassification()` overridden in subclasses, called via base references. | Module 2 (Slides 17-26) |
| **Interfaces** | `InventoryOperations.java` interface implemented by `FoodBankDAO.java`. | Module 3 (Slides 54-68) |
| **Custom Exceptions** | `InvalidQuantityException` and `ExpiredItemDistributionException` extending `Exception`. | Module 3 (Slides 34-35) |
| **Singleton Design Pattern** | `DatabaseManager.java` with private constructor, static instance, and synchronized `getInstance()`. | Module 3 Syllabus |
| **Swing Fundamentals & CardLayout** | `JFrame`, `JPanel`, `CardLayout`, `BorderLayout`, `GridLayout`, `JTable`, `JButton`, `JTextField`. | Module 4 (Slides 4-55) |
| **Delegation Event Model** | `ActionListener` and `ActionEvent` handling navigation and button triggers. | Module 4 (Slides 60-76) |
| **Database Applications with JDBC** | Standard SQL CRUD operations (`INSERT`, `SELECT`, `UPDATE`, `DELETE`) with `PreparedStatement` and `ResultSet`. | Module 4 Syllabus (Page 3 & 8) |

---

## 4. Priority Distribution Index (PDI) Exact Formula

$$\text{PDI Score} = 
\begin{cases} 
0 & \text{if } D < 0 \quad (\textbf{EXPIRED - QUARANTINED}) \\
\max\big(1, \; 100 - (D \times 2)\big) & \text{if } D \ge 0 \quad (\textbf{SAFE TO DISTRIBUTE})
\end{cases}$$

* $D < 0 \implies \text{PDI} = 0 \implies$ **EXPIRED** (Distribution Blocked)
* $0 \le D \le 5 \implies \text{PDI} \in [90, 100] \implies$ **URGENT** (100% Free / Immediate Clearance)
* $6 \le D \le 15 \implies \text{PDI} \in [70, 88] \implies$ **HIGH** (50% Subsidy)
* $16 \le D \le 30 \implies \text{PDI} \in [40, 68] \implies$ **MEDIUM** (Standard Rotation)
* $D > 30 \implies \text{PDI} \in [1, 38] \implies$ **LOW** (Long Shelf-Life Goods)

---

## 5. Directory Structure

```
collage java project/
├── bin/                          # Compiled bytecode .class files
├── lib/                          # Standalone dependency JARs
│   ├── sqlite-jdbc.jar           # Pure SQLite JDBC driver
│   ├── slf4j-api.jar             # Driver logging support
│   └── slf4j-simple.jar          # Driver logging binding
├── notes/                        # College lecture slides & handwritten notes
├── src/
│   ├── Main.java                 # Program entry point & Swing launcher
│   ├── database/
│   │   ├── DatabaseManager.java  # Singleton JDBC Connection Manager
│   │   ├── FoodBankDAO.java      # CRUD Data Access Object
│   │   └── DataSeeder.java       # Pre-populates 10 realistic sample food items
│   ├── exception/
│   │   ├── InvalidQuantityException.java
│   │   └── ExpiredItemDistributionException.java
│   ├── model/
│   │   ├── FoodItem.java         # Base entity class (Encapsulation)
│   │   ├── PerishableItem.java   # Subclass (Hierarchical Inheritance)
│   │   ├── PackagedItem.java     # Subclass (Hierarchical Inheritance)
│   │   ├── DistributionRecord.java
│   │   └── InventoryOperations.java # Core Interface
│   ├── service/
│   │   └── PriorityPricingService.java # PDI & Dynamic Pricing Engine
│   ├── test/
│   │   └── ProjectTestRunner.java # 35-point automated verification suite
│   └── ui/
│       ├── MainFrame.java        # Top JFrame with CardLayout navigation
│       ├── InputPanel.java       # Module A: Data Input
│       ├── InventoryPanel.java   # Module B: Expiry Tracker & PDI View
│       ├── ManagementPanel.java  # Module C: Stock Inflow & Edit
│       ├── DistributionPanel.java# Module D: Distribution & Subsidy Billing
│       └── AnalyticsPanel.java   # Module E: Overview & Transaction History
├── chronochef.db                 # Persistent local SQLite database
├── compile.bat                   # 1-Click compiler script
├── run.bat                       # 1-Click application launcher
├── run_tests.bat                 # 1-Click automated test runner
└── README.md                     # Documentation & Viva Cheat Sheet
```
