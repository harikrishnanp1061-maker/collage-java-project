import os
import sys
import re
import textwrap
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# =========================================================================
# NUMBERED CANVAS WITH PROFESSIONAL RUNNING HEADER & FOOTER
# =========================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total pages rendered: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.drawString(36, 810, "CHRONOCHEF: 4-MEMBER PRESENTATION & VIVA MASTER GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(559, 810, "Course PBCST304 (OOP) — Autonomous Role Allocation & Defense")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 804, 559, 804)

            # Footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 42, 559, 42)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 30, "Confidential Student Presentation Reference — Food Bank Dynamic Pricing System")
            page_text = f"Page {self._pageNumber} of {total_pages}"
            self.drawRightString(559, 30, page_text)
        self.restoreState()


# =========================================================================
# MAIN PDF GENERATION SCRIPT
# =========================================================================
def create_guide_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )

    bold_body = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor("#0F172A")
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    speech_box_style = ParagraphStyle(
        'SpeechBoxText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )

    viva_q_style = ParagraphStyle(
        'VivaQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor("#991B1B"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    viva_a_style = ParagraphStyle(
        'VivaAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1F2937"),
        leftIndent=10,
        spaceAfter=6
    )

    code_snippet_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#0F172A")
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.white
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # =========================================================================
    # COVER / HEADER BANNER
    # =========================================================================
    meta_box = [
        [
            Paragraph("<b>Project Title:</b> ChronoChef — Smart Dynamic Pricing & Expiry Tracker", tbl_cell_bold),
            Paragraph("<b>Target Audience:</b> 4-Member Project Team (Viva Prep)", tbl_cell)
        ],
        [
            Paragraph("<b>Course:</b> PBCST304 — Object-Oriented Programming (S3)", tbl_cell),
            Paragraph("<b>Tech Stack:</b> Java SE, Java Swing (MVC), JDBC, SQLite", tbl_cell)
        ],
        [
            Paragraph("<b>Verification Status:</b> 35/35 Test Suite Cases Passing (100%)", tbl_cell),
            Paragraph("<b>Recommended Total Time:</b> 12 Minutes (3 Min / Member) + Viva", tbl_cell)
        ]
    ]
    t_meta = Table(meta_box, colWidths=[270, 253])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    story.append(Spacer(1, 4))
    story.append(Paragraph("CHRONOCHEF: 4-MEMBER PRESENTATION & VIVA GUIDE", title_style))
    story.append(Paragraph("Complete Role Allocation, Technical Breakdown, Word-for-Word Scripts & Viva Defense", subtitle_style))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # =========================================================================
    # MASTER ALLOCATION TABLE
    # =========================================================================
    story.append(Paragraph("1. Master Team Division & Presentation Flow", h1_style))
    story.append(Paragraph(
        "To ensure high marks during the project viva and demonstration, the project is divided into four distinct, "
        "academically rigorous sections. Every member covers a core portion of the syllabus (Modules 1 to 4) "
        "and is personally accountable for specific source code files.",
        body_style
    ))

    alloc_data = [
        [
            Paragraph("<b>Member</b>", tbl_header),
            Paragraph("<b>Designated Role & Focus</b>", tbl_header),
            Paragraph("<b>Syllabus Modules</b>", tbl_header),
            Paragraph("<b>Assigned Source Files</b>", tbl_header),
            Paragraph("<b>Time</b>", tbl_header)
        ],
        [
            Paragraph("<b>Member 1</b>", tbl_cell_bold),
            Paragraph("<b>System Architecture & Core OOP Data Modeling</b><br/>Problem statement, domain needs, Encapsulation, Hierarchical Inheritance, Dynamic Method Dispatch.", tbl_cell),
            Paragraph("Module 1 &<br/>Module 2", tbl_cell),
            Paragraph("<code>model/FoodItem.java</code><br/><code>model/PerishableItem.java</code><br/><code>model/PackagedItem.java</code><br/><code>Main.java</code>", tbl_cell),
            Paragraph("2.5 – 3.0 min", tbl_cell)
        ],
        [
            Paragraph("<b>Member 2</b>", tbl_cell_bold),
            Paragraph("<b>Algorithms, Math Formulations & Pricing Engine</b><br/>Days Remaining formula, Priority Distribution Index (PDI), Dynamic Subsidy Tiers, Textbook Bubble Sort.", tbl_cell),
            Paragraph("Module 1 &<br/>Module 3", tbl_cell),
            Paragraph("<code>service/PriorityPricingService.java</code><br/><code>model/DistributionRecord.java</code>", tbl_cell),
            Paragraph("2.5 – 3.0 min", tbl_cell)
        ],
        [
            Paragraph("<b>Member 3</b>", tbl_cell_bold),
            Paragraph("<b>Database Architecture, Patterns & Safety Exceptions</b><br/>Singleton pattern, DAO pattern, PreparedStatement, Custom Checked Exceptions (compile-time safety).", tbl_cell),
            Paragraph("Module 3 &<br/>Module 4", tbl_cell),
            Paragraph("<code>database/DatabaseManager.java</code><br/><code>database/FoodBankDAO.java</code><br/><code>model/InventoryOperations.java</code><br/><code>exception/*.java</code>", tbl_cell),
            Paragraph("2.5 – 3.0 min", tbl_cell)
        ],
        [
            Paragraph("<b>Member 4</b>", tbl_cell_bold),
            Paragraph("<b>Swing GUI Architecture, Event Handling & Live Demo</b><br/>Single-frame CardLayout, Layout managers, Delegation Event Model, 5 Views walkthrough & Live checkout.", tbl_cell),
            Paragraph("Module 4", tbl_cell),
            Paragraph("<code>ui/MainFrame.java</code><br/><code>ui/InputPanel.java</code><br/><code>ui/InventoryPanel.java</code><br/><code>ui/ManagementPanel.java</code><br/><code>ui/DistributionPanel.java</code>", tbl_cell),
            Paragraph("3.0 – 4.0 min", tbl_cell)
        ]
    ]

    t_alloc = Table(alloc_data, colWidths=[55, 175, 60, 175, 58])
    t_alloc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_alloc)
    story.append(Spacer(1, 10))

    # Seamless Transitions Table
    story.append(Paragraph("Hand-Off Transitions Between Members (Practice This Flow)", h2_style))
    trans_data = [
        [
            Paragraph("<b>Transition</b>", tbl_header),
            Paragraph("<b>Exact Hand-off Phrasing to Memorize</b>", tbl_header)
        ],
        [
            Paragraph("<b>Member 1 &rarr; Member 2</b>", tbl_cell_bold),
            Paragraph("<i>\"Now that we have examined our Object-Oriented data structures and domain entities, my teammate (Member 2) will explain the mathematical logic and sorting algorithms powering item urgency and dynamic subsidies.\"</i>", tbl_cell)
        ],
        [
            Paragraph("<b>Member 2 &rarr; Member 3</b>", tbl_cell_bold),
            Paragraph("<i>\"Having explored how urgency scores and subsidy percentages are computed, my teammate (Member 3) will detail how this data is securely persisted via the Singleton pattern and protected by custom checked exceptions.\"</i>", tbl_cell)
        ],
        [
            Paragraph("<b>Member 3 &rarr; Member 4</b>", tbl_cell_bold),
            Paragraph("<i>\"With the persistence and food safety validation mechanisms established, my teammate (Member 4) will now present our Swing GUI architecture and conduct a live end-to-end demonstration of the application.\"</i>", tbl_cell)
        ]
    ]
    t_trans = Table(trans_data, colWidths=[120, 403])
    t_trans.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F766E")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_trans)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: MEMBER 1 DETAILED GUIDE
    # =========================================================================
    story.append(Paragraph("2. Member 1: System Overview & Core OOP Data Modeling", h1_style))
    story.append(Paragraph("<b>Primary Role:</b> System Architect & Domain Modeler &nbsp;|&nbsp; <b>Syllabus Focus:</b> Module 1 & Module 2", bold_body))
    story.append(Paragraph("<b>Assigned Files:</b> <code>src/model/FoodItem.java</code>, <code>src/model/PerishableItem.java</code>, <code>src/model/PackagedItem.java</code>, <code>src/Main.java</code>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1E3A8A"), spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("A. Deep Technical Concepts to Explain", h2_style))
    story.append(Paragraph("&bull; <b>The Real-World Problem:</b> Over 30% of food in charitable distribution centres spoils on warehouse shelves due to static paper/spreadsheet records, lack of price incentives to move expiring goods, and accidental distribution of unsafe food.", bullet_style))
    story.append(Paragraph("&bull; <b>Model-View-Controller (MVC) Architecture:</b> Explain that ChronoChef cleanly decouples data representation (Model), GUI presentation (View), and persistence/logic (DAO & Service).", bullet_style))
    story.append(Paragraph("&bull; <b>Encapsulation (Data Hiding):</b> In <code>FoodItem.java</code>, all state variables (<code>itemId</code>, <code>name</code>, <code>quantity</code>, <code>basePrice</code>, <code>expiryDate</code>) are strictly declared <code>private</code>. Access is exclusively granted through validated public getters and setters (e.g., throwing <code>IllegalArgumentException</code> if quantity < 0).", bullet_style))
    story.append(Paragraph("&bull; <b>Constructor Overloading & 'this' Keyword:</b> Demonstrates constructor overloading in <code>FoodItem</code>: a minimal constructor for basic entries and a full 9-parameter constructor. The <code>this</code> keyword is used to disambiguate shadowing between parameter names and instance variables (e.g., <code>this.name = name;</code>).", bullet_style))
    story.append(Paragraph("&bull; <b>Hierarchical Inheritance & 'super' Keyword:</b> <code>FoodItem</code> is the superclass. It is extended by two distinct child classes:", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <code>PerishableItem extends FoodItem</code>: Introduces cold-chain attributes: <code>refrigerationTemp</code> and <code>maxStorageDays</code>. Calls <code>super(...)</code> to initialize inherited fields.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. <code>PackagedItem extends FoodItem</code>: Introduces shelf-stability attributes: <code>packagingType</code> (CAN, BOX) and <code>isFragile</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Dynamic Method Dispatch (Runtime Polymorphism):</b> <code>FoodItem</code> declares <code>public String getStorageInstructions()</code>. Both child classes <i>override</i> this method. When invoked on a generic <code>FoodItem item</code> reference, the JVM resolves the exact subclass implementation dynamically at runtime.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Word-for-Word Speaking Script (2.5 - 3.0 Minutes)", h2_style))
    speech_1 = (
        "\"Respected evaluators, our project is ChronoChef — a Smart Dynamic Pricing and Expiry Tracking System "
        "designed specifically for food banks and community pantries. In traditional relief centres, over 30% of donated food "
        "is wasted because inventory is managed statically on spreadsheets, near-expiry food sits at fixed fees until spoilage, "
        "and there is no automated barrier to prevent the accidental distribution of expired food.<br/><br/>"
        "To solve this, ChronoChef implements a pure Model-View-Controller architecture in Java. I will present our core "
        "Object-Oriented data structures mapped to Modules 1 and 2 of our syllabus.<br/><br/>"
        "In our model package, our foundation is the <b>FoodItem</b> base class. We strictly enforce <b>Encapsulation</b> by declaring all fields "
        "private and exposing validated getters and setters. We implemented <b>Constructor Overloading</b> and the <b>this</b> keyword "
        "to differentiate instance variables from constructor parameters.<br/><br/>"
        "To model real-world inventory, we implemented <b>Hierarchical Inheritance</b>. FoodItem is extended by <b>PerishableItem</b>, "
        "which adds cold-chain attributes like refrigeration temperature, and <b>PackagedItem</b>, which tracks packaging seal types. "
        "Both subclasses use the <b>super</b> keyword to delegate base initialization to the superclass constructor.<br/><br/>"
        "Crucially, we demonstrate <b>Dynamic Method Dispatch</b>. The base class defines the method <code>getStorageInstructions()</code>, "
        "which is overridden in both subclasses. When our inventory table renders items, calling this method on a generic FoodItem reference "
        "causes the JVM to resolve the exact child implementation dynamically at runtime. "
        "Now, Member 2 will explain the mathematical algorithms and dynamic pricing engine.\""
    )
    t_speech_1 = Table([[Paragraph(speech_1, speech_box_style)]], colWidths=[523])
    t_speech_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_speech_1)

    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Top Viva Voce Questions & Answers for Member 1", h2_style))
    
    viva_m1 = [
        ("Q1: What is Encapsulation, and how is it proven in your code?",
         "Encapsulation is the OOP mechanism of binding data and methods together while hiding internal object state. In FoodItem.java, all 9 fields (itemId, name, quantity, etc.) are private. They cannot be directly modified from outside classes. They are accessible only through getters and setters, which validate constraints like positive quantities."),
        ("Q2: What is Dynamic Method Dispatch? Where does it execute in ChronoChef?",
         "Dynamic Method Dispatch is runtime polymorphism where an overridden method call is resolved at runtime rather than compile time. In our project, FoodItem declares getStorageInstructions(). PerishableItem returns cold-storage guidelines (e.g., 'Keep chilled at 4°C'), while PackagedItem returns dry-shelf rules. When our DAO iterates over a Vector<FoodItem>, calling item.getStorageInstructions() dynamically invokes the correct child class method."),
        ("Q3: Why did you use Hierarchical Inheritance instead of Multiple Inheritance?",
         "Java does not support multiple inheritance with classes to avoid the Diamond Problem (ambiguity when two parents define the same method). Hierarchical inheritance allows multiple specialized subclasses (PerishableItem and PackagedItem) to inherit from a single common parent (FoodItem), sharing core inventory properties while adding specialized behavior."),
        ("Q4: What is the purpose of the 'super' keyword in your constructors?",
         "In Java, subclass constructors do not automatically inherit parent constructors. The 'super' keyword explicitly calls the superclass constructor (e.g., super(itemId, name, category, ...)), ensuring inherited private fields are initialized properly before child-specific attributes like refrigerationTemp are set."),
        ("Q5: What is constructor overloading and why is it useful here?",
         "Constructor overloading means defining multiple constructors within the same class with different parameter lists. In FoodItem, we provide a default constructor, a basic constructor for fast item creation, and a full 9-parameter constructor for database reconstitution."),
        ("Q6: What is the purpose of Main.java in your application?",
         "Main.java contains the JVM entry point: public static void main(String[] args). It initializes the UI on the Swing Event Dispatch Thread (EDT) using SwingUtilities.invokeLater() to ensure thread safety during GUI creation.")
    ]
    for q, a in viva_m1:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: MEMBER 2 DETAILED GUIDE
    # =========================================================================
    story.append(Paragraph("3. Member 2: Mathematical Formulations, Algorithms & Pricing Engine", h1_style))
    story.append(Paragraph("<b>Primary Role:</b> Lead Algorithm & Business Logic Engineer &nbsp;|&nbsp; <b>Syllabus Focus:</b> Module 1 & Module 3", bold_body))
    story.append(Paragraph("<b>Assigned Files:</b> <code>src/service/PriorityPricingService.java</code>, <code>src/model/DistributionRecord.java</code>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F766E"), spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("A. Deep Technical Concepts to Explain", h2_style))
    story.append(Paragraph("&bull; <b>Date Normalization & Days Remaining (D):</b> Normalizes current timestamp and item expiry timestamp to midnight (00:00:00) to avoid timezone/hour discrepancies. Converts millisecond difference into integer days: <code>D = (expiryMs - currentMs) / (1000 * 60 * 60 * 24)</code>. If D < 0, the item is expired.", bullet_style))
    story.append(Paragraph("&bull; <b>Priority Distribution Index (PDI) Formula:</b> A mathematical metric (0 to 100) indicating distribution urgency:", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;If D < 0: PDI = 0 (Quarantined, Unsafe for human consumption).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;If D &ge; 0: PDI = max(1, min(100, 100 - (D &times; 2))). An item expiring in 2 days gets PDI = 96 (Extremely Urgent).", bullet_style))
    story.append(Paragraph("&bull; <b>Dynamic Subsidy & Clearance Tiers:</b> Replaces static pricing with food-bank relief tiers:", bullet_style))
    
    tier_data = [
        [Paragraph("<b>Days Remaining (D)</b>", tbl_header), Paragraph("<b>PDI Score</b>", tbl_header), Paragraph("<b>Priority Tier</b>", tbl_header), Paragraph("<b>Subsidy %</b>", tbl_header), Paragraph("<b>Effective Price</b>", tbl_header), Paragraph("<b>Action</b>", tbl_header)],
        [Paragraph("D < 0", tbl_cell), Paragraph("0", tbl_cell), Paragraph("EXPIRED", tbl_cell), Paragraph("N/A", tbl_cell), Paragraph("Blocked", tbl_cell), Paragraph("Quarantined; Safety exception thrown", tbl_cell)],
        [Paragraph("0 &le; D &le; 2", tbl_cell), Paragraph("96 – 100", tbl_cell), Paragraph("URGENT", tbl_cell), Paragraph("100% FREE", tbl_cell), Paragraph("$0.00", tbl_cell), Paragraph("Emergency clearance to shelters", tbl_cell)],
        [Paragraph("3 &le; D &le; 7", tbl_cell), Paragraph("86 – 94", tbl_cell), Paragraph("HIGH", tbl_cell), Paragraph("50% OFF", tbl_cell), Paragraph("Base &times; 0.50", tbl_cell), Paragraph("Incentivized distribution", tbl_cell)],
        [Paragraph("D &ge; 8", tbl_cell), Paragraph("1 – 84", tbl_cell), Paragraph("MED / LOW", tbl_cell), Paragraph("0% (None)", tbl_cell), Paragraph("Base Price", tbl_cell), Paragraph("Standard recovery fee", tbl_cell)]
    ]
    t_tier = Table(tier_data, colWidths=[65, 55, 60, 60, 65, 218])
    t_tier.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F766E")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_tier)
    story.append(Spacer(1, 4))

    story.append(Paragraph("&bull; <b>Textbook Bubble Sort Algorithm:</b> In <code>PriorityPricingService.sortByUrgencyDescending(Vector&lt;FoodItem&gt; items)</code>, we sort items in memory using nested loops. Items with higher PDI float to the top of the Vector. Time complexity: O(n&sup2;), Space complexity: O(1) auxiliary space.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Word-for-Word Speaking Script (2.5 - 3.0 Minutes)", h2_style))
    speech_2 = (
        "\"Respected professors, I am responsible for the core mathematical algorithms and dynamic pricing engine "
        "encapsulated inside <b>PriorityPricingService.java</b>. Traditional inventory software treats expiry as a static date. "
        "ChronoChef transforms expiry into a real-time operational urgency index.<br/><br/>"
        "First, we calculate <b>Days Remaining (D)</b> by normalizing both the system time and the item expiry time to midnight, "
        "preventing time-of-day miscalculations. From this, our formula computes the <b>Priority Distribution Index (PDI)</b> "
        "bounded between 0 and 100.<br/><br/>"
        "For safe items, PDI equals <code>100 minus (D multiplied by 2)</code>. As food approaches its expiration date, its PDI increases linearly. "
        "If an item expires (D < 0), its PDI drops to 0, flagging it as hazardous and quarantined.<br/><br/>"
        "We mapped PDI directly to an automated <b>Dynamic Subsidy Model</b>. When an item enters the critical 0 to 2 day window, "
        "our system automatically triggers a 100% subsidy, marking it completely free for community shelters. Items with 3 to 7 days "
        "receive a 50% subsidy to stimulate immediate checkout.<br/><br/>"
        "To present items to pantry managers in strict order of urgency, we implemented a textbook <b>Bubble Sort algorithm</b> "
        "operating on a <code>Vector&lt;FoodItem&gt;</code>. By comparing adjacent PDI values across nested loops, the highest-urgency "
        "items naturally bubble to index zero with O(n&sup2;) time complexity.<br/><br/>"
        "Now, Member 3 will explain our database architecture, design patterns, and food-safety exception handling.\""
    )
    t_speech_2 = Table([[Paragraph(speech_2, speech_box_style)]], colWidths=[523])
    t_speech_2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#16A34A")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_speech_2)

    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Top Viva Voce Questions & Answers for Member 2", h2_style))
    
    viva_m2 = [
        ("Q1: Why did you implement Bubble Sort instead of calling Collections.sort()?",
         "While Collections.sort() uses TimSort (O(n log n)), implementing Bubble Sort demonstrates core syllabus mastery of data structures and algorithms (Module 1). In a local food bank with dozens or hundreds of daily batches, Bubble Sort's O(n²) time complexity executes in fractions of a millisecond while remaining simple, stable, and in-place (O(1) extra memory)."),
        ("Q2: How does the system prevent division-by-zero or negative day errors?",
         "Days Remaining is calculated via millisecond subtraction and integer floor division by 86,400,000 ms. If expiryDate < currentDate, D is strictly negative. The calculatePDI() method checks if (D < 0) before applying the formula, instantly returning 0 without calculation errors."),
        ("Q3: What happens to the pricing if an item is already expired?",
         "If D < 0, calculateEffectivePrice() and calculateSubsidyPercentage() immediately throw an ExpiredItemDistributionException. This blocks execution before any price or receipt generation can proceed."),
        ("Q4: Why did you use Vector<FoodItem> instead of ArrayList<FoodItem> for sorting?",
         "Vector is a legacy synchronized collection class from java.util covered in Module 1. Because multiple UI threads or background refresh events could interact with the inventory data, Vector provides built-in thread safety and seamlessly integrates with Swing's DefaultTableModel."),
        ("Q5: What is the purpose of DistributionRecord.java?",
         "DistributionRecord is an immutable audit model storing completed checkouts: recordId, itemId, recipientOrganization, quantityDistributed, originalPrice, subsidyApplied, finalPrice, and timestamp. It preserves an exact historical log even if the original item is subsequently deleted."),
        ("Q6: How does the 100% subsidy benefit the food bank financially?",
         "Food banks do not operate for commercial profit; their primary KPI is waste avoidance and community nutrition. Spoiled food incurs disposal fees and zero social value. Clearances with a 100% subsidy allow shelters to collect safe food within 48 hours for immediate meal preparation.")
    ]
    for q, a in viva_m2:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: MEMBER 3 DETAILED GUIDE
    # =========================================================================
    story.append(Paragraph("4. Member 3: Database Architecture, Design Patterns & Custom Exceptions", h1_style))
    story.append(Paragraph("<b>Primary Role:</b> Backend Architect, Database Engineer & Safety Officer &nbsp;|&nbsp; <b>Syllabus Focus:</b> Module 3 & Module 4", bold_body))
    story.append(Paragraph("<b>Assigned Files:</b> <code>src/database/DatabaseManager.java</code>, <code>src/database/FoodBankDAO.java</code>, <code>src/model/InventoryOperations.java</code>, <code>src/exception/ExpiredItemDistributionException.java</code>, <code>src/exception/InvalidQuantityException.java</code>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#7C3AED"), spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("A. Deep Technical Concepts to Explain", h2_style))
    story.append(Paragraph("&bull; <b>Singleton Design Pattern (DatabaseManager.java):</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. Private static instance variable: <code>private static DatabaseManager instance = null;</code>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. Private constructor: Prevents instantiation from external classes via <code>new</code>.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3. Public static synchronized accessor: <code>public static synchronized DatabaseManager getInstance()</code>.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Why Critical for SQLite:</i> SQLite is an embedded file-based database (<code>chronochef.db</code>). Opening multiple connection instances causes file-locking collisions (<code>SQLITE_BUSY</code>). The synchronized Singleton guarantees a single, thread-safe connection pipeline.", bullet_style))
    story.append(Paragraph("&bull; <b>Data Access Object (DAO) Pattern & Interface Abstraction:</b> <code>FoodBankDAO</code> implements the <code>InventoryOperations</code> interface. This enforces loose coupling: the GUI never interacts with raw SQL queries, only high-level CRUD methods (<code>addItem</code>, <code>getAllItems</code>, <code>updateQuantity</code>, <code>recordDistribution</code>).", bullet_style))
    story.append(Paragraph("&bull; <b>PreparedStatement & SQL Injection Prevention:</b> All database queries strictly use <code>PreparedStatement</code> with <code>?</code> placeholders. Parameter binding ensures user input is treated strictly as literal data, preventing SQL injection attacks and enabling precompiled query caching.", bullet_style))
    story.append(Paragraph("&bull; <b>Custom Checked Exceptions:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <code>ExpiredItemDistributionException extends Exception</code>: Enforces an unbypassable safety barrier. Thrown when a user attempts to distribute or calculate subsidies on expired food.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. <code>InvalidQuantityException extends Exception</code>: Thrown when requested distribution quantity is &le; 0 or exceeds available warehouse stock.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;<i>Why Checked?</i> Extending <code>java.lang.Exception</code> (rather than <code>RuntimeException</code>) forces compile-time handling: any caller must either catch it in a <code>try-catch</code> block or declare it with <code>throws</code>.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Word-for-Word Speaking Script (2.5 - 3.0 Minutes)", h2_style))
    speech_3 = (
        "\"Respected examiners, I am responsible for our persistence layer, design patterns, and exception architecture, "
        "covering Module 3 and the JDBC topics in Module 4.<br/><br/>"
        "To manage database connectivity, we implemented the <b>Singleton Design Pattern</b> in <b>DatabaseManager.java</b>. "
        "It features a private static instance, a private constructor loading the SQLite JDBC driver, and a public static "
        "synchronized <code>getInstance()</code> method. Because SQLite is a serverless, file-based database, maintaining a single "
        "synchronized connection across the application lifecycle is essential to prevent database-locking collisions.<br/><br/>"
        "For database interactions, we followed the <b>Data Access Object (DAO) Pattern</b>. <b>FoodBankDAO</b> implements the "
        "<b>InventoryOperations</b> interface, providing clean abstraction. Every SQL operation uses <b>PreparedStatement</b> "
        "with parameterized placeholders. This completely neutralizes SQL injection vulnerabilities and optimizes query execution.<br/><br/>"
        "A standout feature of ChronoChef is our safety architecture implemented via <b>Custom Checked Exceptions</b>. "
        "We created <b>ExpiredItemDistributionException</b> and <b>InvalidQuantityException</b> by extending <code>java.lang.Exception</code>. "
        "Because they are checked exceptions, the Java compiler guarantees that no distribution or pricing logic can be executed "
        "without explicit exception handling. If a volunteer attempts to distribute expired stock, our food safety exception halts the "
        "transaction immediately, preventing unsafe food from leaving the facility.<br/><br/>"
        "Now, Member 4 will demonstrate our Swing GUI architecture and conduct a live demonstration.\""
    )
    t_speech_3 = Table([[Paragraph(speech_3, speech_box_style)]], colWidths=[523])
    t_speech_3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAF5FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#8B5CF6")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_speech_3)

    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Top Viva Voce Questions & Answers for Member 3", h2_style))
    
    viva_m3 = [
        ("Q1: What is a Checked Exception versus an Unchecked Exception in Java?",
         "A checked exception is a subclass of java.lang.Exception (excluding RuntimeException). The Java compiler forces the programmer to handle it via a try-catch block or declare it via throws. An unchecked exception is a subclass of RuntimeException (like NullPointerException) which occurs at runtime and does not require compile-time checking. Our custom exceptions are checked to enforce safety rules at compile time."),
        ("Q2: Why is the Singleton constructor declared private?",
         "Declaring the constructor private prevents external classes from creating new instances using the 'new' keyword (e.g., new DatabaseManager() is illegal). The only way to access the class is through the controlled static method DatabaseManager.getInstance()."),
        ("Q3: Why is the getInstance() method synchronized?",
         "In a multithreaded application (such as Swing where UI events run on the EDT while background threads may execute), two threads calling getInstance() simultaneously could both see instance == null and instantiate two connections. The 'synchronized' keyword ensures thread safety by allowing only one thread to enter the method at a time."),
        ("Q4: How does PreparedStatement protect against SQL Injection?",
         "PreparedStatement precompiles the SQL command structure on the database engine. When values are passed via setString() or setDouble(), the database treats them strictly as literal parameter data, never as executable SQL code. Any malicious SQL characters (like ' OR '1'='1) are safely escaped."),
        ("Q5: What is the role of the InventoryOperations interface?",
         "InventoryOperations defines a contract for all inventory and distribution actions. FoodBankDAO implements this interface. This promotes loose coupling: if we later migrate from SQLite to MySQL or MongoDB, the GUI code remains 100% unchanged."),
        ("Q6: How does FoodBankDAO reconstitute polymorphic objects from SQLite?",
         "When reading the food_items table, the DAO inspects the item_type column. If 'PERISHABLE', it instantiates a PerishableItem; if 'PACKAGED', it instantiates a PackagedItem. It adds them to a Vector<FoodItem>, achieving clean polymorphic data retrieval.")
    ]
    for q, a in viva_m3:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 5: MEMBER 4 DETAILED GUIDE
    # =========================================================================
    story.append(Paragraph("5. Member 4: Swing GUI Architecture, Event Handling & Live Demo", h1_style))
    story.append(Paragraph("<b>Primary Role:</b> UI/UX Engineer & Live Systems Presenter &nbsp;|&nbsp; <b>Syllabus Focus:</b> Module 4", bold_body))
    story.append(Paragraph("<b>Assigned Files:</b> <code>src/ui/MainFrame.java</code>, <code>src/ui/InputPanel.java</code>, <code>src/ui/InventoryPanel.java</code>, <code>src/ui/ManagementPanel.java</code>, <code>src/ui/DistributionPanel.java</code>, <code>src/ui/AnalyticsPanel.java</code>", body_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#D97706"), spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("A. Deep Technical Concepts to Explain", h2_style))
    story.append(Paragraph("&bull; <b>Single-Window CardLayout Architecture (MainFrame.java):</b> Rather than popping up separate, disruptive <code>JFrame</code> windows (which clutter taskbars and cause memory leaks), <code>MainFrame</code> uses a <code>CardLayout</code>. All 5 application views reside inside one central container, smoothly swapping when navigation buttons are clicked.", bullet_style))
    story.append(Paragraph("&bull; <b>Delegation Event Model:</b> Visual controls (e.g., <code>JButton</code>) act as <b>Event Sources</b>. When clicked, they generate an <b><code>ActionEvent</code></b>. Registered <b>Event Listeners</b> implementing <code>ActionListener</code> capture the event in <code>actionPerformed(ActionEvent e)</code> and trigger business logic.", bullet_style))
    story.append(Paragraph("&bull; <b>Layout Managers in ChronoChef:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&bull; <code>BorderLayout</code>: Divides <code>MainFrame</code> into NORTH (Header & Navigation toolbar) and CENTER (CardLayout view area).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&bull; <code>FlowLayout</code>: Aligns navigation buttons horizontally with consistent spacing.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&bull; <code>GridLayout</code> & <code>GridBagLayout</code>: Aligns input form labels and text boxes in clean, structured columns.", bullet_style))
    story.append(Paragraph("&bull; <b>Walkthrough of the 5 Application Views:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <b>Input Panel:</b> Dynamic form that shows/hides cold-chain fields based on item type (Perishable vs Packaged).", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;2. <b>Inventory Panel:</b> Live urgency dashboard showing color-coded priority badges and sorting items via Bubble Sort.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;3. <b>Management Panel:</b> Real-time inventory search and stock adjustment controls.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;4. <b>Distribution Panel:</b> Subsidized checkout, live subsidy preview, ASCII receipt generation, and safety exception modal.", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;5. <b>Analytics Panel:</b> High-level KPIs (Total Stock, Expiring Stock, Waste Diverted) and historical distribution audit log.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("B. Step-by-Step Live Demonstration Script (Click-by-Click)", h2_style))
    demo_steps = [
        [Paragraph("<b>Step</b>", tbl_header), Paragraph("<b>Screen Action on Live Application</b>", tbl_header), Paragraph("<b>What to Say to Examiners</b>", tbl_header)],
        [
            Paragraph("<b>Step 1</b>", tbl_cell_bold),
            Paragraph("Navigate to <b>Add Food Item</b>.<br/>Select 'Perishable'. Enter <i>'Organic Whole Milk'</i>, Qty: 20, Expiry: <b>Today + 2 Days</b>. Click Save.", tbl_cell),
            Paragraph("\"Here I add fresh perishable milk. The GUI dynamically validates the input, and our DAO inserts it into SQLite using a PreparedStatement.\"", tbl_cell)
        ],
        [
            Paragraph("<b>Step 2</b>", tbl_cell_bold),
            Paragraph("Switch to <b>Priority Expiry Board</b>.<br/>Point to the top row showing the newly added milk.", tbl_cell),
            Paragraph("\"Notice our Bubble Sort immediately floated this milk to Row 1. It displays an <b>URGENT</b> badge and a PDI score of 96 because only 2 days remain.\"", tbl_cell)
        ],
        [
            Paragraph("<b>Step 3</b>", tbl_cell_bold),
            Paragraph("Switch to <b>Distribution & Checkout</b>.<br/>Select the Milk. Enter Recipient: <i>'St. Jude Shelter'</i>, Qty: 10. Click Checkout.", tbl_cell),
            Paragraph("\"Watch the dynamic subsidy in action: because D &le; 2, the subsidy is automatically 100%. The system prints an ASCII receipt with $0.00 total and deducts stock.\"", tbl_cell)
        ],
        [
            Paragraph("<b>Step 4</b>", tbl_cell_bold),
            Paragraph("Select an <b>Expired Item</b> (D < 0) from the dropdown and click 'Calculate / Distribute'.", tbl_cell),
            Paragraph("\"Here is our safety barrier in action: the system intercepts the expired item, throws our custom <b>ExpiredItemDistributionException</b>, and displays a red warning modal!\"", tbl_cell)
        ]
    ]
    t_demo = Table(demo_steps, colWidths=[45, 235, 243])
    t_demo.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D97706")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_demo)

    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Word-for-Word Speaking Script (3.0 Minutes)", h2_style))
    speech_4 = (
        "\"Respected evaluators, I will present our Swing Graphical User Interface and demonstrate our live application.<br/><br/>"
        "In <b>MainFrame.java</b>, we engineered a unified single-window interface utilizing <b>CardLayout</b>. "
        "Opening multiple JFrame windows creates desktop clutter and resource leaks; CardLayout allows all 5 views to live in "
        "a single window, switching instantaneously when toolbar buttons are clicked.<br/><br/>"
        "We utilized multiple layout managers: <b>BorderLayout</b> structures the frame, <b>FlowLayout</b> manages navigation tabs, "
        "and <b>GridLayout</b> structures our input forms. Every button click follows Java's <b>Delegation Event Model</b>, "
        "firing an <code>ActionEvent</code> processed by registered <code>ActionListener</code> callbacks.<br/><br/>"
        "Let me demonstrate our end-to-end workflow on the live system: [Execute Steps 1 to 4 above].<br/><br/>"
        "As demonstrated, ChronoChef is not just a database viewer; it is an intelligent, reactive decision-support system "
        "that eliminates food waste while maintaining uncompromised food safety. Our entire team is now ready for your viva questions.\""
    )
    t_speech_4 = Table([[Paragraph(speech_4, speech_box_style)]], colWidths=[523])
    t_speech_4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_speech_4)

    story.append(Spacer(1, 4))
    story.append(Paragraph("D. Top Viva Voce Questions & Answers for Member 4", h2_style))
    
    viva_m4 = [
        ("Q1: Why did you choose CardLayout over opening separate JFrame dialogs?",
         "Separate JFrames cause taskbar clutter, memory overhead, and synchronization bugs where one window has stale data. CardLayout maintains all views in a single persistent JFrame. When navigation occurs, mainFrame.refreshAllViews() cleanly syncs data across all panels from the single database connection."),
        ("Q2: How does the Delegation Event Model work in Java Swing?",
         "The Delegation Event Model separates the UI component generating an event (Event Source, like a JButton) from the object handling the event (Event Listener, implementing ActionListener). When the button is clicked, it generates an ActionEvent and invokes listener.actionPerformed(e)."),
        ("Q3: What Swing component was used for displaying tabular data, and how does it update?",
         "We used JTable backed by a DefaultTableModel. When data updates in SQLite, the DAO retrieves an updated Vector<FoodItem>, and the table model's data vector is replaced and notified via fireTableDataChanged(), repainting the view instantly."),
        ("Q4: How did you format the distribution receipt in DistributionPanel?",
         "We used a JTextArea styled with a monospaced font ('Courier New', Font.PLAIN, 12). Monospaced fonts guarantee that character widths are identical, allowing ASCII borders, item columns, quantities, and totals to align like a physical supermarket thermal receipt."),
        ("Q5: What is the Event Dispatch Thread (EDT)?",
         "The EDT is a dedicated single thread in Java Swing responsible for processing GUI events, painting components, and executing event listeners. All GUI creations and updates must execute on the EDT via SwingUtilities.invokeLater() to prevent race conditions.")
    ]
    for q, a in viva_m4:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 6: GROUP CROSS-DEFENSE & TRAP QUESTIONS
    # =========================================================================
    story.append(Paragraph("6. Group Cross-Defense & Common Examiner Trap Questions", h1_style))
    story.append(Paragraph(
        "Examiners frequently ask cross-cutting questions to test whether each team member understands the entire "
        "system rather than just their isolated topic. Below are the top group trap questions with complete model answers.",
        body_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#DC2626"), spaceBefore=4, spaceAfter=8))

    cross_q = [
        ("TRAP Q1: Trace the lifecycle of a single button click from GUI to Database and back.",
         "<b>Lifecycle Steps:</b><br/>"
         "1. <b>User Action (View - Member 4):</b> User clicks 'Confirm Distribution' in <code>DistributionPanel</code>.<br/>"
         "2. <b>Event Handling (Member 4):</b> <code>actionPerformed()</code> fires and invokes <code>validateAndPrepareRecord()</code>.<br/>"
         "3. <b>Domain Check (Model - Member 1):</b> The selected <code>FoodItem</code> is inspected for days remaining ($D$).<br/>"
         "4. <b>Safety Exception (Member 3):</b> If $D < 0$, <code>ExpiredItemDistributionException</code> is thrown and caught, halting execution.<br/>"
         "5. <b>Pricing Math (Member 2):</b> If D &ge; 0, <code>PriorityPricingService.calculateEffectivePrice()</code> computes dynamic subsidy.<br/>"
         "6. <b>Database Persistence (Member 3):</b> <code>FoodBankDAO.recordDistribution()</code> uses the Singleton <code>DatabaseManager</code> and a <code>PreparedStatement</code> to update stock in <code>food_items</code> and insert an audit row into <code>distributions</code>.<br/>"
         "7. <b>GUI Refresh (Member 4):</b> <code>mainFrame.refreshAllViews()</code> re-queries SQLite and triggers <code>fireTableDataChanged()</code> on all <code>JTable</code> views."),
        
        ("TRAP Q2: Why did you choose SQLite over MySQL or PostgreSQL for this project?",
         "<b>Answer:</b> SQLite is an embedded, serverless relational database engine stored as a single disk file (<code>chronochef.db</code>). Community food banks and disaster relief stations frequently operate in bandwidth-constrained or offline environments without dedicated IT administrators or local database servers. SQLite requires zero configuration, embeds cleanly via a standalone JAR, and guarantees ACID compliance with zero deployment friction."),

        ("TRAP Q3: What happens if two volunteers run ChronoChef simultaneously on the same machine?",
         "<b>Answer:</b> Because our <code>DatabaseManager</code> is implemented as a synchronized Singleton, all threads within the JVM share one synchronized connection pipeline. If two separate JVM processes attempt to open the SQLite file concurrently, SQLite's built-in file-locking mechanism serializes write transactions, preventing database corruption."),

        ("TRAP Q4: What are the primary limitations of the current implementation and future scope?",
         "<b>Answer:</b><br/>"
         "1. <i>Network Centralization:</i> Currently a standalone desktop app; future work could migrate to client-server architecture with REST APIs.<br/>"
         "2. <i>Hardware Integration:</i> Barcode and RFID scanner integration for automated expiry date capture upon donation intake.<br/>"
         "3. <i>Predictive Spoilage AI:</i> Incorporating humidity and environmental sensor data to adjust PDI dynamically for non-refrigerated goods."),

        ("TRAP Q5: How do you prove that your system is thoroughly tested and bug-free?",
         "<b>Answer:</b> ChronoChef includes an automated unit test suite (<code>ProjectTestRunner.java</code>) executing <b>35 comprehensive tests</b> across all modules. It validates OOP inheritance, polymorphism, Bubble Sort ordering, PDI boundary conditions (D < 0, D = 0, D > 30), custom exception throwing, and SQLite DAO CRUD operations, achieving a verified 100% pass rate.")
    ]

    for q, a in cross_q:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(a, viva_a_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Presentation Day Emergency Checklist", h2_style))
    chk_items = [
        "&check; <b>Compile & Run:</b> Execute <code>run.bat</code> or <code>compile.bat</code> prior to presentation to ensure zero build errors.",
        "&check; <b>Test Suite Proof:</b> Run <code>run_tests.bat</code> and show the console output: <code>[35 / 35 PASS - 100%]</code> if asked about testing.",
        "&check; <b>Sample Data Ready:</b> Ensure <code>chronochef.db</code> contains at least 1 Urgent item, 1 Expired item, 1 Perishable item, and 1 Packaged item for the demo.",
        "&check; <b>Time Discipline:</b> Keep each member's speech strictly between 2.5 and 3 minutes so the total presentation wraps up under 11 minutes."
    ]
    for chk in chk_items:
        story.append(Paragraph(chk, bullet_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ChronoChef_4_Member_Presentation_and_Viva_Guide.pdf")
    create_guide_pdf(target)
