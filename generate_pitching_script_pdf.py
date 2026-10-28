import os
import sys
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
            self.drawString(36, 810, "CHRONOCHEF: 4-MEMBER ORAL PITCH & PROFESSOR VIVA DEFENSE GUIDE")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(559, 810, "Course PBCST304 (OOP) — Full Presentation & Defense Script")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 804, 559, 804)

            # Footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 42, 559, 42)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 30, "Confidential Academic Reference — Java SE / Swing / SQLite Food Bank System")
            page_text = f"Page {self._pageNumber} of {total_pages}"
            self.drawRightString(559, 30, page_text)
        self.restoreState()


# =========================================================================
# MAIN PDF GENERATION
# =========================================================================
def build_pitch_script_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.2,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2.5
    )

    speech_box_style = ParagraphStyle(
        'SpeechBoxText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#1E293B")
    )

    viva_q_style = ParagraphStyle(
        'VivaQuestion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor("#991B1B"),
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    viva_a_style = ParagraphStyle(
        'VivaAnswer',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=colors.HexColor("#1F2937"),
        leftIndent=8,
        spaceAfter=4
    )

    tbl_header = ParagraphStyle(
        'TblHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, BANNER & SYSTEM / HARDWARE REQUIREMENTS
    # =========================================================================
    meta_data = [
        [
            Paragraph("<b>Project Title:</b> ChronoChef — Smart Dynamic Pricing & Expiry Tracker", tbl_cell_bold),
            Paragraph("<b>Academic Defense Target:</b> 4-Member Oral Presentation & Viva", tbl_cell)
        ],
        [
            Paragraph("<b>Course:</b> PBCST304 — Object-Oriented Programming (S3)", tbl_cell),
            Paragraph("<b>Tech Stack:</b> Java SE, Java Swing (MVC), JDBC, SQLite", tbl_cell)
        ],
        [
            Paragraph("<b>Verification Status:</b> 35/35 Test Suite Cases Passing (100% Verified)", tbl_cell),
            Paragraph("<b>Recommended Total Time:</b> 11-12 Minutes Total (~2.5m / Member)", tbl_cell)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[270, 253])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))

    story.append(Paragraph("CHRONOCHEF: 4-MEMBER PITCHING SCRIPT & VIVA DEFENSE GUIDE", title_style))
    story.append(Paragraph("A Complete Guide for Pitching to Your Java Professor — Architecture, System Specs, Spoken Scripts, Q&A & Codebase Reference", subtitle_style))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. System Architecture & Hardware Requirements (Project Prerequisite)", h1_style))
    story.append(Paragraph(
        "Member 1 introduces these specifications during the opening presentation to demonstrate that ChronoChef "
        "was engineered with an ultra-lightweight, zero-bloat footprint, enabling community food banks and relief shelters "
        "to run reliably on budget or donated hardware without external database server overhead.",
        body_style
    ))

    hw_data = [
        [
            Paragraph("<b>Component / Spec</b>", tbl_header),
            Paragraph("<b>Minimum Requirement</b>", tbl_header),
            Paragraph("<b>Recommended Specification</b>", tbl_header),
            Paragraph("<b>Engineering & Academic Rationale</b>", tbl_header)
        ],
        [
            Paragraph("<b>Processor (CPU)</b>", tbl_cell_bold),
            Paragraph("Intel Core i3 (4th Gen) / AMD Ryzen 3 / Dual-Core 2.0 GHz", tbl_cell),
            Paragraph("Intel Core i5 / AMD Ryzen 5 or higher", tbl_cell),
            Paragraph("Lightweight multithreading and event dispatching via the Swing Event Dispatch Thread (EDT).", tbl_cell)
        ],
        [
            Paragraph("<b>Memory (RAM)</b>", tbl_cell_bold),
            Paragraph("4 GB DDR3 / DDR4", tbl_cell),
            Paragraph("8 GB DDR4", tbl_cell),
            Paragraph("Minimal JVM heap allocation (~128MB to 256MB active memory under full operational load).", tbl_cell)
        ],
        [
            Paragraph("<b>Storage (Disk)</b>", tbl_cell_bold),
            Paragraph("250 MB free disk space", tbl_cell),
            Paragraph("500 MB SSD", tbl_cell),
            Paragraph("Zero-configuration embedded SQLite engine; entire relational schema is stored in one local file (<code>chronochef.db</code>).", tbl_cell)
        ],
        [
            Paragraph("<b>Operating System</b>", tbl_cell_bold),
            Paragraph("Windows 10/11, Ubuntu Linux 20.04+, macOS Catalina+", tbl_cell),
            Paragraph("Any 64-bit OS with Java support", tbl_cell),
            Paragraph("Cross-platform portability guaranteed by the Java Virtual Machine (WORA — <i>Write Once, Run Anywhere</i>).", tbl_cell)
        ],
        [
            Paragraph("<b>Java Runtime</b>", tbl_cell_bold),
            Paragraph("Java SE Runtime (JRE / JDK 11+)", tbl_cell),
            Paragraph("OpenJDK / Oracle JDK 17 (LTS)", tbl_cell),
            Paragraph("Standard library implementation using Java Swing, AWT, Event Delegation Model, and JDBC 4.2 API.", tbl_cell)
        ],
        [
            Paragraph("<b>Display Resolution</b>", tbl_cell_bold),
            Paragraph("1366 &times; 768 (HD)", tbl_cell),
            Paragraph("1920 &times; 1080 (Full HD)", tbl_cell),
            Paragraph("Responsive single-window <code>CardLayout</code> dynamically adjusts layout panels without visual truncation.", tbl_cell)
        ]
    ]

    t_hw = Table(hw_data, colWidths=[90, 125, 120, 188])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Key Engineering Advantages for Academic Defense:", h2_style))
    adv_points = [
        "<b>Zero Server Dependencies:</b> Unlike web applications that require external MySQL/PostgreSQL servers and HTTP web servers, ChronoChef is fully self-contained.",
        "<b>100% Offline Resilience:</b> Operates without internet connectivity, making it ideal for disaster zones and food distribution camps.",
        "<b>Sub-Millisecond Query Response:</b> In-process JDBC queries execute instantaneously with zero network latency overhead."
    ]
    for pt in adv_points:
        story.append(Paragraph(f"• {pt}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TEAM ALLOCATION, VERBAL HANDOFFS & PITCH STRATEGY
    # =========================================================================
    story.append(Paragraph("2. Master 4-Member Allocation, Transitions & Pitching Strategy", h1_style))
    story.append(Paragraph(
        "Each member has a designated technical focus mapped directly to the OOP syllabus (Modules 1 to 4). "
        "The presentation avoids line-by-line syntax recitation and instead emphasizes <b>architecture, design patterns, "
        "mathematical modeling, and live execution</b>.",
        body_style
    ))

    alloc_data = [
        [
            Paragraph("<b>Member</b>", tbl_header),
            Paragraph("<b>Designated Role & Focus</b>", tbl_header),
            Paragraph("<b>Syllabus</b>", tbl_header),
            Paragraph("<b>Key Source Files</b>", tbl_header),
            Paragraph("<b>Time</b>", tbl_header)
        ],
        [
            Paragraph("<b>Member 1</b>", tbl_cell_bold),
            Paragraph("<b>System Specs, Problem Motivation & Core OOP</b><br/>Hardware needs, Encapsulation, Hierarchical Inheritance, Dynamic Method Dispatch.", tbl_cell),
            Paragraph("Mod 1 &<br/>Mod 2", tbl_cell),
            Paragraph("<code>model/FoodItem.java</code><br/><code>model/PerishableItem.java</code><br/><code>model/PackagedItem.java</code>", tbl_cell),
            Paragraph("2.5 min", tbl_cell)
        ],
        [
            Paragraph("<b>Member 2</b>", tbl_cell_bold),
            Paragraph("<b>Mathematics, Urgency Formulas & Sorting Algorithms</b><br/>Days Remaining, Priority Distribution Index (PDI), Dynamic Subsidies, Bubble Sort.", tbl_cell),
            Paragraph("Mod 1 &<br/>Mod 3", tbl_cell),
            Paragraph("<code>service/PriorityPricingService.java</code><br/><code>model/DistributionRecord.java</code>", tbl_cell),
            Paragraph("2.5 min", tbl_cell)
        ],
        [
            Paragraph("<b>Member 3</b>", tbl_cell_bold),
            Paragraph("<b>Persistence, Design Patterns & Food Safety Exceptions</b><br/>Singleton pattern, DAO pattern, PreparedStatement security, Custom Checked Exceptions.", tbl_cell),
            Paragraph("Mod 3 &<br/>Mod 4", tbl_cell),
            Paragraph("<code>database/DatabaseManager.java</code><br/><code>database/FoodBankDAO.java</code><br/><code>exception/*.java</code>", tbl_cell),
            Paragraph("2.5 min", tbl_cell)
        ],
        [
            Paragraph("<b>Member 4</b>", tbl_cell_bold),
            Paragraph("<b>Swing GUI Architecture, Live Demo & Social Impact</b><br/>CardLayout, Event Delegation Model, 5 modules live checkout, automated test proof.", tbl_cell),
            Paragraph("Mod 4", tbl_cell),
            Paragraph("<code>ui/MainFrame.java</code><br/><code>ui/InventoryPanel.java</code><br/><code>ui/DistributionPanel.java</code>", tbl_cell),
            Paragraph("3.0 min", tbl_cell)
        ]
    ]

    t_alloc = Table(alloc_data, colWidths=[55, 175, 55, 185, 53])
    t_alloc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F766E")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_alloc)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Verbal Handoff Transitions (Memorize These Cue Lines)", h2_style))
    handoff_data = [
        [
            Paragraph("<b>Transition</b>", tbl_header),
            Paragraph("<b>Exact Spoken Handoff Cue to Recite</b>", tbl_header)
        ],
        [
            Paragraph("<b>Member 1 &rarr; Member 2</b>", tbl_cell_bold),
            Paragraph("<i>\"Now that we have seen how our Object-Oriented domain entities represent the real world, my teammate [Member 2] will explain the mathematical algorithms and pricing rules that drive our inventory urgency.\"</i>", tbl_cell)
        ],
        [
            Paragraph("<b>Member 2 &rarr; Member 3</b>", tbl_cell_bold),
            Paragraph("<i>\"Having explored our algorithm and pricing logic, my teammate [Member 3] will now discuss how this data is securely stored in SQLite and protected by custom exceptions.\"</i>", tbl_cell)
        ],
        [
            Paragraph("<b>Member 3 &rarr; Member 4</b>", tbl_cell_bold),
            Paragraph("<i>\"Now, my teammate [Member 4] will take you through our Swing graphical user interface and demonstrate the live running application.\"</i>", tbl_cell)
        ],
        [
            Paragraph("<b>Member 4 &rarr; Professor</b>", tbl_cell_bold),
            Paragraph("<i>\"We have verified all 35 project test assertions with a 100% pass rate. Our team is now ready for your questions. Thank you!\"</i>", tbl_cell)
        ]
    ]
    t_handoff = Table(handoff_data, colWidths=[110, 413])
    t_handoff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_handoff)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Presentation Rules of Engagement (How to Score Maximum Marks)", h2_style))
    rules = [
        "<b>No Line-by-Line Code Reading:</b> Explain <i>what</i> the system accomplishes and <i>which OOP principle</i> makes it possible. Professors deduct marks for reading syntax.",
        "<b>Maintain Eye Contact:</b> Speak directly to your professor while making gestures toward the slide or application.",
        "<b>Strict Time Discipline:</b> Never exceed 3 minutes per member so the evaluator has ample time to conduct the viva defense."
    ]
    for r in rules:
        story.append(Paragraph(f"• {r}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: MEMBER 1 PITCH & VIVA
    # =========================================================================
    story.append(Paragraph("3. Member 1: Problem Motivation, System Specs & Core OOP Modeling", h1_style))
    story.append(Paragraph("<b>Assigned Files:</b> <code>Main.java</code>, <code>model/FoodItem.java</code>, <code>model/PerishableItem.java</code>, <code>model/PackagedItem.java</code> | <b>Time:</b> 0:00 – 2:30", h3_style))
    story.append(Spacer(1, 4))

    m1_speech = (
        "\"Respected Professor and evaluators, good morning. Today, our team is presenting <b>ChronoChef</b> — "
        "an intelligent desktop food inventory and dynamic subsidy management system developed in Java.<br/><br/>"
        "To understand why we built ChronoChef, let us look at the operational reality of charitable food banks. "
        "Food banks handle massive volumes of donated groceries with varying expiration dates. Tragically, over "
        "<b>30% of donated perishable inventory spoils on warehouse shelves</b> before it can reach needy families. "
        "The reasons are static paper logs, lack of urgency-based subsidies, and the human risk of distributing expired stock.<br/><br/>"
        "ChronoChef eliminates this waste. It autonomously computes remaining shelf-life, assigns a real-time urgency score, "
        "subsidizes near-expiry food up to 100% free distribution, and strictly blocks expired goods from being handed out.<br/><br/>"
        "Before looking at the code structure, I want to emphasize the <b>System Requirements</b>. Because relief shelters operate on "
        "budget or donated machines, we engineered ChronoChef with an ultra-lightweight footprint:<br/>"
        "• On hardware: It runs smoothly on an entry-level <b>Intel Core i3 or AMD Ryzen 3 CPU with just 4 GB of RAM</b> and under 250 MB disk space.<br/>"
        "• On software: It requires <b>Java SE 11 or higher</b> and uses an embedded zero-configuration database, making it 100% offline-ready.<br/><br/>"
        "In our core data tier, we strictly implemented <b>Key Object-Oriented Principles</b>:<br/>"
        "1. <b>Encapsulation:</b> Our base entity, <code>FoodItem</code>, strictly protects internal state with private attributes and public getters and setters.<br/>"
        "2. <b>Hierarchical Inheritance:</b> Food categories have distinct real-world physical properties. Therefore, <code>FoodItem</code> is extended by two specialized subclasses: "
        "<code>PerishableItem</code> — which encapsulates cold-chain storage temperatures — and <code>PackagedItem</code>, which tracks manufacturer batch lot numbers.<br/>"
        "3. <b>Dynamic Method Dispatch:</b> Each subclass overrides the polymorphic <code>getStorageInstructions()</code> method. At runtime, the JVM dynamically resolves whether to return chilled refrigeration instructions or dry pantry instructions based on the actual object instance.<br/><br/>"
        "<i>Now that we have seen how our Object-Oriented domain entities represent the real world, my teammate [Member 2] will explain the mathematical algorithms and pricing rules that drive our inventory urgency.</i>\""
    )

    t_m1_speech = Table([[Paragraph(m1_speech, speech_box_style)]], colWidths=[523])
    t_m1_speech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_m1_speech)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Professor Viva Questions & Model Answers for Member 1", h2_style))
    m1_qa = [
        ("Q1: Why did you use inheritance instead of simply putting an 'isPerishable' boolean flag inside FoodItem?",
         "Putting a flag inside <code>FoodItem</code> violates the Single Responsibility Principle and causes code pollution with messy <code>if-else</code> checks whenever storage behavior or attributes differ. By using Hierarchical Inheritance, <code>PerishableItem</code> and <code>PackagedItem</code> maintain their own distinct attributes (such as <code>optimumTempCelsius</code> vs <code>batchNumber</code>) and cleanly override behavior through polymorphism."),
        
        ("Q2: How does the Java Virtual Machine (JVM) resolve Dynamic Method Dispatch in your code?",
         "When <code>getStorageInstructions()</code> is called on a <code>FoodItem</code> reference, Java verifies at compile time that the method exists in the superclass interface. At runtime, however, the JVM inspects the object's virtual method table (vtable) and dispatches the call directly to the overriding method of the actual runtime subclass instance."),
        
        ("Q3: Why build a standalone Java desktop application instead of a web app for this use case?",
         "Food banks, disaster relief camps, and emergency shelters often operate in areas with unstable or non-existent internet connectivity. A Java Swing desktop app with an embedded SQLite database guarantees 100% offline functionality, instantaneous sub-millisecond response times, and zero server hosting expenses.")
    ]
    for q, a in m1_qa:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: MEMBER 2 PITCH & VIVA
    # =========================================================================
    story.append(Paragraph("4. Member 2: Mathematical Logic, Urgency Formulas & Sorting Algorithms", h1_style))
    story.append(Paragraph("<b>Assigned Files:</b> <code>service/PriorityPricingService.java</code>, <code>model/DistributionRecord.java</code> | <b>Time:</b> 2:30 – 5:00", h3_style))
    story.append(Spacer(1, 4))

    m2_speech = (
        "\"Thank you, [Member 1]. Good morning, Professor. I will explain the mathematical logic, automated decision formulas, "
        "and sorting algorithms that power ChronoChef.<br/><br/>"
        "In a food bank, inventory cannot be treated as a simple First-In, First-Out queue. Fresh milk received today that expires in 2 days "
        "must be prioritized far ahead of canned beans received a month ago that expire next year. To solve this, we formulated the "
        "<b>Priority Distribution Index (PDI)</b>.<br/><br/>"
        "Our engine evaluates two primary mathematical formulas:<br/>"
        "1. <b>Days Remaining Calculation (D):</b> We compute the delta between the expiry timestamp and the current system timestamp converted to days:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>Days Remaining (D) = (ExpiryDate_ms - CurrentDate_ms) / (1000 * 60 * 60 * 24)</code><br/>"
        "If D is negative, the item is mathematically flagged as expired.<br/><br/>"
        "2. <b>Priority Distribution Index (PDI Score):</b> For non-expired items, we map shelf life into a normalized 1-to-100 urgency score using:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<code>PDI = max(1, 100 - (D * 2))</code><br/>"
        "• If an item has <b>5 days or fewer</b>, its PDI reaches <b>90 to 100</b>, classifying it as <b>URGENT</b>.<br/>"
        "• 6 to 15 days maps to <b>HIGH</b> priority.<br/>"
        "• 16 to 30 days maps to <b>MEDIUM</b> priority.<br/>"
        "• Anything over 30 days is categorized as <b>LOW</b> priority.<br/><br/>"
        "3. <b>Dynamic Rule-Based Subsidies:</b> To incentivize community shelters to clear stock before it spoils, our pricing engine applies automatic subsidies:<br/>"
        "• Items within <b>2 days of expiry</b> receive a <b>100% Subsidy (distributed completely FREE - ₹0.00)</b>.<br/>"
        "• Items within <b>3 to 7 days</b> receive a <b>50% Subsidy</b>.<br/>"
        "• Items beyond 7 days remain at their standard base price.<br/><br/>"
        "4. <b>Algorithm & Sorting:</b> To display inventory strictly by urgency, our service implements an in-memory <b>Bubble Sort algorithm</b> "
        "directly on a <code>Vector&lt;FoodItem&gt;</code>. It iterates through adjacent items and sorts them in descending order of their PDI scores. "
        "Because a local shelter manages around 500 to 1,000 active inventory items, this classic O(n²) sorting technique completes in just a few milliseconds "
        "on 4 GB RAM while perfectly demonstrating textbook data structure manipulation.<br/><br/>"
        "<i>Having explored our algorithm and pricing logic, my teammate [Member 3] will now discuss how this data is securely stored in SQLite and protected by custom exceptions.</i>\""
    )

    t_m2_speech = Table([[Paragraph(m2_speech, speech_box_style)]], colWidths=[523])
    t_m2_speech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_m2_speech)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Professor Viva Questions & Model Answers for Member 2", h2_style))
    m2_qa = [
        ("Q1: Why did you use Bubble Sort instead of built-in Collections.sort() or Arrays.sort()?",
         "While <code>Collections.sort()</code> implements TimSort with O(n log n) efficiency, we intentionally implemented the classic Bubble Sort algorithm to demonstrate fundamental computer science sorting mechanics directly on Java Collections (<code>Vector</code>), aligning with university course guidelines. For standard food bank batch sizes of under 1,000 items, execution time is negligible."),
        
        ("Q2: What happens mathematically when an item's expiration date has already passed (D < 0)?",
         "When D < 0, <code>calculatePdiScore()</code> short-circuits and immediately returns <code>0</code>, tagging the item with the <code>EXPIRED</code> enum. This acts as an automated quarantine flag that prevents the item from entering the subsidy calculation or distribution pipelines."),
        
        ("Q3: Could an operator tamper with the system clock to manipulate PDI scores?",
         "While the formula evaluates against system time, date integrity is strictly validated upon donation intake via ISO <code>YYYY-MM-DD</code> regular expression patterns and calendar bounds, preventing corrupted timestamps from entering the system.")
    ]
    for q, a in m2_qa:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: MEMBER 3 PITCH & VIVA
    # =========================================================================
    story.append(Paragraph("5. Member 3: Persistence Layer, Design Patterns & Food Safety Exceptions", h1_style))
    story.append(Paragraph("<b>Assigned Files:</b> <code>database/DatabaseManager.java</code>, <code>database/FoodBankDAO.java</code>, <code>model/InventoryOperations.java</code>, <code>exception/*.java</code> | <b>Time:</b> 5:00 – 7:30", h3_style))
    story.append(Spacer(1, 4))

    m3_speech = (
        "\"Thank you, [Member 2]. Good morning, Professor. I will present our persistence tier, software design patterns, "
        "and our robust food safety exception handling mechanism.<br/><br/>"
        "For data persistence, ChronoChef utilizes <b>JDBC with SQLite</b>. We chose an embedded SQLite database because it creates a "
        "portable, self-contained database file (<code>chronochef.db</code>) stored directly in the project directory, eliminating the need "
        "for external database servers or complex network configurations.<br/><br/>"
        "To manage database operations cleanly, we incorporated two proven software design patterns:<br/>"
        "1. <b>Singleton Pattern:</b> Opening database connections is computationally expensive and uncontrolled connections can lock SQLite database files. "
        "In <code>DatabaseManager.java</code>, we implemented a private constructor and a <code>static synchronized getInstance()</code> method. "
        "This guarantees that exactly one connection pipeline exists throughout the entire JVM lifecycle.<br/>"
        "2. <b>Data Access Object (DAO) Pattern:</b> We decoupled the database from the user interface by defining an interface: <code>InventoryOperations</code>. "
        "Our DAO class, <code>FoodBankDAO</code>, implements this contract to handle all CRUD queries, category filtering, and transaction logging.<br/>"
        "3. <b>SQL Injection Prevention:</b> We strictly avoided raw string concatenation in SQL queries. Every single database query uses parameterized "
        "<code>PreparedStatement</code> objects. The SQL structure is pre-compiled by the database engine and user inputs are bound strictly as data literals, "
        "neutralizing SQL injection attacks.<br/><br/>"
        "Next, I want to emphasize <b>Food Safety & Custom Exceptions</b>:<br/>"
        "• In a commercial grocery store, an expired sale is a financial error; in a food bank distributing to vulnerable shelters, giving out expired food is a hazardous safety violation.<br/>"
        "• To enforce safety at the compiler level, we created two custom checked exceptions:<br/>"
        "&nbsp;&nbsp;• <code>ExpiredItemDistributionException</code>: Thrown if an operator attempts to distribute an item with D &lt; 0.<br/>"
        "&nbsp;&nbsp;• <code>InvalidQuantityException</code>: Thrown if an operator attempts to dispatch more stock than physically exists in warehouse inventory.<br/>"
        "• Because these are <b>checked exceptions</b> inheriting directly from <code>java.lang.Exception</code>, the Java compiler enforces strict <code>try-catch</code> handling. "
        "The distribution transaction cannot execute without explicit exception handling, safety rollback, and operator alerts.<br/><br/>"
        "<i>Now, my teammate [Member 4] will take you through our Swing graphical user interface and demonstrate the live running application.</i>\""
    )

    t_m3_speech = Table([[Paragraph(m3_speech, speech_box_style)]], colWidths=[523])
    t_m3_speech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_m3_speech)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Professor Viva Questions & Model Answers for Member 3", h2_style))
    m3_qa = [
        ("Q1: Why did you implement DatabaseManager as a Singleton instead of opening a 'new Connection()' in every DAO method?",
         "Creating connections on every query creates massive CPU and memory overhead due to repeated file descriptor handshakes. Furthermore, SQLite is an embedded file database; concurrent unmanaged connections can lead to <code>SQLITE_BUSY</code> file locking errors. The Singleton pattern guarantees centralized connection lifecycle management and controlled access."),
        
        ("Q2: Why make ExpiredItemDistributionException a checked exception instead of an unchecked RuntimeException?",
         "Checked exceptions enforce <b>compile-time safety</b>. An unchecked <code>RuntimeException</code> can be overlooked by a developer and crash the app during production. By making it checked, the compiler forces the UI controller to wrap distribution calls in a <code>try-catch</code> block, ensuring safety alerts and rollbacks are always executed."),
        
        ("Q3: How do you prevent JDBC connection leaks and cursor exhaustion?",
         "Every database operation uses Java's <b>try-with-resources</b> or explicit <code>finally</code> blocks to close all <code>ResultSet</code> and <code>PreparedStatement</code> objects immediately after execution, releasing OS file handles even if an unexpected SQL error occurs.")
    ]
    for q, a in m3_qa:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MEMBER 4 PITCH & VIVA
    # =========================================================================
    story.append(Paragraph("6. Member 4: Swing GUI Architecture, Live Demo & Social Impact", h1_style))
    story.append(Paragraph("<b>Assigned Files:</b> <code>ui/MainFrame.java</code>, <code>ui/InputPanel.java</code>, <code>ui/InventoryPanel.java</code>, <code>ui/ManagementPanel.java</code>, <code>ui/DistributionPanel.java</code> | <b>Time:</b> 7:30 – 10:30", h3_style))
    story.append(Spacer(1, 4))

    m4_speech = (
        "\"Thank you, [Member 3]. Good morning, Professor. I will present our Swing UI architecture and walk you through the live application.<br/><br/>"
        "When designing the graphical user interface, our objective was to build a clean, modern, and reliable dashboard using "
        "<b>pure Java Swing and AWT</b>, strictly complying with the college syllabus.<br/><br/>"
        "Our UI architecture is grounded in three core design decisions:<br/>"
        "1. <b>Single-Window CardLayout Pattern:</b> Instead of opening multiple messy pop-up windows (<code>JFrame</code>s) that clutter the desktop, "
        "we host all 5 system views inside a single <code>MainFrame</code> using <code>CardLayout</code>. A top navigation bar switches between panels with zero screen flicker.<br/>"
        "2. <b>Delegation Event Model:</b> We cleanly decouple UI components from backend logic. Buttons register <code>ActionListener</code> instances "
        "that capture <code>ActionEvent</code>s and delegate execution to service methods.<br/>"
        "3. <b>Layout Hierarchy:</b> We combined nested layout managers — <code>BorderLayout</code> for main frames, <code>GridLayout</code> for structured forms, "
        "and <code>FlowLayout</code> for toolbars — ensuring consistent rendering across screen resolutions.<br/><br/>"
        "<i>(Member 4 now transitions to the live demo screen)</i><br/><br/>"
        "Allow me to demonstrate the <b>5 Core Modules</b> in action:<br/>"
        "• <b>Module 1 — Data Input Panel:</b> Here we register incoming food donations. Form validation prevents blank fields, negative numbers, and malformed dates.<br/>"
        "• <b>Module 2 — Live Inventory & Expiry Tracker:</b> This table renders live stock with color-coded urgency badges — <b>Red for Urgent</b>, <b>Orange for High</b>, and <b>Green for Medium</b>. "
        "Clicking 'Sort by PDI' triggers our Bubble Sort algorithm, instantly bubbling urgent perishable goods to the top of the operator's view.<br/>"
        "• <b>Module 3 — Management Panel:</b> Allows staff to select existing stock, restock new shipments, or write off damaged goods.<br/>"
        "• <b>Module 4 — Distribution & Subsidy Billing:</b> This is our checkout station. When we select near-expiry Milk (2 days remaining) and dispatch it to a shelter, "
        "watch the system automatically apply a <b>100% Zero-Waste Subsidy (Total: ₹0.00)</b>, deduct stock safely in SQLite, and generate an itemized text receipt.<br/>"
        "Now watch what happens if we attempt to distribute an expired item: the system intercepts the action, throws our <code>ExpiredItemDistributionException</code>, "
        "and displays a red safety modal, strictly blocking the checkout.<br/>"
        "• <b>Module 5 — Analytics & Social Impact:</b> Displays 6 aggregated metrics: Total Inventory Count, Urgent Items Count, Total Food Waste Prevented in Kilograms, "
        "and Total Community Subsidies Granted.<br/><br/>"
        "In summary, ChronoChef combines <b>core Object-Oriented principles, deterministic mathematical algorithms, secure database design, and an intuitive Swing interface</b> "
        "to solve a critical real-world problem: ending food waste and hunger in our communities.<br/><br/>"
        "Our automated test suite has verified all 35 project test assertions with a 100% pass rate. We are now ready for your questions. Thank you!\""
    )

    t_m4_speech = Table([[Paragraph(m4_speech, speech_box_style)]], colWidths=[523])
    t_m4_speech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FDF2F8")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F472B6")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_m4_speech)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Professor Viva Questions & Model Answers for Member 4", h2_style))
    m4_qa = [
        ("Q1: Why did you use CardLayout instead of opening multiple JFrames or using JTabbedPane?",
         "Opening multiple <code>JFrame</code> windows causes desktop clutter and consumes extra OS window handles. While <code>JTabbedPane</code> works, <code>CardLayout</code> paired with a custom navigation toolbar gives us full programmatic control over view transitions, lazy loading, and automatic table re-queries whenever a panel is brought to the front."),
        
        ("Q2: What thread does Swing use to paint components and handle button clicks?",
         "Swing components are not thread-safe and must be manipulated strictly on the <b>Event Dispatch Thread (EDT)</b>. In our <code>Main.java</code>, we launch the interface using <code>SwingUtilities.invokeLater(() -&gt; { ... })</code> to ensure the GUI is initialized on the EDT, preventing deadlocks and race conditions."),
        
        ("Q3: How does InventoryPanel update its table when a new item is added in InputPanel?",
         "When an item is added, the DAO saves the record in SQLite. When the user navigates to the Inventory view, our transition listener triggers <code>refreshTableData()</code>, which re-queries the DAO, clears the <code>DefaultTableModel</code> vector, repopulates rows, and calls <code>fireTableDataChanged()</code> to re-render the table with fresh PDI urgency badges.")
    ]
    for q, a in m4_qa:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: EXAMINER CROSS-DEFENSE TRAP QUESTIONS & EMERGENCY CHECKLIST
    # =========================================================================
    story.append(Paragraph("7. Examiner Cross-Defense & Trap Questions", h1_style))
    story.append(Paragraph(
        "Professors frequently ask cross-cutting questions to test whether every team member understands how the entire "
        "system connects together. Below are the top cross-defense questions with complete model answers.",
        body_style
    ))

    trap_qa = [
        ("TRAP Q1: Trace the lifecycle of a single button click from GUI to Database and back.",
         "1. <b>User Action (View - Member 4):</b> Operator clicks 'Confirm Distribution' in <code>DistributionPanel</code>.<br/>"
         "2. <b>Event Handling (Member 4):</b> <code>actionPerformed()</code> fires and validates user input fields.<br/>"
         "3. <b>Domain Check (Model - Member 1):</b> The selected <code>FoodItem</code> is checked for days remaining (D).<br/>"
         "4. <b>Safety Exception (Member 3):</b> If D &lt; 0, <code>ExpiredItemDistributionException</code> is thrown and caught, stopping the transaction.<br/>"
         "5. <b>Pricing Math (Member 2):</b> If D &ge; 0, <code>PriorityPricingService</code> calculates dynamic subsidy.<br/>"
         "6. <b>Persistence (Member 3):</b> <code>FoodBankDAO</code> uses the Singleton <code>DatabaseManager</code> and a <code>PreparedStatement</code> to update stock in <code>food_items</code> and log a row in <code>distributions</code>.<br/>"
         "7. <b>GUI Refresh (Member 4):</b> <code>mainFrame.refreshAllViews()</code> re-queries SQLite and triggers <code>fireTableDataChanged()</code> across all tables."),
        
        ("TRAP Q2: Why did you choose SQLite over MySQL or PostgreSQL for this project?",
         "SQLite is an embedded, serverless relational database engine stored as a single disk file (<code>chronochef.db</code>). Community food banks and relief shelters often operate in bandwidth-constrained or offline environments without dedicated IT staff or database servers. SQLite requires zero configuration, embeds cleanly via a standalone JAR, and guarantees full ACID compliance with zero deployment overhead."),

        ("TRAP Q3: What happens if two volunteers run ChronoChef simultaneously on the same machine?",
         "Because our <code>DatabaseManager</code> is implemented as a synchronized Singleton, all threads within the JVM share one synchronized connection pipeline. If two separate JVM processes attempt to write to the SQLite file concurrently, SQLite's built-in file-locking mechanism serializes write transactions, preventing database corruption."),

        ("TRAP Q4: How do you prove that your system is thoroughly tested and bug-free?",
         "ChronoChef includes an automated unit test suite (<code>ProjectTestRunner.java</code>) executing <b>35 comprehensive tests</b> across all modules. It validates OOP inheritance, polymorphism, Bubble Sort ordering, PDI boundary conditions (D &lt; 0, D = 0, D &gt; 30), custom exception throwing, and SQLite DAO CRUD operations, achieving a verified 100% pass rate.")
    ]

    for q, a in trap_qa:
        story.append(Paragraph(q, viva_q_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", viva_a_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))
    story.append(Paragraph("Presentation Day Emergency Checklist", h2_style))
    chk_items = [
        "&check; <b>Compile & Run:</b> Double-click <code>run.bat</code> or <code>compile.bat</code> prior to presentation to ensure zero build errors.",
        "&check; <b>Automated Test Proof:</b> Run <code>run_tests.bat</code> and show the console output: <code>[35 / 35 PASS - 100%]</code> if asked about testing.",
        "&check; <b>Sample Data Ready:</b> Ensure <code>chronochef.db</code> contains at least 1 Urgent item, 1 Expired item, 1 Perishable item, and 1 Packaged item for the demo.",
        "&check; <b>Time Discipline:</b> Keep each member's speech strictly between 2.5 and 3 minutes so the total presentation wraps up under 11 minutes."
    ]
    for chk in chk_items:
        story.append(Paragraph(chk, bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SECTION 8 - PROJECT DIRECTORY STRUCTURE & FOLDER ANATOMY
    # =========================================================================
    story.append(Paragraph("8. Project Directory Structure & Folder Anatomy", h1_style))
    story.append(Paragraph(
        "A rigorous explanation of every folder in the project workspace, distinguishing between build outputs, "
        "runtime libraries, persistent database stores, and source package structures.",
        body_style
    ))

    folder_data = [
        [
            Paragraph("<b>Folder / Directory Path</b>", tbl_header),
            Paragraph("<b>Category / Type</b>", tbl_header),
            Paragraph("<b>Architectural Role & Contents</b>", tbl_header)
        ],
        [
            Paragraph("<code>project code/</code>", tbl_cell_bold),
            Paragraph("Root Container", tbl_cell),
            Paragraph("Top-level directory housing the complete executable project, batch scripts, and local database file.", tbl_cell)
        ],
        [
            Paragraph("<code>project code/src/</code>", tbl_cell_bold),
            Paragraph("Source Root", tbl_cell),
            Paragraph("Root directory for all uncompiled Java source files (<code>.java</code>), organized into modular, domain-driven package namespaces.", tbl_cell)
        ],
        [
            Paragraph("<code>project code/bin/</code>", tbl_cell_bold),
            Paragraph("Build Artifacts", tbl_cell),
            Paragraph("Destination folder where the Java compiler (<code>javac</code>) outputs compiled bytecode (<code>.class</code> files), preserving package structures.", tbl_cell)
        ],
        [
            Paragraph("<code>project code/lib/</code>", tbl_cell_bold),
            Paragraph("External Dependencies", tbl_cell),
            Paragraph("Contains external runtime JAR archives: <code>sqlite-jdbc-3.45.2.0.jar</code> (embedded SQLite driver) and SLF4J logging bridge.", tbl_cell)
        ],
        [
            Paragraph("<code>src/database/</code>", tbl_cell_bold),
            Paragraph("Persistence Package", tbl_cell),
            Paragraph("Handles low-level JDBC database connections, connection pooling via Singleton, data access objects (DAO), and automated mock data seeders.", tbl_cell)
        ],
        [
            Paragraph("<code>src/model/</code>", tbl_cell_bold),
            Paragraph("Domain Entity Package", tbl_cell),
            Paragraph("Houses core OOP data models (<code>FoodItem</code>, <code>PerishableItem</code>, <code>PackagedItem</code>, <code>DistributionRecord</code>) and interface contracts.", tbl_cell)
        ],
        [
            Paragraph("<code>src/service/</code>", tbl_cell_bold),
            Paragraph("Business Logic Package", tbl_cell),
            Paragraph("Contains algorithmic evaluation engines: Days Remaining calculations, Priority Distribution Index (PDI), dynamic subsidy tiers, and Bubble Sort.", tbl_cell)
        ],
        [
            Paragraph("<code>src/exception/</code>", tbl_cell_bold),
            Paragraph("Custom Exception Package", tbl_cell),
            Paragraph("Defines custom checked exceptions (<code>ExpiredItemDistributionException</code>, <code>InvalidQuantityException</code>) enforcing compile-time safety.", tbl_cell)
        ],
        [
            Paragraph("<code>src/ui/</code>", tbl_cell_bold),
            Paragraph("Presentation GUI Package", tbl_cell),
            Paragraph("Hosts all Java Swing views, custom cards, navigation toolbars, table renderers, and event listeners built with pure Swing and AWT.", tbl_cell)
        ],
        [
            Paragraph("<code>src/test/</code>", tbl_cell_bold),
            Paragraph("Verification Package", tbl_cell),
            Paragraph("Automated test harness executing 35 unit assertions and diagnostic UI capture tools verifying 100% codebase correctness.", tbl_cell)
        ]
    ]

    t_folder = Table(folder_data, colWidths=[120, 95, 308])
    t_folder.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_folder)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Root Batch Launcher Scripts:", h2_style))
    batch_data = [
        ("compile.bat", "Invokes <code>javac</code> with the classpath set to <code>lib/*</code>, compiling all 20 source files from <code>src/</code> into <code>bin/</code>."),
        ("run.bat", "Executes the compiled application entry point <code>Main</code> using <code>java -cp \"bin;lib/*\" Main</code>."),
        ("run_tests.bat", "Runs the automated test suite <code>ProjectTestRunner</code>, executing 35 unit assertions with console pass/fail summaries.")
    ]
    for b_name, b_desc in batch_data:
        story.append(Paragraph(f"• <b><code>{b_name}</code>:</b> {b_desc}", bullet_style))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SECTION 9 - CLASS REFERENCE PART 1 (CORE, MODEL, DATABASE, SERVICE)
    # =========================================================================
    story.append(Paragraph("9. Complete Class Reference Guide (Part 1: Core, Model, DB & Service)", h1_style))
    story.append(Paragraph(
        "A definitive explanation of every class in each project package, detailing its specific technical role, "
        "OOP mechanism, and practical use in ChronoChef.",
        body_style
    ))

    cls_data_1 = [
        [
            Paragraph("<b>Package / Class</b>", tbl_header),
            Paragraph("<b>Type & Inheritance</b>", tbl_header),
            Paragraph("<b>Technical Role, Purpose & Practical Use</b>", tbl_header)
        ],
        [
            Paragraph("<code>Main.java</code><br/><i>(Root Package)</i>", tbl_cell_bold),
            Paragraph("Entry Point Class", tbl_cell),
            Paragraph("<b>Bootstrap Coordinator:</b> Initial entry point of ChronoChef. Invokes database initialization, verifies table schemas, runs <code>DataSeeder</code> if records are empty, and initializes <code>MainFrame</code> strictly on the Swing Event Dispatch Thread (EDT) using <code>SwingUtilities.invokeLater()</code>.", tbl_cell)
        ],
        [
            Paragraph("<code>model/<br/>FoodItem.java</code>", tbl_cell_bold),
            Paragraph("Base Superclass<br/>(Encapsulated)", tbl_cell),
            Paragraph("<b>Core Domain Entity:</b> Encapsulates common attributes of donated food items (ID, name, category, quantity, basePrice, expiryDate, receivedDate). Features overloaded constructors, parameter validation, and defines the polymorphic base method <code>getStorageInstructions()</code>.", tbl_cell)
        ],
        [
            Paragraph("<code>model/<br/>PerishableItem.java</code>", tbl_cell_bold),
            Paragraph("Subclass<br/><code>extends FoodItem</code>", tbl_cell),
            Paragraph("<b>Cold-Chain Goods:</b> Specializes <code>FoodItem</code> for dairy, meat, and fresh produce. Adds the private attribute <code>optimumTempCelsius</code> and overrides <code>getStorageInstructions()</code> to supply mandatory refrigeration guidelines (e.g. 'Keep refrigerated between 2°C and 4°C').", tbl_cell)
        ],
        [
            Paragraph("<code>model/<br/>PackagedItem.java</code>", tbl_cell_bold),
            Paragraph("Subclass<br/><code>extends FoodItem</code>", tbl_cell),
            Paragraph("<b>Dry / Canned Goods:</b> Specializes <code>FoodItem</code> for dry pantry goods (canned vegetables, rice, cereals). Adds <code>batchNumber</code> for manufacturer recall audits and overrides <code>getStorageInstructions()</code> for dry pantry room-temperature storage.", tbl_cell)
        ],
        [
            Paragraph("<code>model/<br/>DistributionRecord.java</code>", tbl_cell_bold),
            Paragraph("Transaction Audit Entity", tbl_cell),
            Paragraph("<b>Distribution Transaction Model:</b> Immutable representation of an itemized food clearance event. Tracks transaction ID, food item reference, quantity issued, recipient shelter name, base price, dynamic subsidy percentage, effective price, and dispatch timestamp.", tbl_cell)
        ],
        [
            Paragraph("<code>model/<br/>InventoryOperations.java</code>", tbl_cell_bold),
            Paragraph("Interface Contract", tbl_cell),
            Paragraph("<b>Abstract Operational Contract:</b> Declares standard abstract methods for CRUD actions, category searches, restocking, distribution transactions, and analytics aggregation (<code>addItem</code>, <code>getAllItems</code>, <code>recordDistribution</code>).", tbl_cell)
        ],
        [
            Paragraph("<code>database/<br/>DatabaseManager.java</code>", tbl_cell_bold),
            Paragraph("Singleton Pattern<br/>(Thread-Safe)", tbl_cell),
            Paragraph("<b>Central Connection Manager:</b> Ensures only one active connection manager pipeline exists across the JVM lifecycle. Features a private constructor, a <code>static synchronized getInstance()</code> method, and safe connection lifecycle and cleanup methods.", tbl_cell)
        ],
        [
            Paragraph("<code>database/<br/>FoodBankDAO.java</code>", tbl_cell_bold),
            Paragraph("DAO Pattern<br/><code>implements<br/>InventoryOperations</code>", tbl_cell),
            Paragraph("<b>Data Access Object:</b> Bridges Java objects and SQLite. Pre-compiles SQL using parameterized <code>PreparedStatement</code> to prevent SQL injection, maps relational rows (<code>ResultSet</code>) to Java entities, and handles transactional stock deductions.", tbl_cell)
        ],
        [
            Paragraph("<code>database/<br/>DataSeeder.java</code>", tbl_cell_bold),
            Paragraph("Mock Data Utility", tbl_cell),
            Paragraph("<b>Automated Seed Generator:</b> Creates SQLite tables (<code>food_items</code>, <code>distributions</code>) if absent, and populates 10 realistic sample food items across Urgent, High, Medium, and Expired categories for instant evaluation.", tbl_cell)
        ],
        [
            Paragraph("<code>service/<br/>PriorityPricingService.java</code>", tbl_cell_bold),
            Paragraph("Business Logic Service", tbl_cell),
            Paragraph("<b>Computational Engine:</b> Evaluates Days Remaining ($D$), computes Priority Distribution Index (PDI), applies rule-based dynamic subsidies (100% free / 50% discount), and implements in-memory Bubble Sort directly on <code>Vector&lt;FoodItem&gt;</code>.", tbl_cell)
        ]
    ]

    t_cls_1 = Table(cls_data_1, colWidths=[90, 85, 348])
    t_cls_1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0F766E")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cls_1)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SECTION 9 - CLASS REFERENCE PART 2 (EXCEPTIONS, UI, TEST)
    # =========================================================================
    story.append(Paragraph("9. Complete Class Reference Guide (Part 2: Exceptions, UI & Test)", h1_style))
    story.append(Paragraph(
        "Continuing the class-by-class technical breakdown covering custom safety exceptions, Swing UI MVC panels, "
        "and automated quality assurance test harnesses.",
        body_style
    ))

    cls_data_2 = [
        [
            Paragraph("<b>Package / Class</b>", tbl_header),
            Paragraph("<b>Type & Base Class</b>", tbl_header),
            Paragraph("<b>Technical Role, Purpose & Practical Use</b>", tbl_header)
        ],
        [
            Paragraph("<code>exception/<br/>ExpiredItemDistributionException.java</code>", tbl_cell_bold),
            Paragraph("Checked Exception<br/><code>extends Exception</code>", tbl_cell),
            Paragraph("<b>Food Safety Invariant Enforcer:</b> Thrown when an operator attempts to distribute an item with $D < 0$. Because it is a checked exception, the Java compiler mandates explicit <code>try-catch</code> handling, preventing expired food distribution.", tbl_cell)
        ],
        [
            Paragraph("<code>exception/<br/>InvalidQuantityException.java</code>", tbl_cell_bold),
            Paragraph("Checked Exception<br/><code>extends Exception</code>", tbl_cell),
            Paragraph("<b>Inventory Bounds Enforcer:</b> Thrown when user enters non-positive quantities (&le; 0) or attempts to distribute more items than currently exist in stock, preventing negative inventory balances.", tbl_cell)
        ],
        [
            Paragraph("<code>ui/<br/>MainFrame.java</code>", tbl_cell_bold),
            Paragraph("Swing Frame Container<br/><code>extends JFrame</code>", tbl_cell),
            Paragraph("<b>Single-Window Shell:</b> Master window using <code>CardLayout</code> to manage the 5 primary views. Features a unified top navigation toolbar, window listener hooks, and coordinates global table refreshes across views without opening multiple windows.", tbl_cell)
        ],
        [
            Paragraph("<code>ui/<br/>InputPanel.java</code>", tbl_cell_bold),
            Paragraph("Swing Panel View<br/><code>extends JPanel</code>", tbl_cell),
            Paragraph("<b>Module A (Intake):</b> Form view for registering donated items. Enforces field validation (empty check, number formats, ISO <code>YYYY-MM-DD</code> date pattern) and dispatches clean objects to <code>FoodBankDAO</code>.", tbl_cell)
        ],
        [
            Paragraph("<code>ui/<br/>InventoryPanel.java</code>", tbl_cell_bold),
            Paragraph("Swing Panel View<br/><code>extends JPanel</code>", tbl_cell),
            Paragraph("<b>Module B (Expiry Tracker):</b> Live table dashboard with real-time text search, priority category filters, custom table cell renderers showing urgency color badges (Red/Orange/Green), and a button triggering Bubble Sort.", tbl_cell)
        ],
        [
            Paragraph("<code>ui/<br/>ManagementPanel.java</code>", tbl_cell_bold),
            Paragraph("Swing Panel View<br/><code>extends JPanel</code>", tbl_cell),
            Paragraph("<b>Module C (Maintenance):</b> Inventory maintenance terminal. Allows staff to select existing stock, restock incoming donations, update price or storage attributes, or write off damaged stock.", tbl_cell)
        ],
        [
            Paragraph("<code>ui/<br/>DistributionPanel.java</code>", tbl_cell_bold),
            Paragraph("Swing Panel View<br/><code>extends JPanel</code>", tbl_cell),
            Paragraph("<b>Module D (Subsidy Checkout):</b> Point-of-distribution terminal. Calculates dynamic subsidies, catches safety exceptions, updates SQLite inventory, and prints itemized ASCII distribution receipts.", tbl_cell)
        ],
        [
            Paragraph("<code>ui/<br/>AnalyticsPanel.java</code>", tbl_cell_bold),
            Paragraph("Swing Panel View<br/><code>extends JPanel</code>", tbl_cell),
            Paragraph("<b>Module E (Impact Analytics):</b> Executive reporting view. Renders 6 metric cards (total items, urgent items, food waste prevented in kg, total subsidies granted) and an audit table of historical distributions.", tbl_cell)
        ],
        [
            Paragraph("<code>test/<br/>ProjectTestRunner.java</code>", tbl_cell_bold),
            Paragraph("Automated Test Suite", tbl_cell),
            Paragraph("<b>Verification Harness:</b> Executes 35 standalone unit assertions across all packages. Validates inheritance, polymorphism, PDI boundary mathematics, Bubble Sort ordering, safety exceptions, and SQLite DAO queries (100% pass rate).", tbl_cell)
        ],
        [
            Paragraph("<code>test/<br/>CaptureScreenshots.java</code>", tbl_cell_bold),
            Paragraph("Diagnostic Utility", tbl_cell),
            Paragraph("<b>Automated UI Capture:</b> Programmatically initializes GUI frames off-screen and saves high-resolution PNG screenshots of all 5 operational panels for documentation and viva presentations.", tbl_cell)
        ]
    ]

    t_cls_2 = Table(cls_data_2, colWidths=[90, 85, 348])
    t_cls_2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1E3A8A")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cls_2)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Codebase Architecture Summary for Professor Evaluation:", h2_style))
    summary_bullets = [
        "<b>High Cohesion, Low Coupling:</b> The UI classes know only about interfaces and data transfer objects; they never perform direct raw SQL operations.",
        "<b>Extensibility:</b> New food types (e.g. <code>FrozenItem</code>, <code>PreparedMealItem</code>) can be introduced simply by extending <code>FoodItem</code> and overriding <code>getStorageInstructions()</code> without modifying existing code (Open/Closed Principle).",
        "<b>Auditability:</b> Every item issue is tracked in an immutable distribution audit log, ensuring complete transparency for charitable donors."
    ]
    for b in summary_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {output_path}")


if __name__ == '__main__':
    target = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ChronoChef_Pitching_Script_and_Viva_Guide.pdf")
    build_pitch_script_pdf(target)
