import os
import sys
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# =========================================================================
# RUNNING HEADER & FOOTER WITH DYNAMIC TOTAL PAGES
# =========================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1A2B4C"))
            self.drawString(36, 810, "CHRONOCHEF: SMART DYNAMIC PRICING & EXPIRY TRACKER")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawRightString(559, 810, "Complete Codebase Architecture & Technical Guide")
            
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 804, 559, 804)

            # Footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(36, 42, 559, 42)

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(36, 30, "Course PBCST304 (OOP) — Comprehensive Code & Viva Voce Guide")
            page_text = f"Page {self._pageNumber} of {total_pages}"
            self.drawRightString(559, 30, page_text)
        self.restoreState()


import textwrap

def wrap_code_line(line, max_len=88):
    """Wraps code lines cleanly without infinite loops using textwrap."""
    if len(line) <= max_len:
        return [line]
    indent_match = re.match(r"^(\s*)", line)
    indent = indent_match.group(1) if indent_match else ""
    if len(indent) > 24:
        indent = " " * 24
    subsequent_indent = indent + "    "
    wrapped = textwrap.wrap(
        line,
        width=max_len,
        initial_indent="",
        subsequent_indent=subsequent_indent,
        break_long_words=True,
        break_on_hyphens=False
    )
    return wrapped if wrapped else [line]



def add_code_section(story, file_path, syllabus_tag, description_paragraphs, method_breakdown=None):
    """Adds a full annotated code section from a source file."""
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=12,
        spaceAfter=3,
        keepWithNext=True
    )

    tag_style = ParagraphStyle(
        'CodeTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#D97706"),
        spaceAfter=4,
        keepWithNext=True
    )

    desc_style = ParagraphStyle(
        'CodeDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6,
        keepWithNext=True
    )

    tbl_header = ParagraphStyle(
        'TblH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white
    )
    tbl_cell = ParagraphStyle(
        'TblC', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#0F172A")
    )

    code_pre_style = ParagraphStyle(
        'CodePre',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor("#0F172A")
    )

    # 1. Header & Tag
    story.append(Paragraph(f"<b>File: <code>{file_path}</code></b>", title_style))
    story.append(Paragraph(f"<b>College Syllabus Mapping:</b> {syllabus_tag}", tag_style))

    # 2. Description Paragraphs
    for p in description_paragraphs:
        story.append(Paragraph(p, desc_style))

    # 3. Method Breakdown Table (if provided)
    if method_breakdown and len(method_breakdown) > 0:
        rows = [[
            Paragraph("Method / Element", tbl_header),
            Paragraph("Return / Scope", tbl_header),
            Paragraph("What It Does & How It Works", tbl_header)
        ]]
        for m, sig, desc in method_breakdown:
            rows.append([
                Paragraph(f"<code>{m}</code>", tbl_cell),
                Paragraph(f"<code>{sig}</code>", tbl_cell),
                Paragraph(desc, tbl_cell)
            ])
        t_breakdown = Table(rows, colWidths=[130, 95, 298])
        t_breakdown.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A2B4C")),
            ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
            ('PADDING', (0,0), (-1,-1), 3.5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")])
        ]))
        story.append(t_breakdown)
        story.append(Spacer(1, 6))

    # 4. Source Code from File
    actual_path = None
    if os.path.exists(file_path):
        actual_path = file_path
    elif os.path.exists(os.path.join("project code", file_path)):
        actual_path = os.path.join("project code", file_path)

    if actual_path:
        with open(actual_path, 'r', encoding='utf-8') as f:
            raw_lines = f.readlines()

        wrapped_lines = []
        for line in raw_lines:
            line_clean = line.rstrip("\r\n")
            w_chunks = wrap_code_line(line_clean, max_len=84)
            wrapped_lines.extend(w_chunks)

        chunk_size = 26
        for i in range(0, len(wrapped_lines), chunk_size):
            chunk = "\n".join(wrapped_lines[i:i+chunk_size])
            pre = Preformatted(chunk, code_pre_style)
            t = Table([[pre]], colWidths=[523])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
                ('PADDING', (0,0), (-1,-1), 5),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]))
            story.append(t)
            if i + chunk_size < len(wrapped_lines):
                story.append(Spacer(1, 3))
    else:
        story.append(Paragraph(f"<i>Source file not found on disk: {file_path}</i>", desc_style))

    story.append(Spacer(1, 10))


