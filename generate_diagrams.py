import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    font_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts", font_name)
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    x0, y0, x1, y1 = bbox
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)

def draw_uml_class(draw, x, y, width, height, title, subtitle, attributes, methods, header_bg="#1E3A8A"):
    # Card Background
    draw_rounded_rect(draw, (x, y, x + width, y + height), radius=8, fill="#FFFFFF", outline="#94A3B8", width=2)
    # Header
    draw_rounded_rect(draw, (x, y, x + width, y + 42), radius=8, fill=header_bg)
    draw.rectangle([x, y + 25, x + width, y + 42], fill=header_bg) # Flatten bottom corners of header
    
    font_title = get_font(13, bold=True)
    font_sub = get_font(10, bold=False)
    font_body = get_font(11, bold=False)
    font_body_b = get_font(11, bold=True)
    
    # Title & Subtitle
    draw.text((x + width//2, y + 12), title, fill="#FFFFFF", font=font_title, anchor="mm")
    if subtitle:
        draw.text((x + width//2, y + 28), subtitle, fill="#E2E8F0", font=font_sub, anchor="mm")
        
    # Dividing line after attributes
    curr_y = y + 48
    for attr in attributes:
        draw.text((x + 10, curr_y), attr, fill="#1E293B", font=font_body)
        curr_y += 16
        
    draw.line([x, curr_y + 4, x + width, curr_y + 4], fill="#CBD5E1", width=1)
    curr_y += 8
    
    for m in methods:
        draw.text((x + 10, curr_y), m, fill="#0F172A", font=font_body)
        curr_y += 16

def generate_class_diagram():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw_rounded_rect(draw, (20, 15, w - 20, 60), radius=6, fill="#0F172A")
    title_font = get_font(18, bold=True)
    sub_font = get_font(12, bold=False)
    draw.text((w//2, 38), "CHRONOCHEF: OBJECT-ORIENTED CLASS & ARCHITECTURE DIAGRAM (PBCST304)", fill="#FFFFFF", font=title_font, anchor="mm")
    
    # 1. Base Class: FoodItem (Encapsulation)
    draw_uml_class(draw, 40, 85, 270, 260, 
                   "FoodItem (Abstract)", "<<Base Entity - Encapsulation>>",
                   ["- itemId : String", "- name : String", "- category : String", 
                    "- quantity : double", "- unit : String", "- dateReceived : String", 
                    "- expiryDate : String", "- basePrice : double"],
                   ["+ getDaysRemaining() : long", 
                    "+ getStorageInstructions()* : String", 
                    "+ getItemClassification()* : String", 
                    "+ getters() / setters()"],
                   header_bg="#1E3A8A")

    # 2. Subclass 1: PerishableItem (Inheritance)
    draw_uml_class(draw, 40, 400, 270, 150, 
                   "PerishableItem", "<<Inheritance: extends FoodItem>>",
                   ["- optimalStorageTemp : double"],
                   ["+ getStorageInstructions() : String", 
                    "+ getItemClassification() : String",
                    "+ getOptimalStorageTemp() : double"],
                   header_bg="#2563EB")

    # 3. Subclass 2: PackagedItem (Inheritance)
    draw_uml_class(draw, 40, 580, 270, 150, 
                   "PackagedItem", "<<Inheritance: extends FoodItem>>",
                   ["- sealIntegrityVerified : boolean", "- packagingType : String"],
                   ["+ getStorageInstructions() : String", 
                    "+ getItemClassification() : String"],
                   header_bg="#2563EB")

    # Inheritance arrows: PerishableItem & PackagedItem -> FoodItem
    draw.line([175, 400, 175, 347], fill="#2563EB", width=2)
    draw.polygon([(175, 347), (170, 357), (180, 357)], fill="#2563EB")
    
    draw.line([310, 655, 335, 655, 335, 300, 312, 300], fill="#2563EB", width=2)

    # 4. Interface: InventoryOperations (Module 3)
    draw_uml_class(draw, 350, 85, 260, 180, 
                   "<<interface>>", "InventoryOperations",
                   [],
                   ["+ addItem(item: FoodItem) : boolean",
                    "+ getAllItems() : Vector<FoodItem>",
                    "+ updateItem(item: FoodItem) : boolean",
                    "+ deleteItem(itemId: String) : boolean",
                    "+ restockItem(id, qty) : boolean",
                    "+ logDistribution(r: DistRecord) : bool"],
                   header_bg="#0D9488")

    # 5. DAO Implementation: FoodBankDAO
    draw_uml_class(draw, 350, 310, 260, 220, 
                   "FoodBankDAO", "<<implements InventoryOperations>>",
                   ["- dbManager : DatabaseManager"],
                   ["+ addItem(FoodItem) : boolean",
                    "+ searchItems(name) : Vector",
                    "+ searchItems(cat, days) : Vector",
                    "+ getAllItems() : Vector<FoodItem>",
                    "+ updateQuantity(id, dQty) : boolean",
                    "+ logDistribution(...) : boolean",
                    "+ getDistributionHistory() : Vector"],
                   header_bg="#0F766E")

    # Implements dashed line: FoodBankDAO -> InventoryOperations
    for y_dash in range(267, 308, 6):
        draw.line([480, y_dash, 480, y_dash + 3], fill="#0D9488", width=2)
    draw.polygon([(480, 267), (475, 277), (485, 277)], fill="#0D9488")

    # 6. DatabaseManager (Singleton Pattern - Module 3)
    draw_uml_class(draw, 350, 560, 260, 170, 
                   "DatabaseManager", "<<Singleton Pattern - JDBC>>",
                   ["- static instance : DatabaseManager",
                    "- connection : Connection",
                    "- static DB_URL : String"],
                   ["- DatabaseManager()",
                    "+ static getInstance() : DBManager",
                    "+ getConnection() : Connection",
                    "- createTables() : void"],
                   header_bg="#4338CA")

    # Association DAO -> DatabaseManager
    draw.line([480, 532, 480, 558], fill="#4338CA", width=2)

    # 7. PriorityPricingService (Algorithm Engine)
    draw_uml_class(draw, 640, 85, 260, 220, 
                   "PriorityPricingService", "<<Business Logic & Algorithm>>",
                   ["+ URGENT_THRESHOLD = 5",
                    "+ HIGH_THRESHOLD = 15",
                    "+ MEDIUM_THRESHOLD = 30"],
                   ["+ calcDaysRemaining(expiry) : long",
                    "+ calcPDIScore(days) : int",
                    "+ calcSubsidyDiscount(days) : double",
                    "+ calcEffectivePrice(base, days)",
                    "+ getPriorityBadge(days) : String",
                    "+ sortItemsByUrgency(Vector)"],
                   header_bg="#B45309")

    # 8. Custom Exceptions (Module 3)
    draw_uml_class(draw, 640, 340, 260, 160, 
                   "Custom Exceptions", "<<Module 3 - Robust Exception Handling>>",
                   [],
                   ["+ ExpiredItemDistributionException",
                    "  (Extends Exception - Blocks expired)",
                    "",
                    "+ InvalidQuantityException",
                    "  (Extends Exception - Validates inputs)"],
                   header_bg="#BE123C")

    # 9. UI Presentation Tier (Module 4 Swings & MVC View)
    draw_uml_class(draw, 930, 85, 240, 420, 
                   "MainFrame (JFrame)", "<<MVC View Coordinator - CardLayout>>",
                   ["- cardLayout : CardLayout",
                    "- cardsPanel : JPanel",
                    "- inputPanel : InputPanel",
                    "- inventoryPanel : InventoryPanel",
                    "- managementPanel : ManagePanel",
                    "- distributionPanel : DistPanel",
                    "- analyticsPanel : AnalyticsPanel",
                    "- navButtons : JButton[]"],
                   ["+ MainFrame()",
                    "+ actionPerformed(ActionEvent e)",
                    "+ highlightActiveButton(JButton)",
                    "+ refreshAllViews() : void",
                    "+ showCard(String cardName)"],
                   header_bg="#0F172A")

    # 10. DistributionRecord Model
    draw_uml_class(draw, 640, 535, 260, 195, 
                   "DistributionRecord", "<<Transaction Model Entity>>",
                   ["- transId : String", "- itemId : String", "- itemName : String", 
                    "- recipient : String", "- quantity : double", "- basePrice : double",
                    "- discountPct : double", "- totalValue : double", "- transDate : String"],
                   ["+ getters() / setters()",
                    "+ getFormattedReceipt() : String"],
                   header_bg="#1E3A8A")

    # Save Class Diagram
    img.save("screenshots/class_diagram.png")
    print("Class diagram saved to screenshots/class_diagram.png")

def generate_database_diagram():
    w, h = 1200, 620
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    
    # Title Banner
    draw_rounded_rect(draw, (20, 15, w - 20, 60), radius=6, fill="#0F172A")
    title_font = get_font(18, bold=True)
    draw.text((w//2, 38), "CHRONOCHEF: RELATIONAL DATABASE SCHEMA & ARCHITECTURE (SQLite / JDBC)", fill="#FFFFFF", font=title_font, anchor="mm")

    font_title = get_font(14, bold=True)
    font_col_b = get_font(11, bold=True)
    font_col = get_font(11, bold=False)

    # Table 1: food_items
    t1_x, t1_y, t1_w, t1_h = 60, 100, 480, 460
    draw_rounded_rect(draw, (t1_x, t1_y, t1_x + t1_w, t1_y + t1_h), radius=8, fill="#FFFFFF", outline="#1E3A8A", width=2)
    draw_rounded_rect(draw, (t1_x, t1_y, t1_x + t1_w, t1_y + 45), radius=8, fill="#1E3A8A")
    draw.rectangle([t1_x, t1_y + 25, t1_x + t1_w, t1_y + 45], fill="#1E3A8A")
    draw.text((t1_x + t1_w//2, t1_y + 22), "TABLE: food_items (Master Inventory)", fill="#FFFFFF", font=font_title, anchor="mm")

    t1_cols = [
        ("item_id", "VARCHAR(20)", "PRIMARY KEY", "Unique Food Batch Tracking ID (FD-XXXX)"),
        ("name", "VARCHAR(100)", "NOT NULL", "Food item description / title"),
        ("category", "VARCHAR(50)", "NOT NULL", "Dairy, Bakery, Produce, Canned, Grains"),
        ("item_type", "VARCHAR(20)", "NOT NULL", "PERISHABLE or PACKAGED (OOP Polymorphism)"),
        ("quantity", "DOUBLE", "NOT NULL", "Available stock balance (> 0)"),
        ("unit", "VARCHAR(20)", "NOT NULL", "kg, Liters, Packs, Loaves, Cans"),
        ("date_received", "VARCHAR(10)", "NOT NULL", "ISO Date Format: YYYY-MM-DD"),
        ("expiry_date", "VARCHAR(10)", "NOT NULL", "ISO Expiry Date used for PDI Calculation"),
        ("base_price", "DOUBLE", "NOT NULL", "Normal fair market retail price (INR)"),
        ("storage_info", "VARCHAR(100)", "NULLABLE", "Refrigeration Temp or Packaging Type")
    ]

    curr_y = t1_y + 60
    for col, c_type, constraint, desc in t1_cols:
        color = "#B91C1C" if "PRIMARY" in constraint else "#1E293B"
        draw.text((t1_x + 15, curr_y), f"{col}", fill=color, font=font_col_b)
        draw.text((t1_x + 130, curr_y), f"{c_type}", fill="#475569", font=font_col)
        draw.text((t1_x + 230, curr_y), f"[{constraint}]", fill="#D97706" if "PRIMARY" in constraint else "#059669", font=font_col_b)
        draw.text((t1_x + 15, curr_y + 16), f"• {desc}", fill="#64748B", font=get_font(9.5))
        draw.line([t1_x + 10, curr_y + 34, t1_x + t1_w - 10, curr_y + 34], fill="#F1F5F9", width=1)
        curr_y += 38

    # Table 2: distribution_records
    t2_x, t2_y, t2_w, t2_h = 660, 100, 480, 460
    draw_rounded_rect(draw, (t2_x, t2_y, t2_x + t2_w, t2_y + t2_h), radius=8, fill="#FFFFFF", outline="#0D9488", width=2)
    draw_rounded_rect(draw, (t2_x, t2_y, t2_x + t2_w, t2_y + 45), radius=8, fill="#0D9488")
    draw.rectangle([t2_x, t2_y + 25, t2_x + t2_w, t2_y + 45], fill="#0D9488")
    draw.text((t2_x + t2_w//2, t2_y + 22), "TABLE: distribution_records (Audit & Billing)", fill="#FFFFFF", font=font_title, anchor="mm")

    t2_cols = [
        ("trans_id", "VARCHAR(20)", "PRIMARY KEY", "Unique Distribution Transaction ID (TX-XXXX)"),
        ("item_id", "VARCHAR(20)", "FOREIGN KEY", "References food_items(item_id)"),
        ("item_name", "VARCHAR(100)", "NOT NULL", "Snapshot of item name at distribution time"),
        ("recipient_name", "VARCHAR(100)", "NOT NULL", "Beneficiary Shelter, Kitchen, or Family"),
        ("distributed_qty", "DOUBLE", "NOT NULL", "Quantity deducted from inventory"),
        ("unit", "VARCHAR(20)", "NOT NULL", "Unit of measurement"),
        ("base_price", "DOUBLE", "NOT NULL", "Original base price per unit"),
        ("discount_percent", "DOUBLE", "NOT NULL", "Dynamic Subsidy (0%, 50%, or 100%)"),
        ("effective_price", "DOUBLE", "NOT NULL", "Subsidized price per unit charged"),
        ("total_value", "DOUBLE", "NOT NULL", "Final bill amount: distributed_qty * effective_price"),
        ("trans_date", "VARCHAR(20)", "NOT NULL", "Audit timestamp of distribution")
    ]

    curr_y = t2_y + 55
    for col, c_type, constraint, desc in t2_cols:
        color = "#B91C1C" if "PRIMARY" in constraint else ("#2563EB" if "FOREIGN" in constraint else "#1E293B")
        draw.text((t2_x + 15, curr_y), f"{col}", fill=color, font=font_col_b)
        draw.text((t2_x + 130, curr_y), f"{c_type}", fill="#475569", font=font_col)
        draw.text((t2_x + 230, curr_y), f"[{constraint}]", fill="#D97706" if "PRIMARY" in constraint else ("#2563EB" if "FOREIGN" in constraint else "#059669"), font=font_col_b)
        draw.text((t2_x + 15, curr_y + 14), f"• {desc}", fill="#64748B", font=get_font(9.5))
        draw.line([t2_x + 10, curr_y + 31, t2_x + t2_w - 10, curr_y + 31], fill="#F1F5F9", width=1)
        curr_y += 35

    # Relationship connector between Table 1 and Table 2
    # 1:N relationship
    draw.line([t1_x + t1_w, 170, 600, 170, 600, 205, t2_x, 205], fill="#2563EB", width=3)
    draw.polygon([(t2_x, 205), (t2_x - 10, 200), (t2_x - 10, 210)], fill="#2563EB")
    
    # Label on connector
    draw_rounded_rect(draw, (560, 172, 640, 200), radius=4, fill="#1E293B")
    draw.text((600, 186), "1 : N (FK)", fill="#FFFFFF", font=get_font(10, bold=True), anchor="mm")

    # Bottom notes
    draw.text((w//2, h - 25), "Transactional Integrity: Enforces stock deductions & records immutable distribution audit trail", fill="#64748B", font=get_font(11, bold=True), anchor="mm")

    # Save Database Diagram
    img.save("screenshots/database_design.png")
    print("Database design saved to screenshots/database_design.png")

if __name__ == "__main__":
    generate_class_diagram()
    generate_database_diagram()
