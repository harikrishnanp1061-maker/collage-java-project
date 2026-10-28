import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._element.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="CBD5E1", sz="4"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>\n'
            f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
            f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
            f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
            f'  <w:left w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'  <w:insideV w:val="none"/>\n'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def build_oop_guide():
    doc = Document()

    # Page Margins (Standard 1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        # Header & Footer setup for subsequent pages
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("ChronoChef — Object-Oriented Programming (OOP) Implementation Guide | PBCST304")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Artificial Intelligence & Machine Learning — Marian Engineering College")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # Styles
    try:
        code_style = doc.styles.add_style('OOPCode', WD_STYLE_TYPE.PARAGRAPH)
    except:
        code_style = doc.styles['OOPCode']
    code_style.font.name = 'Consolas'
    code_style.font.size = Pt(8.0)
    code_style.font.color.rgb = RGBColor(30, 41, 59)
    code_style.paragraph_format.line_spacing = 1.05
    code_style.paragraph_format.space_before = Pt(0)
    code_style.paragraph_format.space_after = Pt(0)
    code_style.paragraph_format.left_indent = Inches(0.2)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(20)
        run.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(16)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h1(text, page_break=True):
        if page_break:
            doc.add_page_break()
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_p(text, space_before=0, space_after=6):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        return p

    def add_bullet(bold_prefix, text, space_after=3):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        
        r1 = p.add_run(bold_prefix)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r1.bold = True
        
        r2 = p.add_run(text)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)
        return p

    def add_code_block(code_str):
        for line in code_str.strip().splitlines():
            p = doc.add_paragraph(style='OOPCode')
            if not line.strip():
                p.add_run(" ")
            else:
                p.add_run(line)

    def add_callout(box_title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.rows[0].cells[0]
        cell.width = Inches(6.5)
        set_cell_shading(cell, "EFF6FF")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        
        # Left border thick blue
        tcPr = cell._element.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>\n'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="1E3A8A"/>\n'
            f'  <w:top w:val="none"/>\n'
            f'  <w:right w:val="none"/>\n'
            f'  <w:bottom w:val="none"/>\n'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"📌 {box_title}: ")
        r_t.bold = True
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = RGBColor(30, 58, 138)
        
        r_b = p.add_run(text)
        r_b.font.name = "Times New Roman"
        r_b.font.size = Pt(10)
        r_b.font.color.rgb = RGBColor(30, 41, 59)

    # =========================================================================
    # COVER / HEADER SECTION
    # =========================================================================
    add_title("CHRONOCHEF: OBJECT-ORIENTED PROGRAMMING (OOP) IMPLEMENTATION & ARCHITECTURAL MAPPING GUIDE")
    add_subtitle("KTU PBCST304: OBJECT ORIENTED PROGRAMMING — B.TECH AI & ML")

    # Metadata Table
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    col_w = [Inches(2.4), Inches(4.1)]
    
    meta_data = [
        ("Course & Syllabus:", "KTU Course PBCST304: Object Oriented Programming (2024 Scheme)"),
        ("Institution & Department:", "Dept. of Artificial Intelligence & Machine Learning, Marian Engineering College"),
        ("Project Team:", "Harikrishnan P (Lead - MEC25AIM029), Athira L S (MEC25AIM019), Abhichandhana C R (MEC25AIM003), Aparna G (MEC25AIM016)"),
        ("Supervision & Evaluation:", "Guide: Ms. Aswathy T K (Asst. Prof.) | HOD: Prof. Balu John")
    ]
    for r_idx, (k, v) in enumerate(meta_data):
        row = meta_tbl.rows[r_idx]
        for c_idx in range(2):
            c = row.cells[c_idx]
            c.width = col_w[c_idx]
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            set_cell_shading(c, "F8FAFC" if r_idx % 2 == 0 else "FFFFFF")
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(k if c_idx == 0 else v)
            run.font.name = "Times New Roman"
            run.font.size = Pt(9.5)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(30, 58, 138)
    set_table_borders(meta_tbl)

    add_p(
        "This technical document provides a rigorous, code-level architectural mapping of all Object-Oriented "
        "Programming concepts implemented in the ChronoChef system. It details the exact source files, classes, methods, "
        "line numbers, and execution rationales, serving as an authoritative evaluation reference for academic viva voce "
        "and syllabus compliance verification.",
        space_before=10,
        space_after=12
    )

    # =========================================================================
    # MASTER MAPPING MATRIX TABLE
    # =========================================================================
    add_h2("Master OOP Concept Implementation Matrix")
    
    master_table = doc.add_table(rows=1, cols=5)
    master_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    master_table.autofit = False
    
    col_widths = [Inches(0.4), Inches(1.3), Inches(1.3), Inches(1.6), Inches(1.9)]
    hdr_cells = master_table.rows[0].cells
    headers = ["#", "OOP Concept", "Core Java Mechanism", "File & Class Location", "System Role & Academic Purpose"]
    for i, h in enumerate(headers):
        hdr_cells[i].width = col_widths[i]
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=80, right=80)
        set_cell_shading(hdr_cells[i], "1E3A8A")
        p = hdr_cells[i].paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.name = "Times New Roman"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(255, 255, 255)

    matrix_rows = [
        ("1", "Classes & Objects", "Class declaration, instantiation via 'new', heap memory allocation", "model/FoodItem.java\nmodel/DistributionRecord.java", "Models real-world relief pantry entities with encapsulated state and behavior."),
        ("2", "Encapsulation & Data Hiding", "private instance fields, public getters, validating setters", "model/FoodItem.java (L13-24, L60-120)\nmodel/DistributionRecord.java", "Protects state integrity; prevents non-positive quantities and invalid base pricing."),
        ("3", "Abstract Classes & Methods", "abstract class FoodItem, abstract String getStorageInstructions()", "model/FoodItem.java (L11, L139)\nInherited by subclasses", "Establishes template entity contract requiring specific food subclasses to define storage."),
        ("4", "Hierarchical Inheritance", "extends keyword; specialized domain entity subclasses", "model/PerishableItem.java (L7)\nmodel/PackagedItem.java (L7)", "Reuses base properties while adding cold-chain temps and packaging seal validations."),
        ("5", "Dynamic Polymorphism (Dispatch)", "@Override annotation; dynamic method overriding at runtime", "model/PerishableItem.java (L29-32)\nmodel/PackagedItem.java (L27-30)", "JVM determines whether to display refrigeration or dry storage directives at runtime."),
        ("6", "Static Polymorphism (Overloading)", "Overloaded method signatures and overloaded constructors", "model/FoodItem.java (L25-58)\nmodel/InventoryOperations.java (L18-24)", "Permits flexible object initialization and multi-criteria inventory lookup (ID/Name/Cat)."),
        ("7", "Interfaces & Realization", "interface keyword, implements keyword, contract realization", "model/InventoryOperations.java (L10)\ndatabase/FoodBankDAO.java (L15)", "Decouples business logic from persistence; guarantees strict contract for CRUD."),
        ("8", "Custom Exception Handling", "extends Exception, checked exceptions, throw & throws", "exception/ExpiredItemDistributionException.java\nexception/InvalidQuantityException.java", "Enforces food safety guardrail; strictly prevents checkout of expired food items."),
        ("9", "Exception Handling (Robustness)", "try-catch-finally blocks, multi-catch, safe resource closure", "database/DatabaseManager.java\nui/DistributionPanel.java (L180-230)", "Handles SQL failures gracefully and releases database Statement/Connection locks safely."),
        ("10", "Singleton Design Pattern", "private static instance, private constructor, synchronized getInstance()", "database/DatabaseManager.java (L14-25)", "Guarantees exactly one thread-safe SQLite connection across the entire application."),
        ("11", "MVC Architecture", "Strict package decoupling across model, view, controller/service", "model/, ui/, service/,\ndatabase/ packages", "Separates GUI rendering from computational decay math and SQLite persistence."),
        ("12", "Generics & Collections", "Vector<FoodItem>, Vector<DistributionRecord>", "model/InventoryOperations.java\nui/InventoryPanel.java (L140-190)", "Provides compile-time type safety and synchronized backing data for Swing tables."),
        ("13", "JDBC Persistence", "Connection, PreparedStatement (parameterized), ResultSet", "database/DatabaseManager.java\ndatabase/FoodBankDAO.java", "Protects against SQL Injection while executing ACID compliant storage operations."),
        ("14", "Event-Driven GUI Model", "Java Swing JFrame, JPanel, CardLayout, ActionListener", "ui/MainFrame.java (L18-120)\nui/InputPanel.java", "Provides authentic desktop UI; handles user events asynchronously via EDT."),
        ("15", "Algorithmic In-Memory Sorting", "Custom Bubble Sort algorithm ordering items by PDI score", "service/PriorityPricingService.java (L110-145)", "Sorts pantry items so that urgently expiring food appears first for rapid dispatch.")
    ]

    for row_data in matrix_rows:
        row = master_table.add_row()
        for idx, text in enumerate(row_data):
            cell = row.cells[idx]
            cell.width = col_widths[idx]
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.12
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(8.5)
            if idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run.bold = True
            elif idx == 1:
                run.bold = True
                run.font.color.rgb = RGBColor(30, 58, 138)
    set_table_borders(master_table)

    # =========================================================================
    # DEEP-DIVE SECTIONS FOR EACH OOP CONCEPT
    # =========================================================================

    # Concept 1
    add_h1("1. Classes, Objects, State & Behavior", page_break=True)
    add_p(
        "A class is a blueprint from which individual objects are created. In ChronoChef, classes encapsulate the real-world "
        "entities of a community relief operation. Objects maintain instance state in heap memory and expose behavioral "
        "methods to operate on that state."
    )
    add_bullet("Implementation Location: ", "model/FoodItem.java (Lines 11-170) and model/DistributionRecord.java (Lines 11-154).")
    add_bullet("Object Instantiation: ", "Main.java (Line 42) and database/DataSeeder.java (Lines 35-75) using new FoodItem subclass instances.")
    add_code_block("""// Example from database/DataSeeder.java: Object instantiation on the JVM Heap
FoodItem milk = new PerishableItem(
    "FD-1001", "Organic Whole Milk (1L)", "Dairy",
    25.0, "Litres", "2026-10-20", "2026-10-29", 45.0, 4.0
);
FoodItem rice = new PackagedItem(
    "FD-1005", "Basmati Rice (5kg Bag)", "Grains",
    40.0, "Bags", "2026-10-01", "2026-11-20", 250.0, "Triple-Layer Foil Seal"
);""")
    add_callout(
        "Academic Context",
        "Demonstrates Module 1 syllabus requirements: class structure, object creation via 'new', constructor execution, "
        "heap reference management, and separation of instance state from class definitions."
    )

    # Concept 2
    add_h2("2. Encapsulation & Data Hiding")
    add_p(
        "Encapsulation is the mechanism that binds together code and the data it manipulates, keeping both safe from outside "
        "interference and misuse. In ChronoChef, all internal state variables are declared strictly private, accessible solely "
        "through public getters and validating setters."
    )
    add_bullet("Implementation Location: ", "model/FoodItem.java (Lines 13-24, 60-120).")
    add_bullet("Integrity Verification: ", "setQuantity(double) enforces non-negative inventory levels; setBasePrice(double) prevents zero or negative retail valuation.")
    add_code_block("""// Encapsulation with defensive setter validation in model/FoodItem.java
private String itemId;
private String name;
private double quantity;
private double basePrice;

public double getQuantity() {
    return this.quantity;
}

public void setQuantity(double quantity) {
    if (quantity < 0) {
        throw new IllegalArgumentException("Inventory quantity cannot be negative: " + quantity);
    }
    this.quantity = quantity;
}""")

    # Concept 3
    add_h2("3. Abstract Classes & Abstract Methods")
    add_p(
        "An abstract class cannot be instantiated directly and serves as a formal superclass template. ChronoChef defines "
        "FoodItem as an abstract class containing common inventory metadata, while declaring getStorageInstructions() as an "
        "abstract method to compel all concrete food categories to provide specialized environmental preservation guidelines."
    )
    add_bullet("Implementation Location: ", "model/FoodItem.java (Line 11, Line 139).")
    add_bullet("Abstract Signature: ", "public abstract String getStorageInstructions();")
    add_code_block("""// Abstract Class Template in model/FoodItem.java
public abstract class FoodItem {
    protected String itemId;
    protected String name;
    // ... Common state fields ...

    /**
     * Abstract method enforcing specialized preservation directives.
     * Must be implemented by all derived concrete subclasses.
     */
    public abstract String getStorageInstructions();
}""")

    # Concept 4
    add_h1("4. Hierarchical Inheritance", page_break=True)
    add_p(
        "Inheritance is the mechanism by which one class acquires the properties and behaviors of another class. ChronoChef "
        "implements hierarchical inheritance where multiple specialized subclasses extend the common FoodItem abstract parent. "
        "Additionally, custom system exceptions extend the standard Java Exception class."
    )
    add_bullet("Cold-Chain Subclass: ", "model/PerishableItem.java extends FoodItem (adding requiredTempCelsius).")
    add_bullet("Dry Goods Subclass: ", "model/PackagedItem.java extends FoodItem (adding packagingType).")
    add_bullet("Exception Subclasses: ", "exception/ExpiredItemDistributionException.java extends Exception.")
    add_code_block("""// Hierarchical Subclass 1: Cold-Chain Food Items (model/PerishableItem.java)
public class PerishableItem extends FoodItem {
    private double requiredTempCelsius;

    public PerishableItem(String itemId, String name, String category, double quantity,
                          String unit, String dateReceived, String expiryDate,
                          double basePrice, double requiredTempCelsius) {
        super(itemId, name, category, quantity, unit, dateReceived, expiryDate, basePrice);
        this.requiredTempCelsius = requiredTempCelsius;
    }
}

// Hierarchical Subclass 2: Ambient Packaged Goods (model/PackagedItem.java)
public class PackagedItem extends FoodItem {
    private String packagingType;

    public PackagedItem(String itemId, String name, String category, double quantity,
                        String unit, String dateReceived, String expiryDate,
                        double basePrice, String packagingType) {
        super(itemId, name, category, quantity, unit, dateReceived, expiryDate, basePrice);
        this.packagingType = packagingType;
    }
}""")

    # Concept 5
    add_h2("5. Dynamic Polymorphism (Runtime Method Dispatch)")
    add_p(
        "Dynamic Polymorphism is the process by which a call to an overridden method is resolved at runtime rather than compile-time. "
        "In ChronoChef, when iterating over a heterogeneous collection of FoodItem references, calling item.getStorageInstructions() "
        "invokes the specialized subclass implementation dynamically based on the actual object instance present on the heap."
    )
    add_bullet("PerishableItem Override: ", "Returns cold-chain temperature directives (e.g., 'Keep Refrigerated at 4.0°C').")
    add_bullet("PackagedItem Override: ", "Returns dry storage instructions and packaging seal integrity details.")
    add_code_block("""// Dynamic Method Dispatch at runtime
@Override
public String getStorageInstructions() {
    return "Keep Refrigerated at " + this.requiredTempCelsius + "°C (Cold-Chain)";
}

// In ui/InventoryPanel.java: Polymorphic execution across mixed items
for (FoodItem item : inventoryVector) {
    // JVM dynamically resolves getStorageInstructions() based on actual object type
    String storageInfo = item.getStorageInstructions();
    tableModel.addRow(new Object[]{ item.getName(), item.getCategory(), storageInfo });
}""")

    # Concept 6
    add_h2("6. Static Polymorphism (Method & Constructor Overloading)")
    add_p(
        "Static (compile-time) polymorphism occurs when multiple methods or constructors in the same class share the same "
        "identifier but possess distinct parameter lists (different arity or types). ChronoChef implements constructor "
        "overloading for entity instantiation and method overloading for flexible inventory querying."
    )
    add_bullet("Constructor Overloading: ", "model/FoodItem.java provides full parameterized constructor and minimal fallback constructor.")
    add_bullet("Method Overloading: ", "model/InventoryOperations.java and database/FoodBankDAO.java declare searchItems(keyword), searchItems(category, onlyActive), and getItemById(itemId).")
    add_code_block("""// Overloaded Query Methods in model/InventoryOperations.java
public Vector<FoodItem> searchItems(String keyword);
public Vector<FoodItem> searchItems(String category, boolean onlyActive);
public FoodItem getItemById(String itemId);""")

    # Concept 7
    add_h1("7. Interfaces & Contractual Realization", page_break=True)
    add_p(
        "An interface is a completely abstract type used to specify a contractual behavior that classes must implement. "
        "ChronoChef defines InventoryOperations to enforce a strict boundary between user interface controllers and the "
        "underlying database access layer, achieving 100% loose coupling."
    )
    add_bullet("Interface Definition: ", "model/InventoryOperations.java (Lines 10-44).")
    add_bullet("Interface Realization: ", "database/FoodBankDAO.java implements InventoryOperations (Lines 15-381).")
    add_code_block("""// Contractual Interface in model/InventoryOperations.java
public interface InventoryOperations {
    public boolean addItem(FoodItem item);
    public boolean updateStock(String itemId, double newQuantity);
    public boolean deleteItem(String itemId);
    public Vector<FoodItem> getAllItems();
    public FoodItem getItemById(String itemId);
    public boolean recordDistribution(DistributionRecord record)
        throws ExpiredItemDistributionException, InvalidQuantityException;
}

// Realization in database/FoodBankDAO.java
public class FoodBankDAO implements InventoryOperations {
    @Override
    public boolean addItem(FoodItem item) { /* JDBC PreparedStatement Insert */ }
    
    @Override
    public boolean recordDistribution(DistributionRecord record)
        throws ExpiredItemDistributionException, InvalidQuantityException {
        // Enforces safety guardrails prior to executing SQL transaction
    }
}""")

    # Concept 8 & 9
    add_h2("8. Custom Exception Handling & Safety Guardrails")
    add_p(
        "Custom exceptions extend the standard Exception hierarchy to represent domain-specific fault states. ChronoChef "
        "creates custom checked exceptions to enforce strict public health safety rules and inventory volume invariants."
    )
    add_bullet("Expired Food Barrier: ", "exception/ExpiredItemDistributionException.java ensures no volunteer can distribute expired goods.")
    add_bullet("Quantity Barrier: ", "exception/InvalidQuantityException.java blocks zero, negative, or overdraft checkout volumes.")
    add_code_block("""// Custom Checked Exception enforcing Public Health Safety
package exception;

public class ExpiredItemDistributionException extends Exception {
    private String itemId;
    private int daysRemaining;

    public ExpiredItemDistributionException(String itemId, String itemName, int daysRemaining) {
        super("CRITICAL SAFETY VIOLATION: Cannot distribute expired food item [" + 
              itemId + " - " + itemName + "]! Expiry was " + Math.abs(daysRemaining) + " days ago.");
        this.itemId = itemId;
        this.daysRemaining = daysRemaining;
    }

    public int getDaysRemaining() { return daysRemaining; }
}""")

    add_h2("9. Robust Exception Handling (Try-Catch-Finally Architecture)")
    add_p(
        "ChronoChef uses structured try-catch-finally blocks to intercept checked exceptions, display user-friendly modal "
        "alerts in Java Swing, and ensure database Statement and Connection resources are closed deterministically in all execution paths."
    )
    add_code_block("""// Safe Resource Management & Safety Interception in ui/DistributionPanel.java
try {
    dao.recordDistribution(record);
    JOptionPane.showMessageDialog(this, "Distribution Completed Successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
} catch (ExpiredItemDistributionException ex) {
    JOptionPane.showMessageDialog(this, ex.getMessage(), "Food Safety Violation", JOptionPane.ERROR_MESSAGE);
} catch (InvalidQuantityException ex) {
    JOptionPane.showMessageDialog(this, ex.getMessage(), "Input Quantity Error", JOptionPane.WARNING_MESSAGE);
} catch (SQLException ex) {
    JOptionPane.showMessageDialog(this, "Database Transaction Failed: " + ex.getMessage(), "SQL Error", JOptionPane.ERROR_MESSAGE);
} finally {
    refreshTable(); // Always update UI state regardless of success or failure
}""")

    # Concept 10
    add_h1("10. Singleton Design Pattern", page_break=True)
    add_p(
        "The Singleton pattern ensures that a class has only one instance while providing a global access point to that instance. "
        "In ChronoChef, DatabaseManager implements the Singleton pattern with synchronized initialization to prevent multiple "
        "threads from establishing concurrent, conflicting SQLite file locks."
    )
    add_bullet("Implementation Location: ", "database/DatabaseManager.java (Lines 14-25).")
    add_bullet("Pattern Elements: ", "1) private static instance; 2) private constructor; 3) public static synchronized getInstance().")
    add_code_block("""// Thread-Safe Singleton Implementation in database/DatabaseManager.java
public class DatabaseManager {
    private static DatabaseManager instance;
    private Connection connection;

    // 1. Private constructor blocks direct instantiation from external classes
    private DatabaseManager() {
        initConnection();
        createTables();
    }

    // 2. Synchronized global access point
    public static synchronized DatabaseManager getInstance() {
        if (instance == null) {
            instance = new DatabaseManager();
        }
        return instance;
    }

    public Connection getConnection() {
        return this.connection;
    }
}""")

    # Concept 11
    add_h2("11. Model-View-Controller (MVC) Architectural Pattern")
    add_p(
        "ChronoChef strictly decouples data representation, presentation, and algorithmic processing across four clean packages:"
    )
    add_bullet("Model (model/): ", "Encapsulates food items, relief distribution records, and contractual interfaces.")
    add_bullet("View (ui/): ", "Java Swing graphical panels (Input, Inventory, Management, Distribution, Analytics) organized under MainFrame.")
    add_bullet("Controller / Service (service/, database/): ", "Computes PDI decay scores, applies tiered subsidies, and persists state via FoodBankDAO.")

    # Concept 12
    add_h2("12. Java Collections & Generics")
    add_p(
        "Generics introduce compile-time type safety, eliminating the necessity for explicit type casting. ChronoChef utilizes "
        "Vector<FoodItem> and Vector<DistributionRecord> as synchronized collections that interface directly with Swing DefaultTableModel."
    )
    add_code_block("""// Type-Safe Collection Declaration in model/InventoryOperations.java
Vector<FoodItem> getAllItems();
Vector<DistributionRecord> getAllDistributions();

// Thread-safe table iteration in ui/AnalyticsPanel.java
Vector<DistributionRecord> records = dao.getAllDistributions();
for (DistributionRecord rec : records) {
    totalKgDistributed += rec.getDistributedQty();
    totalSubsidySaved += (rec.getBasePrice() - rec.getEffectivePrice()) * rec.getDistributedQty();
}""")

    # Concept 13
    add_h1("13. JDBC Persistence & SQL Injection Defense", page_break=True)
    add_p(
        "Java Database Connectivity (JDBC) standardizes relational database interactions. In database/FoodBankDAO.java, all "
        "queries are executed via parameterized PreparedStatement objects, completely eliminating SQL Injection vulnerabilities "
        "while ensuring atomic database commits."
    )
    add_code_block("""// Parameterized PreparedStatement in database/FoodBankDAO.java
String sql = "INSERT INTO food_items (item_id, name, category, item_type, quantity, unit, " +
             "date_received, expiry_date, base_price, storage_info) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
    pstmt.setString(1, item.getItemId());
    pstmt.setString(2, item.getName());
    pstmt.setString(3, item.getCategory());
    pstmt.setString(4, item instanceof PerishableItem ? "PERISHABLE" : "PACKAGED");
    pstmt.setDouble(5, item.getQuantity());
    pstmt.setString(6, item.getUnit());
    pstmt.setString(7, item.getDateReceived());
    pstmt.setString(8, item.getExpiryDate());
    pstmt.setDouble(9, item.getBasePrice());
    pstmt.setString(10, item.getStorageInstructions());
    pstmt.executeUpdate();
}""")

    # Concept 14
    add_h2("14. Event-Driven GUI Programming (Java Swing & AWT)")
    add_p(
        "ChronoChef is constructed with Java Swing and AWT layout managers, coordinating views through CardLayout and "
        "the Delegation Event Model. Thread safety is guaranteed by launching the UI on the Event Dispatch Thread (EDT)."
    )
    add_bullet("EDT Lifecycle: ", "SwingUtilities.invokeLater(() -> new MainFrame().setVisible(true)) in Main.java.")
    add_bullet("Delegation Listeners: ", "ActionListener attached to donation intake, category filters, and checkout buttons.")
    add_bullet("CardLayout Navigation: ", "MainFrame switches between 5 modular view panels seamlessly without recreating windows.")

    # Concept 15
    add_h2("15. Algorithmic In-Memory Sorting (Custom Bubble Sort)")
    add_p(
        "To fulfill the First-Expired, First-Out (FEFO) food banking principle, ChronoChef implements an in-memory Bubble Sort "
        "algorithm in service/PriorityPricingService.java. The algorithm sorts Vector<FoodItem> in descending order of the Priority "
        "Distribution Index (PDI), ensuring critical near-expiry batches appear at the top of the volunteer screen."
    )
    add_code_block("""// In-Memory Bubble Sort prioritizing food items by PDI score (service/PriorityPricingService.java)
public static void sortByPriorityDescending(Vector<FoodItem> items) {
    if (items == null || items.size() <= 1) return;
    int n = items.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            int pdi1 = calculatePDI(getDaysRemaining(items.get(j).getExpiryDate()));
            int pdi2 = calculatePDI(getDaysRemaining(items.get(j + 1).getExpiryDate()));
            // Swap if preceding item has lower priority score
            if (pdi1 < pdi2) {
                FoodItem temp = items.get(j);
                items.set(j, items.get(j + 1));
                items.set(j + 1, temp);
            }
        }
    }
}""")

    # =========================================================================
    # VIVA VOCE EXAMINATION CHEAT SHEET
    # =========================================================================
    add_h1("16. Viva Voce Examination Q&A Cheat Sheet", page_break=True)
    add_p("Comprehensive answers to the most probable OOP architecture questions asked during university evaluation:")

    viva_qa = [
        ("Q1: Why did you declare FoodItem as an abstract class instead of an interface?",
         "FoodItem represents a foundational entity with substantial common state (itemId, name, quantity, basePrice) and concrete setter validation methods that are shared across all food categories. An interface cannot hold mutable instance state. Making FoodItem an abstract class allows code reuse for common attributes while enforcing getStorageInstructions() as an abstract method for specialized subclasses."),
        
        ("Q2: Where is Dynamic Method Dispatch demonstrated in your project?",
         "It occurs when calling item.getStorageInstructions() on a generic FoodItem reference. If the object on the heap is a PerishableItem, the JVM dynamically invokes PerishableItem.getStorageInstructions() to return refrigeration temperatures. If it is a PackagedItem, it dynamically executes PackagedItem.getStorageInstructions() to return seal integrity data."),
        
        ("Q3: Why is DatabaseManager implemented as a Singleton?",
         "SQLite operates in file-locking mode. Creating multiple database manager instances across different UI panels would lead to concurrent connection attempts, database lock exceptions, and connection leaks. The Singleton pattern guarantees exactly one thread-safe connection instance globally."),
        
        ("Q4: How do your custom exceptions contribute to software robustness?",
         "ExpiredItemDistributionException and InvalidQuantityException are checked exceptions. By declaring them on the DAO distribution method signature, the compiler forces any calling UI controller to wrap checkouts in a try-catch block, guaranteeing that expired food can never be checked out under any operational circumstance."),
        
        ("Q5: What is the purpose of the InventoryOperations interface?",
         "It enforces the Dependency Inversion Principle. The UI views (DistributionPanel, InputPanel) program against the InventoryOperations interface contract rather than the concrete FoodBankDAO implementation. This allows swapping the SQLite storage engine with PostgreSQL or cloud mock engines without modifying any UI code.")
    ]

    for q, a in viva_qa:
        add_p(f"{q}", space_before=6, space_after=2)
        doc.paragraphs[-1].runs[0].bold = True
        doc.paragraphs[-1].runs[0].font.color.rgb = RGBColor(30, 58, 138)
        add_p(f"Answer: {a}", space_before=0, space_after=8)

    # Save document
    out_docx = "ChronoChef_OOP_Concepts_Implementation_Guide.docx"
    doc.save(out_docx)
    print(f"Successfully generated {out_docx}!")

if __name__ == "__main__":
    build_oop_guide()