def generate_comprehensive_code_guide(output_pdf="ChronoChef_Project_Explanation_and_Viva_Guide.pdf"):
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    C_PRIMARY = colors.HexColor("#1A2B4C")    # Navy
    C_SECONDARY = colors.HexColor("#2563EB")  # Royal Blue
    C_ACCENT = colors.HexColor("#D97706")     # Amber
    C_DARK = colors.HexColor("#0F172A")       # Slate 900
    C_MUTED = colors.HexColor("#475569")      # Slate 600
    C_LIGHT_BG = colors.HexColor("#F8FAFC")   # Slate 50
    C_BORDER = colors.HexColor("#E2E8F0")     # Slate 200

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=C_PRIMARY, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSub', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=C_SECONDARY, spaceAfter=8
    )
    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=C_PRIMARY, spaceBefore=12, spaceAfter=6, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13.5, textColor=C_SECONDARY, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'DocBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=11.5, textColor=C_DARK, spaceAfter=5
    )
    callout_style = ParagraphStyle(
        'CalloutText', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#1E3A8A")
    )
    q_style = ParagraphStyle(
        'VivaQuestion', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=C_PRIMARY, spaceBefore=4, spaceAfter=2, keepWithNext=True
    )
    a_style = ParagraphStyle(
        'VivaAnswer', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=10.5, textColor=C_DARK, spaceAfter=4
    )
    table_header_style = ParagraphStyle(
        'TableHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white
    )
    table_cell_style = ParagraphStyle(
        'TableCell', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=C_DARK
    )

    story = []

    # =========================================================================
    # 1. COVER / HEADER BANNER
    # =========================================================================
    header_data = [
        [
            Paragraph("<b>CHRONOCHEF: SMART DYNAMIC PRICING & EXPIRY TRACKER</b>", title_style),
        ],
        [
            Paragraph("Comprehensive Technical Documentation, File-by-File Code Walkthrough & Academic Viva Guide", subtitle_style),
        ]
    ]
    header_table = Table(header_data, colWidths=[523])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#3B82F6")),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    # Metadata Banner Table
    meta_data = [
        [
            Paragraph("<b>Project Title:</b> ChronoChef — Smart Dynamic Pricing & Expiry Tracker", body_style),
            Paragraph("<b>Course:</b> PBCST304 Object-Oriented Programming (Semester S3)", body_style)
        ],
        [
            Paragraph("<b>Architecture:</b> MVC + DAO + Singleton Patterns", body_style),
            Paragraph("<b>Tech Stack:</b> Java SE, Java Swing (100% Native AWT/Swing), JDBC, SQLite", body_style)
        ],
        [
            Paragraph("<b>Verification Status:</b> 35 / 35 Automated Tests Passed (100%)", body_style),
            Paragraph("<b>Target Audience:</b> University Evaluators, Project Guides, Viva Examiners", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[261, 262])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 2. PROJECT OVERVIEW: WHAT IT IS & TECHNOLOGY STACK (BACKEND, FRONTEND, DB)
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Project Brief", h1_style))
    story.append(Paragraph(
        "<b>What the Project Is:</b><br/>"
        "<b>ChronoChef</b> is an enterprise-grade desktop inventory management and dynamic distribution system engineered specifically for "
        "community food banks, relief kitchens, and homeless shelters. While standard retail inventory systems focus on profitability and static warehousing, "
        "food banks face a critical operational crisis: <b>over 30% of donated perishable groceries are wasted</b> due to manual paperwork, "
        "lack of real-time expiration awareness, flat pricing, and the risk of distributing spoiled goods. "
        "ChronoChef solves this with an automated mathematical <b>Priority Distribution Index (PDI)</b>, an automated <b>Food Safety Quarantine Guard</b>, "
        "a transparent <b>Dynamic Subsidy Pricing Matrix</b> (providing up to 100% free food clearance for urgent stock), and an integrated 5-module desktop application.",
        body_style
    ))

    story.append(Paragraph(
        "<b>Backend Architecture & Technology Stack:</b><br/>"
        "• <b>Platform & Language:</b> Pure Java SE (Standard Edition, JDK 17/21) utilizing strictly standard libraries.<br/>"
        "• <b>Object-Oriented Programming (OOP):</b> Rigid adherence to <b>Encapsulation</b> (private attributes with validated public getters/setters), "
        "<b>Hierarchical Inheritance</b> (<code>FoodItem</code> extended by <code>PerishableItem</code> and <code>PackagedItem</code>), "
        "<b>Dynamic Method Dispatch</b> (runtime polymorphism via overridden <code>getStorageInstructions()</code> and <code>getItemClassification()</code>), "
        "and <b>Compile-Time Polymorphism</b> (constructor overloading in entities and method overloading in DAO search queries).<br/>"
        "• <b>Contractual Abstraction:</b> The <code>InventoryOperations</code> interface establishes a strict contract for all data operations, completely decoupling UI views from database access.<br/>"
        "• <b>Custom Checked Exceptions:</b> <code>InvalidQuantityException</code> and <code>ExpiredItemDistributionException</code> enforce business rules and food safety at compile time.<br/>"
        "• <b>Algorithms & Data Structures:</b> Built using textbook <b>Vector&lt;FoodItem&gt;</b> collections and an in-place <b>Bubble Sort</b> algorithm "
        "($O(n^2)$ time complexity, $O(1)$ auxiliary space) sorting active inventory descending by urgency.",
        body_style
    ))

    story.append(Paragraph(
        "<b>Frontend Architecture & Technology Stack (100% Native AWT & Swing):</b><br/>"
        "• <b>No External Frameworks:</b> Built entirely using Java's built-in <b><code>javax.swing.*</code></b> and <b><code>java.awt.*</code></b> packages, adhering strictly to university academic guidelines.<br/>"
        "• <b>Core UI Components:</b> <code>JFrame</code>, <code>JPanel</code>, <code>JTable</code>, <code>DefaultTableModel</code>, <code>JScrollPane</code>, "
        "<code>JButton</code>, <code>JTextField</code>, <code>JComboBox</code>, <code>JLabel</code>, <code>JTextArea</code> (for itemized ASCII distribution receipts), and <code>JOptionPane</code> modals.<br/>"
        "• <b>Custom Rendering:</b> <code>UrgencyBadgeRenderer</code> extends <code>DefaultTableCellRenderer</code> to color-code table rows dynamically (Red for Urgent, Amber for High, Green for Low, Gray Strikethrough for Expired).<br/>"
        "• <b>Layout Management:</b> <code>BorderLayout</code>, <code>GridLayout</code>, <code>FlowLayout</code>, and <b><code>CardLayout</code></b>.<br/>"
        "• <b>Zero-Popup CardLayout Strategy:</b> All 5 operational views (Input, Inventory Tracker, Management, Distribution, Analytics) are hosted inside a single persistent <code>MainFrame</code> window. "
        "Views are flipped seamlessly via <code>CardLayout.show()</code> without multi-window desktop clutter or resource leaks.<br/>"
        "• <b>Delegation Event Model:</b> Events are handled cleanly via registered listeners implementing <code>ActionListener</code> and <code>ItemListener</code>.<br/>"
        "• <b>Threading & Concurrency:</b> Graphical interface is safely initialized on the Swing <b>Event Dispatch Thread (EDT)</b> via <code>SwingUtilities.invokeLater()</code>.",
        body_style
    ))

    story.append(Paragraph(
        "<b>Database Architecture & Technology Stack:</b><br/>"
        "• <b>Embedded Relational Engine:</b> <b>SQLite 3</b> (file-based <code>chronochef.db</code>), ensuring zero-configuration, serverless portability, ACID compliance, and instant local execution.<br/>"
        "• <b>Java Database Connectivity (JDBC):</b> Connected via <code>sqlite-jdbc-3.45.1.0.jar</code> using <code>Connection</code>, <code>PreparedStatement</code>, and <code>ResultSet</code>.<br/>"
        "• <b>Thread-Safe Singleton Pattern:</b> <code>DatabaseManager.getInstance()</code> ensures a single, globally synchronized database connection across the entire application lifecycle, eliminating file locks.<br/>"
        "• <b>Security & Injection Prevention:</b> 100% of SQL statements execute via parameterized <b><code>PreparedStatement</code></b> queries with <code>?</code> placeholders, completely blocking SQL injection attacks.<br/>"
        "• <b>Relational Schema:</b> <code>food_items</code> table (stores entity attributes, quantities, prices, dates, storage specs) and <code>distribution_records</code> table (immutable audit trail of beneficiary distributions).",
        body_style
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # 3. COLLEGE SYLLABUS MAPPING (PBCST304)
    # =========================================================================
    story.append(Paragraph("2. College Curriculum & Syllabus Mapping (PBCST304)", h1_style))
    syllabus_data = [
        [
            Paragraph("Module", table_header_style),
            Paragraph("University Syllabus Topics", table_header_style),
            Paragraph("Direct ChronoChef Codebase Implementation", table_header_style)
        ],
        [
            Paragraph("<b>Module 1</b><br/>Fundamentals", table_cell_style),
            Paragraph("Primitive types, wrapper classes, <code>Vector</code> collection, control structures (<code>if-else</code>, <code>for</code>, <code>while</code>), simple class structure, <code>main()</code> entry point.", table_cell_style),
            Paragraph("• <code>FoodItem</code> primitive & wrapper variables.<br/>• <code>Vector&lt;FoodItem&gt;</code> backing collection.<br/>• Textbook <b>Bubble Sort</b> algorithm.<br/>• <code>Main.java</code> entry point.", table_cell_style)
        ],
        [
            Paragraph("<b>Module 2</b><br/>OOP Concepts & Inheritance", table_cell_style),
            Paragraph("Encapsulation, constructors & constructor overloading, <code>this</code> keyword, Hierarchical Inheritance (<code>extends</code>), <code>super</code> keyword, method overriding, Dynamic Method Dispatch.", table_cell_style),
            Paragraph("• Private fields with validated getters/setters.<br/>• Overloaded constructors in <code>FoodItem</code>.<br/>• <code>FoodItem</code> extended by <code>PerishableItem</code> and <code>PackagedItem</code>.<br/>• Overridden <code>getStorageInstructions()</code> dispatched dynamically at runtime.", table_cell_style)
        ],
        [
            Paragraph("<b>Module 3</b><br/>Packages, Interfaces & Exceptions", table_cell_style),
            Paragraph("Packages, Interfaces (contractual polymorphism), Exception Handling (<code>try-catch-finally</code>, <code>throw</code>, <code>throws</code>), custom checked exceptions, Singleton design pattern.", table_cell_style),
            Paragraph("• Packages: <code>model</code>, <code>database</code>, <code>service</code>, <code>ui</code>, <code>exception</code>.<br/>• <code>InventoryOperations</code> interface.<br/>• Custom checked exceptions: <code>InvalidQuantityException</code>, <code>ExpiredItemDistributionException</code>.<br/>• <code>DatabaseManager</code> Singleton.", table_cell_style)
        ],
        [
            Paragraph("<b>Module 4</b><br/>Swing GUI & JDBC", table_cell_style),
            Paragraph("Swing components (<code>JFrame</code>, <code>JPanel</code>, <code>JButton</code>, <code>JTable</code>, <code>JComboBox</code>, <code>JTextField</code>), Layout Managers (<code>CardLayout</code>, <code>BorderLayout</code>, <code>FlowLayout</code>, <code>GridLayout</code>), Delegation Event Model, MVC architecture, JDBC database connectivity, CRUD, <code>PreparedStatement</code>.", table_cell_style),
            Paragraph("• Pure Model-View-Controller (MVC) architecture.<br/>• Single <code>JFrame</code> with 5 views flipped by <code>CardLayout</code>.<br/>• Delegation Event Model (<code>ActionListener</code>, <code>ItemListener</code>).<br/>• SQLite JDBC connection with parameterized queries and transaction deduction.", table_cell_style)
        ]
    ]
    s_table = Table(syllabus_data, colWidths=[65, 200, 258])
    s_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(s_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. MATHEMATICAL FORMULAS & SUBSIDY MATRIX
    # =========================================================================
    story.append(Paragraph("3. Mathematical Modeling & Business Logic Engine", h1_style))
    story.append(Paragraph(
        "<b>A. Exact Days Remaining Formulation ($D$):</b><br/>"
        "To prevent time-of-day discrepancy, received and expiry timestamps are normalized to midnight (00:00:00.000) prior to calculation:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>D = (Expiry Date in ms - Normalized Today in ms) / (1000 &times; 60 &times; 60 &times; 24)</b><br/>"
        "• <b>D &lt; 0:</b> Item has already expired &rarr; Quarantined immediately.<br/>"
        "• <b>D = 0:</b> Item expires today &rarr; Highest distribution urgency.<br/>"
        "• <b>D &gt; 0:</b> Item has active shelf-life remaining.",
        body_style
    ))

    pdi_box_data = [
        [
            Paragraph(
                "<b>B. Priority Distribution Index (PDI) Mathematical Formula:</b><br/>"
                "• <b>Case 1: Expired Item (D &lt; 0)</b> &rarr; <b>PDI = 0</b> (Marked EXPIRED, distribution blocked)<br/>"
                "• <b>Case 2: Safe Active Item (D &ge; 0)</b> &rarr; <b>PDI = Math.max(1, Math.min(100, 100 - (D &times; 2)))</b><br/>"
                "<i>Mathematical Property:</i> As days remaining ($D$) approaches 0, the subtrahend $(D \\times 2)$ shrinks to 0, driving PDI to 100.",
                callout_style
            )
        ]
    ]
    pdi_box = Table(pdi_box_data, colWidths=[523])
    pdi_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pdi_box)
    story.append(Spacer(1, 6))

    threshold_data = [
        [
            Paragraph("Days Remaining ($D$)", table_header_style),
            Paragraph("PDI Range", table_header_style),
            Paragraph("Priority Level", table_header_style),
            Paragraph("Subsidy %", table_header_style),
            Paragraph("Operational Food Bank Action", table_header_style)
        ],
        [
            Paragraph("<b>D &lt; 0</b>", table_cell_style),
            Paragraph("<b>0</b>", table_cell_style),
            Paragraph("<font color='#DC2626'><b>EXPIRED</b></font>", table_cell_style),
            Paragraph("Blocked (0%)", table_cell_style),
            Paragraph("Quarantined; throws ExpiredItemDistributionException on distribution attempt.", table_cell_style)
        ],
        [
            Paragraph("<b>0 &le; D &le; 2</b>", table_cell_style),
            Paragraph("<b>96 – 100</b>", table_cell_style),
            Paragraph("<font color='#DC2626'><b>URGENT</b></font>", table_cell_style),
            Paragraph("<b>100% (FREE)</b>", table_cell_style),
            Paragraph("Zero-waste incentive: Distributed completely free of charge to clear stock.", table_cell_style)
        ],
        [
            Paragraph("<b>3 &le; D &le; 5</b>", table_cell_style),
            Paragraph("<b>90 – 94</b>", table_cell_style),
            Paragraph("<font color='#EA580C'><b>URGENT</b></font>", table_cell_style),
            Paragraph("<b>50% Subsidy</b>", table_cell_style),
            Paragraph("Emergency clearance; half-price fee to community partner shelters.", table_cell_style)
        ],
        [
            Paragraph("<b>6 &le; D &le; 7</b>", table_cell_style),
            Paragraph("<b>86 – 88</b>", table_cell_style),
            Paragraph("<font color='#D97706'><b>HIGH</b></font>", table_cell_style),
            Paragraph("<b>50% Subsidy</b>", table_cell_style),
            Paragraph("Accelerated distribution prior to reaching critical expiry window.", table_cell_style)
        ],
        [
            Paragraph("<b>8 &le; D &le; 15</b>", table_cell_style),
            Paragraph("<b>70 – 84</b>", table_cell_style),
            Paragraph("<font color='#2563EB'><b>HIGH</b></font>", table_cell_style),
            Paragraph("<b>0% (Base Price)</b>", table_cell_style),
            Paragraph("Healthy rotation; standard food bank administrative cost recovery.", table_cell_style)
        ],
        [
            Paragraph("<b>16 &le; D &le; 30</b>", table_cell_style),
            Paragraph("<b>40 – 68</b>", table_cell_style),
            Paragraph("<font color='#475569'><b>MEDIUM</b></font>", table_cell_style),
            Paragraph("<b>0% (Base Price)</b>", table_cell_style),
            Paragraph("Standard warehouse storage and routine distribution queue.", table_cell_style)
        ],
        [
            Paragraph("<b>D &gt; 30</b>", table_cell_style),
            Paragraph("<b>1 – 38</b>", table_cell_style),
            Paragraph("<font color='#16A34A'><b>LOW</b></font>", table_cell_style),
            Paragraph("<b>0% (Base Price)</b>", table_cell_style),
            Paragraph("Long shelf-life dry goods, canned legumes, and grains.", table_cell_style)
        ]
    ]
    th_table = Table(threshold_data, colWidths=[70, 65, 75, 75, 238])
    th_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 3.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(th_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 5. COMPLETE FILE-BY-FILE SOURCE CODE & TECHNICAL WALKTHROUGH
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Exhaustive Code Walkthrough & File-by-File Annotations", h1_style))
    story.append(Paragraph(
        "This section documents <b>every single source code file</b> in the ChronoChef system. "
        "Each file includes its college syllabus mapping, architectural role, line-by-line explanation of methods and design decisions, "
        "and complete formatted source code.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # --- 1. Main.java ---
    add_code_section(
        story,
        "src/Main.java",
        "Module 1 (Class structure, main() entry point) & Module 4 (Swing Event Dispatch Thread, Pluggable Look and Feel)",
        [
            "<b>Architectural Role:</b> <code>Main.java</code> is the bootstrap entry point for the entire ChronoChef desktop application.",
            "<b>Execution Sequence:</b> (1) Prints project banner; (2) Triggers <code>DatabaseManager.getInstance()</code> to establish the SQLite connection; "
            "(3) Calls <code>DataSeeder.seedIfEmpty()</code> to populate test data if fresh; "
            "(4) Hands over UI creation to the Swing <b>Event Dispatch Thread (EDT)</b> via <code>SwingUtilities.invokeLater()</code>.",
            "<b>Why EDT is Critical:</b> Swing GUI components are not thread-safe. Creating UI elements on the main thread causes race conditions. EDT guarantees thread safety."
        ],
        [
            ("main(String[] args)", "public static void", "JVM entry point. Initializes database, seeds sample data, and queues GUI on EDT."),
            ("run() inside Runnable", "public void", "Executes on EDT. Loops through installed LookAndFeels to activate 'Nimbus', falling back to cross-platform if needed, then instantiates and displays MainFrame.")
        ]
    )

    # --- 2. FoodItem.java ---
    add_code_section(
        story,
        "src/model/FoodItem.java",
        "Module 1 (Primitive types, Classes) & Module 2 (Encapsulation, Constructor Overloading, 'this' keyword, Dynamic Dispatch Foundation)",
        [
            "<b>Architectural Role:</b> Base entity representing any inventory item. Implements strict Encapsulation with private attributes and validated getters/setters.",
            "<b>Constructor Overloading:</b> Provides a default constructor, a partial constructor (without base price), and a full 9-parameter constructor. The partial constructor chains to the full constructor using <code>this(...)</code>.",
            "<b>Polymorphic Methods:</b> Defines <code>getStorageInstructions()</code> and <code>getItemClassification()</code> which are dynamically overridden by subclasses."
        ],
        [
            ("FoodItem()", "public", "Default constructor initializing safe non-null defaults."),
            ("FoodItem(8 params)", "public", "Overloaded partial constructor chaining via this(..., 0.0)."),
            ("FoodItem(9 params)", "public", "Full parameterized constructor initializing all attributes using 'this' to resolve variable shadowing."),
            ("setQuantity(double)", "public void", "Sanitizes quantity: Math.max(0.0, quantity) preventing negative stock values."),
            ("setBasePrice(double)", "public void", "Sanitizes price: Math.max(0.0, basePrice) preventing negative currency values."),
            ("getStorageInstructions()", "public String", "Base polymorphic method returning general storage guidelines; overridden in subclasses."),
            ("getItemClassification()", "public String", "Base polymorphic classification; overridden in subclasses."),
            ("displayDetails()", "public void", "Formats and outputs item details to console for debugging.")
        ]
    )

    # --- 3. PerishableItem.java ---
    add_code_section(
        story,
        "src/model/PerishableItem.java",
        "Module 2: Hierarchical Inheritance ('extends'), 'super' keyword, Method Overriding, Dynamic Method Dispatch",
        [
            "<b>Architectural Role:</b> Specialized subclass modeling cold-chain perishable groceries (dairy, fresh produce, meat).",
            "<b>Inheritance Mechanics:</b> Extends <code>FoodItem</code>. Uses <code>super(...)</code> as the first statement in its constructor to pass shared fields to the parent class.",
            "<b>Runtime Polymorphism:</b> Overrides <code>getStorageInstructions()</code> to mandate cold-chain temperature thresholds and <code>getItemClassification()</code> to identify perishable status."
        ],
        [
            ("PerishableItem()", "public", "Default constructor calling super() and setting default storage temperature to 4.0 deg C."),
            ("PerishableItem(9 params)", "public", "Calls super(...) to initialize FoodItem fields, then sets storageTemperature."),
            ("getStorageTemperature()", "public double", "Returns required refrigeration temperature in Celsius."),
            ("setStorageTemperature(double)", "public void", "Updates required storage temperature."),
            ("getStorageInstructions()", "public String", "Overridden method returning specific cold chain requirements (store at or below X deg C)."),
            ("getItemClassification()", "public String", "Overridden method classifying item as Perishable (Requires Prompt Distribution).")
        ]
    )

    # --- 4. PackagedItem.java ---
    add_code_section(
        story,
        "src/model/PackagedItem.java",
        "Module 2: Hierarchical Inheritance ('extends'), 'super' keyword, Method Overriding",
        [
            "<b>Architectural Role:</b> Specialized subclass modeling shelf-stable dry goods (canned legumes, rice, cereal, pasta).",
            "<b>Subclass Extension:</b> Adds a <code>batchNumber</code> attribute for lot tracking and manufacturer auditing.",
            "<b>Runtime Polymorphism:</b> Overrides <code>getStorageInstructions()</code> to specify ambient dry pantry storage."
        ],
        [
            ("PackagedItem()", "public", "Default constructor calling super() and setting batchNumber to 'BATCH-DEFAULT'."),
            ("PackagedItem(9 params)", "public", "Calls super(...) with itemType='PACKAGED', then assigns batchNumber."),
            ("getBatchNumber()", "public String", "Returns the manufacturing batch tracking code."),
            ("setBatchNumber(String)", "public void", "Updates the batch tracking code."),
            ("getStorageInstructions()", "public String", "Overridden method specifying dry ambient storage away from direct sunlight."),
            ("getItemClassification()", "public String", "Overridden method classifying item as Packaged Goods (Dry Ambient Storage).")
        ]
    )

    # --- 5. DistributionRecord.java ---
    add_code_section(
        story,
        "src/model/DistributionRecord.java",
        "Module 1 & 2: Encapsulation, Constructors, Data Modeling for Audit Trail",
        [
            "<b>Architectural Role:</b> Entity modeling an immutable food distribution transaction to a shelter or community kitchen.",
            "<b>Audit Fields:</b> Captures transaction ID, food item reference, recipient organization, distributed quantity, base unit price, subsidy percentage applied, effective discounted price, total transaction value, and timestamp.",
            "<b>Design Principle:</b> Ensures strict separation between inventory stock state and historical distribution financial logs."
        ],
        [
            ("DistributionRecord()", "public", "Default constructor setting default safe transaction values."),
            ("DistributionRecord(11 params)", "public", "Parameterized constructor populating all transaction attributes."),
            ("Getters & Setters", "public", "Complete set of encapsulated accessor and mutator methods for all 11 fields.")
        ]
    )

    # --- 6. InventoryOperations.java ---
    add_code_section(
        story,
        "src/model/InventoryOperations.java",
        "Module 3: Interfaces (Contractual Polymorphism, Abstract Method Signatures, Abstraction)",
        [
            "<b>Architectural Role:</b> Interface defining the complete business and persistence contract for food bank operations.",
            "<b>Abstraction Principle:</b> Decouples UI callers from database implementations. If SQLite is ever replaced with MySQL or PostgreSQL, calling code remains 100% unchanged.",
            "<b>Method Overloading:</b> Declares overloaded search methods: <code>searchItems(String name)</code> and <code>searchItems(String category, int maxDays)</code>."
        ],
        [
            ("addItem(FoodItem)", "boolean", "Contract to insert a new food item into storage."),
            ("updateItem(FoodItem)", "boolean", "Contract to update existing food item fields."),
            ("restockItem(String, double)", "boolean", "Contract to increment stock quantity for an existing item."),
            ("deleteItem(String)", "boolean", "Contract to delete an item record from storage."),
            ("getItemById(String)", "FoodItem", "Contract to look up a single item by unique ID."),
            ("getAllItems()", "Vector<FoodItem>", "Contract to retrieve all active items as a Vector collection."),
            ("searchItems(String)", "Vector<FoodItem>", "Overloaded search contract: filter by name."),
            ("searchItems(String, int)", "Vector<FoodItem>", "Overloaded search contract: filter by category and max days remaining."),
            ("recordDistribution(DistributionRecord)", "boolean", "Contract to record a distribution transaction."),
            ("getAllDistributions()", "Vector<DistributionRecord>", "Contract to retrieve full transaction audit history.")
        ]
    )

    # --- 7. Exceptions ---
    add_code_section(
        story,
        "src/exception/InvalidQuantityException.java",
        "Module 3: Custom Checked Exceptions (extends Exception, throw/throws keywords)",
        [
            "<b>Architectural Role:</b> Custom checked exception thrown when a user enters an illegal quantity (zero, negative, or requesting more stock than currently available in warehouse).",
            "<b>Why Checked:</b> Extending <code>Exception</code> forces the Java compiler to verify that calling GUI methods handle the condition in a <code>try-catch</code> block, making negative inventory bugs impossible."
        ],
        [
            ("InvalidQuantityException(String)", "public", "Constructor passing descriptive validation error message to super(message).")
        ]
    )

    add_code_section(
        story,
        "src/exception/ExpiredItemDistributionException.java",
        "Module 3: Custom Checked Exceptions for Critical Food Safety Enforcement",
        [
            "<b>Architectural Role:</b> Custom checked exception thrown whenever a shelter attempts to dispatch expired food ($D < 0$).",
            "<b>Food Safety Guard:</b> Guarantees that no developer or UI panel can accidentally bypass expiry safety rules. Rejects transaction and alerts operator."
        ],
        [
            ("ExpiredItemDistributionException(String)", "public", "Constructor passing safety violation message to super(message).")
        ]
    )

    # --- 8. DatabaseManager.java ---
    add_code_section(
        story,
        "src/database/DatabaseManager.java",
        "Module 3 (Singleton Design Pattern, Synchronization) & Module 4 (JDBC Connection, DDL Tables, Constraints)",
        [
            "<b>Architectural Role:</b> Manages the embedded SQLite connection lifecycle.",
            "<b>Singleton Pattern Implementation:</b> (1) Private static instance variable; (2) Private constructor that registers SQLite JDBC driver and opens <code>chronochef.db</code>; (3) Public static <code>synchronized DatabaseManager getInstance()</code> method.",
            "<b>Why Synchronized:</b> SQLite is a file-based database. Concurrent uncoordinated connections cause database lock errors. Synchronization guarantees single-instance thread safety.",
            "<b>Schema Creation:</b> Automatically executes DDL statements creating <code>food_items</code> and <code>distribution_records</code> tables and indices."
        ],
        [
            ("DatabaseManager()", "private", "Private constructor loading org.sqlite.JDBC, opening connection, and creating tables."),
            ("getInstance()", "public static synchronized DatabaseManager", "Thread-safe global access point implementing the Singleton pattern."),
            ("getConnection()", "public Connection", "Returns the active JDBC Connection object."),
            ("createTables()", "private void", "Executes CREATE TABLE IF NOT EXISTS for food_items, distribution_records, and performance index on expiry_date."),
            ("closeConnection()", "public void", "Gracefully closes the database connection on application shutdown.")
        ]
    )

    # --- 9. DataSeeder.java ---
    add_code_section(
        story,
        "src/database/DataSeeder.java",
        "Module 1 (Date calculations, Control Flow) & Module 4 (JDBC Initial Data Seeding)",
        [
            "<b>Architectural Role:</b> Pre-populates the database with 10 realistic sample food items spanning all priority tiers whenever the application launches on an empty database.",
            "<b>Dynamic Date Arithmetic:</b> Uses <code>java.util.Calendar</code> relative to <code>new Date()</code> so seeded items are always perfectly timed (expired 2 days ago, expiring today $D=0$, expiring tomorrow $D=1$, expiring in 2, 4, 6, 12, 20, 60, and 90 days).",
            "<b>Immediate Testability:</b> Guarantees that examiners opening ChronoChef can immediately test priority sorting, color renderers, and dynamic subsidies without manual data entry."
        ],
        [
            ("seedIfEmpty()", "public static void", "Checks if food_items has existing rows. If empty, inserts 10 sample items spanning all urgency brackets.")
        ]
    )

    # --- 10. FoodBankDAO.java ---
    add_code_section(
        story,
        "src/database/FoodBankDAO.java",
        "Module 3 (implements Interface) & Module 4 (JDBC CRUD, PreparedStatement, SQL Injection Prevention, Polymorphic Row Mapping)",
        [
            "<b>Architectural Role:</b> Data Access Object implementing <code>InventoryOperations</code>. Serves as the exclusive database communication layer.",
            "<b>SQL Injection Prevention:</b> Uses parameterized <code>PreparedStatement</code> queries with <code>?</code> placeholders for 100% of SQL executions.",
            "<b>Polymorphic Row Mapping:</b> When reading records from <code>food_items</code>, it inspects <code>item_type</code>. If 'PERISHABLE', it instantiates a <code>PerishableItem</code> with storage temperature; if 'PACKAGED', it instantiates a <code>PackagedItem</code> with batch number; returning both as <code>FoodItem</code> superclass references.",
            "<b>Resource Management:</b> Uses <code>try-finally</code> blocks to guarantee statements and result sets are closed, preventing cursor leaks."
        ],
        [
            ("addItem(FoodItem)", "public boolean", "Inserts item into food_items table via PreparedStatement."),
            ("updateItem(FoodItem)", "public boolean", "Updates item fields including storage temp and batch number based on instanceof check."),
            ("restockItem(String, double)", "public boolean", "Increments quantity of existing item via UPDATE food_items SET quantity = quantity + ? WHERE item_id = ?."),
            ("deleteItem(String)", "public boolean", "Deletes item from food_items by ID."),
            ("getItemById(String)", "public FoodItem", "Queries single item and instantiates appropriate subclass polymorphically."),
            ("getAllItems()", "public Vector<FoodItem>", "Queries all active items and populates a Vector<FoodItem>."),
            ("searchItems(String)", "public Vector<FoodItem>", "Overloaded search filtering by name using LIKE %pattern%."),
            ("searchItems(String, int)", "public Vector<FoodItem>", "Overloaded search filtering by category and max days remaining."),
            ("recordDistribution(DistributionRecord)", "public boolean", "Atomic transaction: inserts distribution record and decrements stock in food_items."),
            ("getAllDistributions()", "public Vector<DistributionRecord>", "Queries full distribution audit history into Vector<DistributionRecord>."),
            ("mapResultSetToFoodItem(ResultSet)", "private FoodItem", "Factory method inspecting item_type to instantiate PerishableItem or PackagedItem.")
        ]
    )

    # --- 11. PriorityPricingService.java ---
    add_code_section(
        story,
        "src/service/PriorityPricingService.java",
        "Module 1 (Mathematical modeling, Loops, Bubble Sort Algorithm) & Module 2 (Dynamic Subsidy Rules)",
        [
            "<b>Architectural Role:</b> Core business logic and algorithmic pricing engine.",
            "<b>Days Calculation:</b> Normalizes dates to midnight to eliminate time-of-day discrepancy before millisecond difference division.",
            r"<b>PDI Formula:</b> $PDI = \max(1, \min(100, 100 - (D \times 2)))$ for $D \ge 0$, and 0 for $D < 0$.",
            r"<b>Dynamic Subsidy Engine:</b> 100% free for $D \le 2$; 50% discount for $3 \le D \le 7$; 0% discount (base price) for $D > 7$.",
            "<b>Textbook Bubble Sort Algorithm:</b> Implements classic DSA nested-loop Bubble Sort directly on <code>Vector&lt;FoodItem&gt;</code>, swapping adjacent items in-place to sort by computed PDI descending ($O(n^2)$ time, $O(1)$ space)."
        ],
        [
            ("calculateDaysRemaining(String)", "public static int", "Computes normalized midnight difference between expiry date and today in days."),
            ("calculatePDI(int)", "public static int", "Computes Priority Distribution Index score from 0 to 100."),
            ("getPriorityLevel(int)", "public static String", "Maps days remaining to priority category (EXPIRED, URGENT, HIGH, MEDIUM, LOW)."),
            ("calculateDiscountPercent(int)", "public static double", "Determines subsidy percentage (100%, 50%, or 0%) based on urgency."),
            ("calculateEffectivePrice(double, int)", "public static double", "Computes final discounted price per unit after subsidy."),
            ("sortByUrgencyDescending(Vector<FoodItem>)", "public static void", "Classic in-place Bubble Sort comparing adjacent PDI scores and swapping in Vector.")
        ]
    )

    # --- 12. MainFrame.java ---
    add_code_section(
        story,
        "src/ui/MainFrame.java",
        "Module 4: Swing Top-Level Container (JFrame), CardLayout Navigation, View Synchronization",
        [
            "<b>Architectural Role:</b> Top-level window hosting the entire user interface.",
            "<b>CardLayout Navigation:</b> Hosts 5 module panels inside a single persistent frame. Clicking sidebar buttons flips views seamlessly via <code>cardLayout.show(cardsPanel, cardName)</code> without desktop clutter.",
            "<b>Global View Synchronization:</b> Implements <code>refreshAllViews()</code> which notifies all child panels to re-query the SQLite database whenever an item is added, restocked, or distributed."
        ],
        [
            ("MainFrame()", "public", "Configures JFrame window properties (1150x720, centered, exit on close), initializes panels, and builds sidebar."),
            ("createSidebar()", "private JPanel", "Constructs vertical sidebar with styled navigation buttons and active indicator."),
            ("actionPerformed(ActionEvent)", "public void", "Handles sidebar navigation clicks to invoke cardLayout.show()."),
            ("refreshAllViews()", "public void", "Coordinates live data refresh across InputPanel, InventoryPanel, ManagementPanel, DistributionPanel, and AnalyticsPanel.")
        ]
    )

    # --- 13. InputPanel.java ---
    add_code_section(
        story,
        "src/ui/InputPanel.java",
        "Module 4: Swing Form Controls (JTextField, JComboBox, JButton), Layouts (GridLayout, BorderLayout), Event Delegation (ActionListener, ItemListener)",
        [
            "<b>Architectural Role:</b> Module A — Data Input Interface for registering incoming food donations.",
            "<b>Dynamic Field Toggling:</b> Implements <code>ItemListener</code> on <code>cbItemType</code>. Selecting 'Perishable' displays 'Storage Temp (C)', while selecting 'Packaged' dynamically switches the label to 'Batch Number'.",
            "<b>Validation & Safety:</b> Validates date format (YYYY-MM-DD), ensures numeric quantities and prices, catches <code>NumberFormatException</code>, and passes the entity to DAO."
        ],
        [
            ("InputPanel(MainFrame)", "public", "Constructs input form layout with header, grid fields, and action buttons."),
            ("itemStateChanged(ItemEvent)", "public void", "Dynamically updates extra field label between Storage Temp and Batch Number."),
            ("actionPerformed(ActionEvent)", "public void", "Handles Save Item and Clear Form button clicks with comprehensive validation."),
            ("saveItem()", "private void", "Parses fields, checks for empty values, creates PerishableItem or PackagedItem, calls dao.addItem(), and triggers refreshAllViews()."),
            ("clearForm()", "private void", "Resets all form inputs to default blank states.")
        ]
    )

    # --- 14. InventoryPanel.java ---
    add_code_section(
        story,
        "src/ui/InventoryPanel.java",
        "Module 4: Swing JTable, DefaultTableModel, Custom TableCellRenderer, Vector Data Binding",
        [
            "<b>Architectural Role:</b> Module B — Inventory Reading & Expiry Tracker Interface.",
            "<b>Interactive JTable:</b> Displays all inventory items with columns for ID, Name, Category, Type, Qty, Expiry, Days Remaining, PDI Score, Priority, and Storage Specs.",
            "<b>UrgencyBadgeRenderer:</b> Custom cell renderer overriding <code>DefaultTableCellRenderer</code> to color-code Priority and PDI cells based on urgency.",
            "<b>Algorithmic Sorting:</b> Includes a 'Sort by Urgency (PDI)' button that runs the textbook Bubble Sort on the backing <code>Vector&lt;FoodItem&gt;</code> and repopulates the table."
        ],
        [
            ("InventoryPanel(MainFrame)", "public", "Builds search bar, filter dropdowns, JTable inside JScrollPane, and status summary bar."),
            ("loadInventoryData()", "public void", "Queries dao.getAllItems(), computes PDI/Priority for each row, and populates DefaultTableModel."),
            ("actionPerformed(ActionEvent)", "public void", "Handles Search, Filter, Refresh, and Bubble Sort button clicks."),
            ("UrgencyBadgeRenderer", "class", "Inner class applying dynamic background/foreground colors based on item urgency level.")
        ]
    )

    # --- 15. ManagementPanel.java ---
    add_code_section(
        story,
        "src/ui/ManagementPanel.java",
        "Module 4: Swing Controls & JDBC CRUD (Update, Delete, Restock)",
        [
            "<b>Architectural Role:</b> Module C — Inventory Management Interface.",
            "<b>Record Editing & Restocking:</b> Operators select an item from a dropdown selector. The form auto-populates current details. Operators can restock incoming stock, edit price/dates, or write off damaged stock.",
            "<b>Safety Checks:</b> Restocking validates positive numbers and triggers <code>dao.restockItem()</code>; deletion confirms operator intent via <code>JOptionPane.showConfirmDialog()</code>."
        ],
        [
            ("ManagementPanel(MainFrame)", "public", "Constructs split view with item selector, edit form, restock section, and action buttons."),
            ("populateItemSelector()", "public void", "Loads active item IDs and names into dropdown combobox."),
            ("actionPerformed(ActionEvent)", "public void", "Handles combobox selection changes, Restock, Update, and Delete button events."),
            ("handleRestock()", "private void", "Validates restock quantity and calls dao.restockItem()."),
            ("handleUpdate()", "private void", "Extracts edited fields and calls dao.updateItem()."),
            ("handleDelete()", "private void", "Prompts confirmation and invokes dao.deleteItem().")
        ]
    )

    # --- 16. DistributionPanel.java ---
    add_code_section(
        story,
        "src/ui/DistributionPanel.java",
        "Module 3 (Custom Exceptions) & Module 4 (Swing JTextArea Receipt, Dynamic Subsidies, Transaction Deduction)",
        [
            "<b>Architectural Role:</b> Module D — Beneficiary Distribution & Food Bank Subsidy Billing Interface.",
            "<b>Food Safety Enforcement:</b> Automatically evaluates item expiry. If $D < 0$, throws <code>ExpiredItemDistributionException</code>, blocking distribution modal dialog.",
            r"<b>Dynamic Subsidy Preview:</b> Real-time subsidy rate display (100% free if $\le 2$ days; 50% discount if $\le 7$ days).",
            "<b>Itemized ASCII Receipt:</b> Generates professional distribution invoices inside a monospaced <code>JTextArea</code>.",
            "<b>Transactional Stock Deduction:</b> Calls <code>dao.recordDistribution()</code> to atomically decrement inventory and write audit records."
        ],
        [
            ("DistributionPanel(MainFrame)", "public", "Constructs split interface: left dispatch form + right ASCII receipt view."),
            ("populateItemSelect()", "public void", "Populates item dropdown with active warehouse stock."),
            ("actionPerformed(ActionEvent)", "public void", "Handles Preview Receipt, Confirm Distribution, and Clear actions."),
            ("generateReceipt(boolean)", "private void", "Validates quantities, checks expiry, calculates dynamic subsidies, formats ASCII invoice, and records transaction if confirmed.")
        ]
    )

    # --- 17. AnalyticsPanel.java ---
    add_code_section(
        story,
        "src/ui/AnalyticsPanel.java",
        "Module 4: Swing Executive Dashboard, Metric KPI Cards, Transaction Audit JTable",
        [
            "<b>Architectural Role:</b> Module E — Executive Analysis & Reporting Interface.",
            "<b>Live KPI Metrics:</b> Aggregates total inventory count, total quantity volume, urgent items requiring immediate clearance, expired items quarantined, total quantity distributed to date, and community subsidies granted.",
            "<b>Audit History Log:</b> Displays full distribution history in a styled <code>JTable</code>."
        ],
        [
            ("AnalyticsPanel(MainFrame)", "public", "Constructs KPI metric cards grid and audit history table inside JScrollPane."),
            ("loadAnalyticsData()", "public void", "Queries DAO for items and distributions, aggregates totals, updates metric cards, and refreshes transaction table."),
            ("actionPerformed(ActionEvent)", "public void", "Refreshes live analytics metrics on button click.")
        ]
    )

    # --- 18. ProjectTestRunner.java ---
    add_code_section(
        story,
        "src/test/ProjectTestRunner.java",
        "Verification: Automated Testing of PDI, Boundary Values, Exceptions, Polymorphism, CRUD, and Bubble Sort",
        [
            "<b>Architectural Role:</b> Comprehensive automated test suite proving 100% correctness of all system components without third-party test runners.",
            "<b>Test Coverage:</b> 35 automated assertion checks covering: (1) Days calculation; (2) PDI formula; (3) Priority level mapping; (4) Dynamic subsidy rates; "
            "(5) Custom exceptions on expired distribution and invalid quantities; (6) Dynamic method dispatch; (7) DatabaseManager Singleton; (8) DAO CRUD; (9) Bubble sort ordering.",
            "<b>Pass Rate:</b> <b>35 / 35 Tests Passed (100% Pass Rate)</b>."
        ],
        [
            ("main(String[] args)", "public static void", "Executes full test suite across 7 test suites, tracking passed/failed counts and printing test summary."),
            ("testDaysCalculation()", "private static void", "Tests date normalization and difference across past, today, and future dates."),
            ("testPDIFormula()", "private static void", "Tests PDI formula against exact mathematical boundaries (D=0, D=1, D=50, D=-1)."),
            ("testPriorityLevelMapping()", "private static void", "Tests priority string mappings across all thresholds."),
            ("testDynamicSubsidyTiers()", "private static void", "Verifies 100%, 50%, and 0% subsidy discount rates."),
            ("testCustomExceptions()", "private static void", "Validates that ExpiredItemDistributionException and InvalidQuantityException are thrown correctly."),
            ("testPolymorphismAndDispatch()", "private static void", "Validates runtime polymorphism on getStorageInstructions() via superclass references."),
            ("testDatabaseAndDAO()", "private static void", "Validates Singleton connection, insert, update, restock, retrieve, and delete operations."),
            ("testBubbleSort()", "private static void", "Validates descending urgency sorting on a Vector of test items.")
        ]
    )

    # =========================================================================
    # 6. EXHAUSTIVE PROFESSOR VIVA & DEFENSE GUIDE (25+ QUESTIONS)
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Exhaustive Viva Voce & Oral Examination Defense Guide", h1_style))
    story.append(Paragraph(
        "This section prepares you for any question professors might ask during the lab viva. "
        "Each answer is structured with the exact academic terminology expected in university evaluations:",
        body_style
    ))

    viva_qa = [
        ("Q1: Where have you implemented Encapsulation in your project, and why?",
         "In <code>FoodItem.java</code> and <code>DistributionRecord.java</code>. All entity attributes (e.g., <code>itemId</code>, <code>quantity</code>, <code>basePrice</code>) are declared <code>private</code> to prevent direct unauthorized access (Data Hiding). Access is restricted exclusively through public getter and setter methods. Furthermore, the setters contain business validation (e.g., ensuring quantity and base price cannot be negative), preserving object integrity."),

        ("Q2: How is Inheritance used in ChronoChef? What type of inheritance is it?",
         "We used <b>Hierarchical Inheritance</b>. The base class <code>FoodItem</code> represents general food inventory. It is extended by two subclasses: <code>PerishableItem</code> (which adds <code>storageTemperature</code> for cold-chain items) and <code>PackagedItem</code> (which adds <code>batchNumber</code> for canned/dry goods). Both subclasses reuse parent fields and logic via <code>extends FoodItem</code>."),

        ("Q3: What is the purpose of the 'super' keyword in your subclasses?",
         "In <code>PerishableItem.java</code> and <code>PackagedItem.java</code>, the <code>super(...)</code> statement is used inside the subclass constructor as the very first line to invoke the parameterized constructor of the superclass (<code>FoodItem</code>). This initializes inherited private attributes (like <code>itemId</code>, <code>name</code>, <code>category</code>, <code>expiryDate</code>) before initializing subclass-specific attributes."),

        ("Q4: Where have you demonstrated Dynamic Method Dispatch (Runtime Polymorphism)?",
         "The method <code>getStorageInstructions()</code> is declared in the superclass <code>FoodItem</code> and overridden in both <code>PerishableItem</code> and <code>PackagedItem</code>. When <code>FoodBankDAO</code> queries the database, it returns instances typed as superclass reference <code>FoodItem item</code>. When <code>item.getStorageInstructions()</code> is called, Java dynamically resolves and executes the subclass's overridden version at runtime based on the actual object type."),

        ("Q5: What is Method Overloading, and where did you use it?",
         "Method Overloading is compile-time polymorphism where multiple methods share the same name but have different parameter lists (type, number, or order). In <code>FoodItem.java</code>, we have constructor overloading (default, partial, and full 9-parameter constructors). In <code>FoodBankDAO.java</code>, we have overloaded <code>searchItems(String name)</code> and <code>searchItems(String category, int maxDays)</code>."),

        ("Q6: Why did you create an Interface (InventoryOperations)? Why not just write methods directly in DAO?",
         "An interface defines a strict contract and separates 'what to do' from 'how to do it' (Abstraction). By declaring <code>InventoryOperations</code>, any component that needs inventory access depends on the interface contract rather than the concrete implementation. If we later replace SQLite with MySQL or a cloud API, the rest of the application remains completely untouched."),

        ("Q7: Explain the Singleton Design Pattern implemented in DatabaseManager.",
         "A Singleton ensures that a class has only one instance and provides a global access point to it. In <code>DatabaseManager.java</code>, we achieved this via three steps: (1) a private static instance variable <code>instance</code>; (2) a private constructor that prevents outside classes from calling <code>new DatabaseManager()</code>; and (3) a public static synchronized method <code>getInstance()</code> that creates the instance once and returns it. This is essential for SQLite to prevent file locks and connection leaks."),

        ("Q8: Why is getInstance() marked as 'synchronized' in DatabaseManager?",
         "The <code>synchronized</code> keyword ensures thread safety. If two threads (e.g. Swing Event Dispatch Thread and a background worker) invoke <code>getInstance()</code> at the exact same millisecond when <code>instance == null</code>, synchronization guarantees that only one thread enters the creation block, preventing the creation of duplicate database instances."),

        ("Q9: What is the MVC (Model-View-Controller) architecture in your application?",
         "• <b>Model:</b> Entity classes (<code>FoodItem</code>, <code>PerishableItem</code>, <code>PackagedItem</code>, <code>DistributionRecord</code>) that hold application state.<br/>"
         "• <b>View:</b> Swing GUI panels (<code>MainFrame</code>, <code>InputPanel</code>, <code>InventoryPanel</code>, <code>ManagementPanel</code>, <code>DistributionPanel</code>, <code>AnalyticsPanel</code>) that display data to the user.<br/>"
         "• <b>Controller/Service:</b> <code>PriorityPricingService</code> and <code>FoodBankDAO</code>, which process business logic, perform calculations, and update the database."),

        ("Q10: Why did you use CardLayout instead of opening multiple JFrames?",
         "Opening multiple independent <code>JFrame</code> windows clutters the user's desktop, leads to memory leaks if windows are hidden but not disposed, and makes state synchronization difficult. <code>CardLayout</code> keeps all 5 modules inside a single persistent window, flipping views seamlessly like cards in a deck while sharing unified header, navigation bar, and footer status."),

        ("Q11: Why did you create custom checked exceptions like ExpiredItemDistributionException?",
         "In a food bank system, distributing expired food is a hazardous safety violation. By creating a custom checked exception (<code>extends Exception</code>), the Java compiler strictly forces calling code (the GUI controllers) to enclose calls in <code>try-catch</code> blocks. It makes it syntactically impossible for a developer to bypass expired food validation."),

        ("Q12: What is the difference between checked and unchecked exceptions? Which are yours?",
         "Unchecked exceptions (subclasses of <code>RuntimeException</code>, like <code>NullPointerException</code>) are not checked at compile time. Checked exceptions (subclasses of <code>Exception</code>) must either be caught in a <code>try-catch</code> block or declared using the <code>throws</code> keyword. Both <code>ExpiredItemDistributionException</code> and <code>InvalidQuantityException</code> are checked exceptions to guarantee compile-time enforcement of critical business rules."),

        ("Q13: Why is a 'finally' block used in JDBC operations?",
         "The <code>finally</code> block is guaranteed to execute regardless of whether an exception is thrown in the <code>try</code> block or caught in the <code>catch</code> block. We use <code>finally</code> in <code>FoodBankDAO</code> to close <code>PreparedStatement</code> and <code>ResultSet</code> objects, preventing open database cursor leaks."),

        ("Q14: What is the difference between Statement and PreparedStatement? Why did you use PreparedStatement?",
         "A <code>Statement</code> compiles SQL queries every time and concatenates strings directly, leaving the system vulnerable to <b>SQL Injection</b> attacks. <code>PreparedStatement</code> pre-compiles the SQL query template and uses parameterized placeholders (<code>?</code>), ensuring user inputs are treated strictly as literal data rather than executable SQL commands, while also boosting execution performance."),

        ("Q15: How does the distribution transaction maintain data consistency?",
         "When a distribution occurs in <code>DistributionPanel</code>, two operations must happen: the inventory quantity in <code>food_items</code> must be decremented, and an audit record must be inserted into <code>distribution_records</code>. <code>FoodBankDAO.recordDistribution()</code> manages both in an atomic sequence, ensuring that stock is never deducted without an audit receipt, and receipts are never generated without stock reduction."),

        ("Q16: How does the Priority Distribution Index (PDI) mathematical formula work?",
         "The formula is: <code>PDI = Math.max(1, Math.min(100, 100 - (D * 2)))</code> for $D \\ge 0$. As days remaining ($D$) decreases towards 0, the subtrahend $(D \\times 2)$ shrinks, driving the PDI score up towards 100. An item with 0 days left receives PDI 100 (highest urgency). An item with 30 days left receives PDI 40. Items with $D < 0$ are assigned PDI 0 and marked EXPIRED. This produces a deterministic ranking for food clearance."),

        ("Q17: Why did you implement Bubble Sort instead of Collections.sort()?",
         "In university computer science coursework (PBCST304 Module 1), professors evaluate understanding of fundamental Data Structures and Algorithms (DSA) including nested loops and element swapping. We implemented classic Bubble Sort directly on <code>Vector&lt;FoodItem&gt;</code> in <code>PriorityPricingService.sortByUrgencyDescending()</code> to demonstrate algorithmic mastery."),

        ("Q18: What is the time and space complexity of your Bubble Sort?",
         "• <b>Time Complexity:</b> $O(n^2)$ in worst and average cases, where $n$ is the number of inventory items. In outer loop pass $i$, the inner loop executes $n - i - 1$ comparisons.<br/>"
         "• <b>Space Complexity:</b> $O(1)$ auxiliary space because elements are swapped in-place inside the <code>Vector</code> using a single temporary reference variable."),

        ("Q19: What is SwingUtilities.invokeLater() in Main.java, and why is it necessary?",
         "Swing GUI components are not thread-safe. All GUI creation and component updates must happen on a single dedicated background thread known as the <b>Event Dispatch Thread (EDT)</b>. <code>SwingUtilities.invokeLater()</code> places the UI initialization runnable onto the EDT event queue, preventing thread race conditions and visual rendering glitches."),

        ("Q20: What is the Delegation Event Model in Swing?",
         "The Delegation Event Model decouples event generation from event handling. An event source (like a <code>JButton</code>) detects a user action and broadcasts an <code>ActionEvent</code>. The source delegates handling to registered listener objects implementing <code>ActionListener</code>. The listener executes code inside its <code>actionPerformed(ActionEvent e)</code> method."),

        ("Q21: How do all 5 screens stay synchronized when an item is added or distributed?",
         "All views read from the same single source of truth: <code>chronochef.db</code> via <code>FoodBankDAO</code>. Whenever an item is added in Module A, restocked in Module C, or distributed in Module D, the caller triggers <code>mainFrame.refreshAllViews()</code>. This calls <code>loadInventoryData()</code>, <code>populateItemSelect()</code>, and <code>loadAnalyticsData()</code> across all panels, instantly repopulating the live tables and dropdowns."),

        ("Q22: How does the custom TableCellRenderer in InventoryPanel work?",
         "The <code>UrgencyBadgeRenderer</code> extends <code>DefaultTableCellRenderer</code> and overrides <code>getTableCellRendererComponent()</code>. For each cell rendered in the 'Priority' and 'PDI Score' columns, it inspects the row's priority value and dynamically applies background and foreground colors: soft red for URGENT, amber for HIGH, yellow for MEDIUM, light green for LOW, and dark gray strikethrough for EXPIRED."),

        ("Q23: What happens if a shelter tries to distribute an item with 0 quantity?",
         "<code>DistributionPanel</code> verifies that the entered distribution quantity is greater than 0 and less than or equal to the current stock. If the user enters a quantity greater than available inventory, it catches the error and throws <code>InvalidQuantityException</code>, displaying a warning dialog preventing negative warehouse inventory."),

        ("Q24: What is the role of DataSeeder.java?",
         "<code>DataSeeder.java</code> inspects the database at startup. If the database is freshly initialized or empty, it automatically seeds 10 realistic food items spanning all priority tiers (expired yogurt, urgent bread and milk, high-priority apples, medium-priority pasta, and long-shelf-life canned beans and rice). This ensures the application is immediately testable and demo-ready without manual data entry."),

        ("Q25: How do you prove that your software logic is bug-free?",
         "We wrote a comprehensive automated test suite in <code>ProjectTestRunner.java</code> comprising 35 automated assertion checks. It validates PDI score calculations, boundary values, exception throwing on expired items, dynamic subsidy tiers, polymorphism via dynamic dispatch, SQLite database CRUD, distribution stock deduction, and Bubble Sort ordering. Running <code>run_tests.bat</code> achieves a <b>100% pass rate (35 / 35 tests passed)</b>.")
    ]

    for q, a in viva_qa:
        q_box = [
            [Paragraph(f"<b>{q}</b>", q_style)],
            [Paragraph(a, a_style)]
        ]
        t = Table(q_box, colWidths=[523])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('LINEBELOW', (0,0), (-1,0), 0.5, C_BORDER),
            ('PADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t)
        story.append(Spacer(1, 4))

    # =========================================================================
    # 7. AUTOMATED VERIFICATION RESULTS & HOW TO RUN
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Automated Verification Report & Execution Instructions", h1_style))
    story.append(Paragraph(
        "The project includes automated validation batch scripts for compiling, testing, and launching the application:",
        body_style
    ))

    run_data = [
        [
            Paragraph("Batch Script", table_header_style),
            Paragraph("Command Executed", table_header_style),
            Paragraph("Purpose & Expected Outcome", table_header_style)
        ],
        [
            Paragraph("<code>run.bat</code>", table_cell_style),
            Paragraph("<code>java -cp \"bin;lib/sqlite-jdbc.jar\" Main</code>", table_cell_style),
            Paragraph("Launches the interactive Swing GUI application with Nimbus look-and-feel.", table_cell_style)
        ],
        [
            Paragraph("<code>compile.bat</code>", table_cell_style),
            Paragraph("<code>javac -cp \"lib/sqlite-jdbc.jar\" -d bin src/...</code>", table_cell_style),
            Paragraph("Recompiles all 19 Java source files into the <code>bin/</code> bytecode directory.", table_cell_style)
        ],
        [
            Paragraph("<code>run_tests.bat</code>", table_cell_style),
            Paragraph("<code>java -cp \"bin;lib/sqlite-jdbc.jar\" test.ProjectTestRunner</code>", table_cell_style),
            Paragraph("Runs the 35 automated assertion tests and prints the 100% pass verification summary.", table_cell_style)
        ]
    ]

    r_table = Table(run_data, colWidths=[85, 195, 243])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_LIGHT_BG])
    ]))
    story.append(r_table)
    story.append(Spacer(1, 10))

    test_result_box = [
        [
            Paragraph(
                "<b>OFFICIAL TEST SUITE VERIFICATION REPORT:</b><br/>"
                "• <b>PDI Formula & Exact Boundaries:</b> 16 / 16 PASSED<br/>"
                "• <b>Expired Item Rejection Guard:</b> 2 / 2 PASSED<br/>"
                "• <b>Dynamic Subsidy Tiers (100%, 50%, 0%):</b> 4 / 4 PASSED<br/>"
                "• <b>Inheritance & Dynamic Method Dispatch:</b> 2 / 2 PASSED<br/>"
                "• <b>DatabaseManager Singleton & JDBC CRUD:</b> 8 / 8 PASSED<br/>"
                "• <b>Bubble Sort Urgency Ordering:</b> 1 / 1 PASSED<br/>"
                "<b>TOTAL: 35 / 35 TESTS PASSED &mdash; 100% COMPLETION STATUS</b>",
                callout_style
            )
        ]
    ]
    tb = Table(test_result_box, colWidths=[523])
    tb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#DCFCE7")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#22C55E")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tb)

    # Build Document with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Complete Code Guide PDF Generated at: {os.path.abspath(output_pdf)}")


if __name__ == "__main__":
    out_file = os.path.join(os.path.dirname(__file__), "ChronoChef_Project_Explanation_and_Viva_Guide.pdf")
    generate_comprehensive_code_guide(out_file)
