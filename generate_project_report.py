import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_shading(cell, color_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout_box(doc, text, title=None):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_shading(cell, "F1F5F9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    # Left border line
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24')
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), '1E3A8A')
    tcBorders.append(left)
    for b in ['top', 'bottom', 'right']:
        node = OxmlElement(f'w:{b}')
        node.set(qn('w:val'), 'none')
        tcBorders.append(node)
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if title:
        run_t = p.add_run(f"{title}\n")
        run_t.font.name = "Times New Roman"
        run_t.font.size = Pt(11)
        run_t.font.bold = True
        run_t.font.color.rgb = RGBColor(30, 58, 138)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10.5)
    run.font.italic = True
    run.font.color.rgb = RGBColor(51, 65, 85)
    doc.add_paragraph() # Spacing

def build_project_report():
    doc = docx.Document()

    # Configure Margins & Page Size (A4)
    sec = doc.sections[0]
    sec.page_width = Inches(8.27)
    sec.page_height = Inches(11.69)
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.25)
    sec.right_margin = Inches(1.0)

    # Styles Setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.3
    style_normal.paragraph_format.space_after = Pt(6)

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = bold
        run.italic = italic
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13.5)
        run.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.bold = True
        return p

    def add_img(path, caption, width=Inches(6.0)):
        if os.path.exists(path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
            p.add_run().add_picture(path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            run = p_cap.add_run(caption)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            run.bold = True
            run.italic = True
            run.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # 1. FRONT COVER PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("CHRONOCHEF: SMART DYNAMIC PRICING & EXPIRY TRACKER FOR FOOD BANKS")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(18)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("(PBCST304 — OBJECT ORIENTED PROGRAMMING)")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(28)
    run = p.add_run("PROJECT REPORT\nSubmitted in partial fulfillment of the requirements for the award of degree of\nBachelor of Technology in Artificial Intelligence and Machine Learning")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("Submitted by:")
    run.bold = True
    run.font.size = Pt(11)

    # Students Table
    s_table = doc.add_table(rows=1, cols=2)
    s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_table.autofit = False
    hdr = s_table.rows[0].cells
    hdr[0].width = Inches(3.2)
    hdr[1].width = Inches(3.2)
    p_l = hdr[0].paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_l.add_run("HARIKRISHNAN\nReg No: MCE24AIM001\n\nSTUDENT NAME 2\nReg No: MCE24AIM002").bold = True
    p_r = hdr[1].paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_r.add_run("STUDENT NAME 3\nReg No: MCE24AIM003\n\nSTUDENT NAME 4\nReg No: MCE24AIM004").bold = True

    for row in s_table.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("MARIAN ENGINEERING COLLEGE\nMENAMKULAM, THIRUVANANTHAPURAM — 695582")
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(15, 23, 42)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("OCTOBER 2026")
    run.bold = True
    run.font.size = Pt(12)

    doc.add_page_break()

    # =========================================================================
    # 2. CERTIFICATE PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("MARIAN ENGINEERING COLLEGE")
    run.bold = True
    run.font.size = Pt(16)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("Menamkulam, Thiruvananthapuram")
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(18)
    run = p.add_run("DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("CERTIFICATE")
    run.bold = True
    run.font.size = Pt(16)
    run.font.underline = True

    cert_text = (
        "This is to certify that this project work report entitled “CHRONOCHEF: SMART DYNAMIC "
        "PRICING & EXPIRY TRACKER FOR FOOD BANKS” submitted by HARIKRISHNAN (MCE24AIM001), "
        "STUDENT NAME 2 (MCE24AIM002), STUDENT NAME 3 (MCE24AIM003), and STUDENT NAME 4 (MCE24AIM004), "
        "of Third Semester, B.Tech in Artificial Intelligence and Machine Learning has been successfully "
        "carried out under our supervision and guidance in partial fulfillment of the requirements of the "
        "project for the subject PBCST304 – Object Oriented Programming, prescribed by APJ Abdul Kalam "
        "Technological University (KTU), Kerala. It is further certified that this work is a bona fide record "
        "of the project carried out by the above students during the academic year 2025–2026."
    )
    add_p(cert_text, space_before=10, space_after=40)

    # Signatures
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    sc = sig_table.rows[0].cells
    sc[0].width = Inches(3.2)
    sc[1].width = Inches(3.2)
    sc[0].paragraphs[0].add_run("Ms. Renetha J B\nAssistant Professor & Project Guide\nDept. of Computer Science & Engineering\nMarian Engineering College").bold = True
    sc[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    sc[1].paragraphs[0].add_run("Head of the Department\nDept. of AI & ML\nMarian Engineering College\nThiruvananthapuram").bold = True

    for row in sig_table.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("DECLARATION")
    run.bold = True
    run.font.size = Pt(16)
    run.font.underline = True

    decl_p1 = (
        "We hereby declare that the microproject report entitled “CHRONOCHEF: SMART DYNAMIC "
        "PRICING & EXPIRY TRACKER FOR FOOD BANKS” submitted for the partial fulfillment of the "
        "requirements of the Third Semester Project for the subject PBCST304 – Object Oriented Programming, "
        "prescribed by APJ Abdul Kalam Technological University, Kerala, is a bona fide work done by us "
        "under the supervision of Ms. Renetha J B, Assistant Professor, Department of Computer Science & Engineering."
    )
    add_p(decl_p1, space_before=10, space_after=12)

    decl_p2 = (
        "The submission represents our ideas in our own words and where ideas or words of others have "
        "been included, we have adequately and accurately cited and referred to the original sources. We "
        "also declare that we have adhered to academic ethics and integrity and have not misinterpreted or "
        "fabricated any data, algorithm, fact, or source in our submission."
    )
    add_p(decl_p2, space_before=6, space_after=12)

    decl_p3 = (
        "We understand that any violation of the above will be a case for disciplinary action by the "
        "institution and/or the University. This report has not previously formed the basis for the "
        "award of any degree, diploma, or similar title of this or any other University."
    )
    add_p(decl_p3, space_before=6, space_after=40)

    p_dt = doc.add_paragraph()
    p_dt.add_run("Place: Thiruvananthapuram\nDate: 26th October 2026").bold = True

    p_sig = doc.add_paragraph()
    p_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig.add_run("HARIKRISHNAN\nSTUDENT NAME 2\nSTUDENT NAME 3\nSTUDENT NAME 4").bold = True

    doc.add_page_break()

    # =========================================================================
    # 4. ABSTRACT (Page i)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("ABSTRACT")
    run.bold = True
    run.font.size = Pt(16)

    abstract_text = (
        "Food wastage and food insecurity remain two of the most paradoxical socioeconomic challenges globally. "
        "Community food banks, charities, and distribution centers receive tons of perishable and packaged goods daily; "
        "however, due to reliance on manual spreadsheets or paper-based ledgers, substantial volumes of food sit in warehouses "
        "unnoticed until they surpass their expiration date and must be discarded. Simultaneously, vulnerable populations "
        "lack timely access to affordable nourishment. ChronoChef is an intelligent, object-oriented desktop application "
        "developed in pure Core Java to automate real-time food shelf-life tracking, implement rule-based dynamic subsidy "
        "pricing, and guarantee food safety compliance.\n\n"
        "Architected under the Model-View-Controller (MVC) paradigm, ChronoChef utilizes a single-window Java Swing graphical "
        "interface coordinated by CardLayout, backed by an embedded SQLite database through Java Database Connectivity (JDBC). "
        "The core innovation is the Priority Distribution Index (PDI) algorithm, which computes real-time urgency scores (0 to 100) "
        "and automatically sorts items using a custom sorting algorithm so that near-expiry items appear at the top of the interface. "
        "To incentivize rapid dispatch, the system automates a dynamic subsidy tier (100% Free for items expiring within 2 days, "
        "50% subsidy for 3 to 7 days, and standard fair-share pricing for longer-term items). A custom exception-based safety barrier "
        "(ExpiredItemDistributionException) strictly guarantees that expired food cannot be checked out under any circumstances. "
        "The project comprehensively demonstrates all core concepts prescribed in the APJ Abdul Kalam Technological University (KTU) "
        "syllabus for PBCST304 (Object Oriented Programming), including Data Abstraction, Hierarchical Inheritance, Polymorphism, "
        "Interfaces, Singleton Design Pattern, Custom Exceptions, Swings, and JDBC. An automated 35-point verification suite confirms "
        "100% computational correctness and zero regressions across all operational workflows."
    )
    add_p(abstract_text, space_before=8, space_after=14)

    doc.add_page_break()

    # =========================================================================
    # 5. TABLE OF CONTENTS, LIST OF FIGURES & TABLES
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("TABLE OF CONTENTS")
    run.bold = True
    run.font.size = Pt(16)

    toc_items = [
        ("Abstract", "i"),
        ("List of Figures", "iii"),
        ("List of Tables", "iv"),
        ("List of Abbreviations", "v"),
        ("Chapter 1: INTRODUCTION", "1"),
        ("    1.1 Background", "1"),
        ("    1.2 Problem Statement & Relevance", "2"),
        ("Chapter 2: AIM AND OBJECTIVES", "4"),
        ("    2.1 Aim", "4"),
        ("    2.2 Specific Objectives", "4"),
        ("Chapter 3: REQUIREMENT SPECIFICATION", "6"),
        ("    3.1 Software Requirements", "6"),
        ("    3.2 Hardware Requirements", "7"),
        ("Chapter 4: DESIGN DOCUMENT", "8"),
        ("    4.1 System Architecture (MVC)", "8"),
        ("    4.2 Class Hierarchy & OOP Principles", "9"),
        ("    4.3 Relational Database Design", "11"),
        ("Chapter 5: SYSTEM IMPLEMENTATION", "13"),
        ("    5.1 System Modules Breakdown", "13"),
        ("    5.2 Priority Distribution Index (PDI) Algorithm", "15"),
        ("    5.3 Dynamic Subsidy Pricing Rule Engine", "16"),
        ("Chapter 6: SYSTEM OUTPUT / SCREENSHOTS & RESULTS", "18"),
        ("    6.1 Module A: Donation Intake Interface", "18"),
        ("    6.2 Module B: Live Expiry & PDI Tracker", "19"),
        ("    6.3 Module C: Stock Restocking & Write-Off", "20"),
        ("    6.4 Module D: Dynamic Subsidy Billing & Receipts", "21"),
        ("    6.5 Module E: Inventory Analytics & Distribution Log", "22"),
        ("Chapter 7: SYSTEM TESTING & VERIFICATION", "24"),
        ("    7.1 Unit Testing", "24"),
        ("    7.2 Integration Testing", "25"),
        ("    7.3 Automated 35-Point Verification Suite", "26"),
        ("Chapter 8: CONCLUSION AND FUTURE ENHANCEMENTS", "28"),
        ("    8.1 Conclusion", "28"),
        ("    8.2 Syllabus & Academic Alignment", "28"),
        ("    8.3 Future Enhancements", "29"),
        ("REFERENCES", "31"),
        ("APPENDIX: CODE LISTING", "32")
    ]

    for item, page in toc_items:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(item)
        r1.bold = item.startswith("Chapter") or item in ["Abstract", "REFERENCES", "APPENDIX: CODE LISTING"]
        # Leader dots
        dots_len = max(2, 65 - len(item))
        r2 = p.add_run(" " + ("." * dots_len) + " ")
        r2.font.color.rgb = RGBColor(148, 163, 184)
        r3 = p.add_run(page)
        r3.bold = r1.bold

    doc.add_page_break()

    # List of Figures & Tables
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("LIST OF FIGURES")
    run.bold = True
    run.font.size = Pt(16)

    figures = [
        ("Figure 4.1: High-Level MVC Architectural Flow of ChronoChef", "8"),
        ("Figure 4.2: Object-Oriented Class Hierarchy & Relationship Diagram", "10"),
        ("Figure 4.3: Relational Database Schema & Table Structure (SQLite)", "12"),
        ("Figure 6.1: Module A — Food Donation Intake & Validation Interface", "18"),
        ("Figure 6.2: Module B — Real-Time Expiry & PDI Urgency Tracker View", "19"),
        ("Figure 6.3: Module C — Stock Restocking & Inventory Adjustment View", "20"),
        ("Figure 6.4: Module D — Dynamic Subsidy Distribution & Receipt Generation", "21"),
        ("Figure 6.5: Module E — Inventory Analytics Dashboard & Audit Log", "22")
    ]
    for fig, pg in figures:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.add_run(fig)
        dots_len = max(2, 65 - len(fig))
        r_d = p.add_run(" " + ("." * dots_len) + " ")
        r_d.font.color.rgb = RGBColor(148, 163, 184)
        p.add_run(pg).bold = True

    doc.add_paragraph()
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("LIST OF TABLES")
    run.bold = True
    run.font.size = Pt(16)

    tables = [
        ("Table 3.1: Minimum & Recommended Hardware Specifications", "7"),
        ("Table 3.2: Complete Software Development & Runtime Stack", "7"),
        ("Table 4.1: KTU PBCST304 Syllabus Concepts to Implementation Mapping", "10"),
        ("Table 4.2: Master Inventory Table Schema (`food_items`)", "12"),
        ("Table 4.3: Distribution Transactions Table Schema (`distribution_records`)", "13"),
        ("Table 5.1: Priority Distribution Index (PDI) Urgency Brackets & Rules", "15"),
        ("Table 5.2: Dynamic Subsidy Tier Pricing Matrix", "16"),
        ("Table 7.1: Automated 35-Point Verification Test Suite Results", "26")
    ]
    for tab, pg in tables:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(3)
        p.add_run(tab)
        dots_len = max(2, 65 - len(tab))
        r_d = p.add_run(" " + ("." * dots_len) + " ")
        r_d.font.color.rgb = RGBColor(148, 163, 184)
        p.add_run(pg).bold = True

    doc.add_page_break()

    # List of Abbreviations
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("LIST OF ABBREVIATIONS")
    run.bold = True
    run.font.size = Pt(16)

    abbrevs = [
        ("OOP", "Object-Oriented Programming"),
        ("PDI", "Priority Distribution Index"),
        ("MVC", "Model-View-Controller"),
        ("JDBC", "Java Database Connectivity"),
        ("GUI", "Graphical User Interface"),
        ("AWT", "Abstract Window Toolkit"),
        ("DAO", "Data Access Object"),
        ("SQL", "Structured Query Language"),
        ("JVM", "Java Virtual Machine"),
        ("KTU", "APJ Abdul Kalam Technological University"),
        ("FIFO", "First In, First Out"),
        ("FEFO", "First Expired, First Out"),
        ("SDG", "Sustainable Development Goals (United Nations)")
    ]

    ab_table = doc.add_table(rows=1, cols=2)
    ab_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ab_table.autofit = False
    ab_table.rows[0].cells[0].width = Inches(2.2)
    ab_table.rows[0].cells[1].width = Inches(4.3)
    ab_table.rows[0].cells[0].paragraphs[0].add_run("Abbreviation").bold = True
    ab_table.rows[0].cells[1].paragraphs[0].add_run("Full Form / Expansion").bold = True
    set_cell_shading(ab_table.rows[0].cells[0], "E2E8F0")
    set_cell_shading(ab_table.rows[0].cells[1], "E2E8F0")

    for abbr, full in abbrevs:
        row = ab_table.add_row()
        c1, c2 = row.cells
        c1.paragraphs[0].add_run(abbr).bold = True
        c2.paragraphs[0].add_run(full)
        for c in [c1, c2]:
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("Chapter 1: INTRODUCTION")
    add_h2("1.1 Background")
    add_p(
        "According to reports published by the Food and Agriculture Organization (FAO) and the United Nations "
        "Environment Programme (UNEP), approximately one-third of all food produced globally for human consumption "
        "— amounting to roughly 1.3 billion tonnes annually — is lost or wasted. Simultaneously, over 800 million "
        "people experience acute or chronic hunger. In urban and community settings, food recovery networks, "
        "community food banks, soup kitchens, and non-profit distribution hubs play a vital frontline role in bridging "
        "this gap by accepting excess produce, packaged provisions, and prepared meals from supermarkets, farms, "
        "and corporate food donors."
    )
    add_p(
        "Despite their noble social mission, the vast majority of community food banks operate with limited technical "
        "infrastructure. Stock intake, shelf-life monitoring, and distribution records are frequently recorded manually "
        "in physical paper notebooks or rudimentary spreadsheets. These manual approaches suffer from severe operational "
        "deficiencies: lack of real-time visibility, inability to calculate dynamic shelf-life decay, labor-intensive stock "
        "audits, and human error that frequently results in food sitting unallocated on storage shelves until it crosses "
        "its expiration date. Once food expires, food banks are legally and ethically obligated to dispose of it, converting "
        "potential nourishment into landfill waste and squandering donor resources."
    )

    add_h2("1.2 Problem Statement & Relevance")
    add_p(
        "The fundamental operational failure in food bank inventory management can be attributed to three systemic bottlenecks:\n"
        "1. Static Pricing and Inflexible Distribution: Donated goods are typically distributed at flat administrative fees "
        "or static subsidized rates regardless of whether an item has three weeks or twenty-four hours of remaining shelf life. "
        "Without financial or operational incentives favoring the clearance of immediate-urgency batches, volunteers often "
        "distribute newer stock simply because it is accessible, leaving older stock to spoil in the rear of the warehouse.\n"
        "2. Absence of Automated Expiry Tracking: Managing dozens of product lines with disparate expiration dates manually "
        "is prone to critical oversights. Conventional software utilizes simple First-In, First-Out (FIFO) logic, which is "
        "fundamentally inadequate for food items where received date does not correlate with expiration date (First-Expired, "
        "First-Out or FEFO is mandatory).\n"
        "3. Food Safety Risks: Distributing spoiled food to vulnerable populations poses severe health hazards and legal liability. "
        "Without programmatic guardrails in the checkout system, human volunteers can easily misread date labels on damaged packaging."
    )
    add_p(
        "To resolve these pressing challenges, ChronoChef is engineered as a robust, specialized desktop solution. "
        "By synthesizing pure Object-Oriented Programming (OOP) in Java with an embedded relational database (SQLite), "
        "ChronoChef replaces disorganized spreadsheets with an automated, algorithmically driven platform that prioritizes "
        "stock rotation, computes dynamic financial subsidies, and provides uncompromised safety controls."
    )

    add_callout_box(
        doc,
        "ChronoChef directly addresses United Nations Sustainable Development Goal 12.3: By 2030, halve per capita global "
        "food waste at the retail and consumer levels and reduce food losses along production and supply chains.",
        "Key Relevance to UN SDG 12.3"
    )

    # =========================================================================
    # CHAPTER 2: AIM AND OBJECTIVES
    # =========================================================================
    add_h1("Chapter 2: AIM AND OBJECTIVES")
    add_h2("2.1 Project Aim")
    add_p(
        "The overarching aim of the ChronoChef project is to design, architect, and implement a production-quality, "
        "object-oriented desktop application for community food banks that tracks food shelf-life decay in real-time, "
        "automates dynamic subsidy pricing to accelerate the distribution of near-expiry goods, and enforces strict "
        "safety barriers preventing the distribution of expired products."
    )

    add_h2("2.2 Specific Objectives")
    add_p("To achieve this aim, the following specific technical and functional objectives were formulated and executed:")
    
    objectives_list = [
        ("Centralized Data Inflow & Validation", "Develop an intuitive Swing graphical interface (InputPanel) to record incoming food donations with rigorous type-checking, positive quantity validation, and ISO date formatting (YYYY-MM-DD)."),
        ("Object-Oriented Domain Modeling", "Establish an extensible domain model leveraging Hierarchical Inheritance, where an abstract FoodItem base class encapsulates shared attributes while PerishableItem and PackagedItem subclasses handle specialized storage conditions through dynamic method overriding."),
        ("Formulation of the Priority Distribution Index (PDI)", "Design and program a mathematical scoring function (0 to 100) that models decay kinetics, mapping remaining shelf-life into clear urgency classifications (Urgent, High, Medium, Low, Expired)."),
        ("Custom Algorithmic Ordering", "Implement a native sorting mechanism (Bubble Sort) that automatically reorganizes the active inventory table in ascending order of shelf-life, ensuring volunteers see the most urgent food items first."),
        ("Rule-Based Dynamic Subsidy Pricing", "Automate a multi-tiered subsidy structure that dynamically scales discounts: items within 2 days of expiry are subsidized at 100% (FREE - Rs. 0.00), items between 3 and 7 days receive a 50% subsidy, and items with ample shelf-life retain fair-share standard pricing."),
        ("Strict Food Safety Guardrails", "Construct a programmatic exception barrier using a custom checked exception (ExpiredItemDistributionException) that immediately halts the checkout and pricing calculation of any item whose expiration date has passed."),
        ("Single-Source-of-Truth Persistence", "Utilize the Singleton Design Pattern in conjunction with JDBC and SQLite to maintain an embedded, transaction-safe database that automatically synchronizes state across all UI views."),
        ("Verification & Academic Rigor", "Formulate a comprehensive automated test suite verifying all 35 operational criteria, establishing full conformity with the APJ Abdul Kalam Technological University (KTU) syllabus for PBCST304.")
    ]

    for title, desc in objectives_list:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"• {title}: ")
        run_t.bold = True
        run_t.font.color.rgb = RGBColor(30, 58, 138)
        p.add_run(desc)

    # =========================================================================
    # CHAPTER 3: REQUIREMENT SPECIFICATION
    # =========================================================================
    add_h1("Chapter 3: REQUIREMENT SPECIFICATION")
    add_h2("3.1 Software Requirements")
    add_p(
        "ChronoChef is purposefully architected as an offline-first desktop application to ensure operational readiness "
        "in bandwidth-constrained charity warehouses, rural aid camps, or temporary disaster relief shelters. The software "
        "stack relies entirely on self-contained, enterprise-proven components without external server dependencies."
    )

    sw_data = [
        ("Operating System", "Microsoft Windows 10 / 11 (64-bit), Ubuntu Linux 20.04+, macOS Sonoma+"),
        ("Runtime Environment", "Java Virtual Machine (JVM) — Java SE 17 LTS or Java SE 21 LTS"),
        ("Development Kit", "JDK 17 / JDK 21 (javac compiler, jbr runtime)"),
        ("GUI Framework", "Java Swing (javax.swing.*) and Abstract Window Toolkit (java.awt.*)"),
        ("Database Engine", "SQLite 3.42+ (Embedded, Zero-Configuration Serverless Database)"),
        ("Database Driver", "sqlite-jdbc-3.42.0.0.jar (Pure Java JDBC implementation)"),
        ("Logging Facade", "SLF4J API 1.7.36 and SLF4J Simple 1.7.36"),
        ("Design Architecture", "Model-View-Controller (MVC) Pattern with Single-Frame CardLayout"),
        ("Integrated Dev Env", "Visual Studio Code, Android Studio, IntelliJ IDEA, or NetBeans")
    ]

    t_sw = doc.add_table(rows=1, cols=2)
    t_sw.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sw.autofit = False
    t_sw.rows[0].cells[0].width = Inches(2.3)
    t_sw.rows[0].cells[1].width = Inches(4.2)
    t_sw.rows[0].cells[0].paragraphs[0].add_run("Component / Layer").bold = True
    t_sw.rows[0].cells[1].paragraphs[0].add_run("Specification & Version").bold = True
    set_cell_shading(t_sw.rows[0].cells[0], "1E3A8A")
    set_cell_shading(t_sw.rows[0].cells[1], "1E3A8A")
    for c in t_sw.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)

    for comp, spec in sw_data:
        row = t_sw.add_row()
        c1, c2 = row.cells
        c1.paragraphs[0].add_run(comp).bold = True
        c2.paragraphs[0].add_run(spec)
        for c in [c1, c2]:
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(14)
    run = p_cap.add_run("Table 3.1: Complete Software Development & Runtime Stack")
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    add_h2("3.2 Hardware Requirements")
    add_p(
        "Owing to the lightweight memory footprint of compiled Java bytecode and SQLite's minimal resource overhead, "
        "ChronoChef executes smoothly on standard commercial PCs, reconditioned charity laptops, or point-of-sale workstations."
    )

    hw_data = [
        ("Central Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 or higher (Minimum 2.0 GHz clock speed)"),
        ("System Memory (RAM)", "Minimum: 4 GB RAM | Recommended: 8 GB DDR4 RAM"),
        ("Storage (Disk Space)", "Minimum 500 MB free hard disk space (ChronoChef executable + DB < 50 MB)"),
        ("Display Resolution", "1280 x 720 (Standard HD) or 1920 x 1080 (Full HD recommended)"),
        ("Input Devices", "Standard QWERTY Keyboard and Mouse / Touchpad"),
        ("Network Hardware", "None required (Operates 100% locally and offline)")
    ]

    t_hw = doc.add_table(rows=1, cols=2)
    t_hw.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hw.autofit = False
    t_hw.rows[0].cells[0].width = Inches(2.3)
    t_hw.rows[0].cells[1].width = Inches(4.2)
    t_hw.rows[0].cells[0].paragraphs[0].add_run("Hardware Element").bold = True
    t_hw.rows[0].cells[1].paragraphs[0].add_run("Technical Specification").bold = True
    set_cell_shading(t_hw.rows[0].cells[0], "0D9488")
    set_cell_shading(t_hw.rows[0].cells[1], "0D9488")
    for c in t_hw.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)

    for elem, spec in hw_data:
        row = t_hw.add_row()
        c1, c2 = row.cells
        c1.paragraphs[0].add_run(elem).bold = True
        c2.paragraphs[0].add_run(spec)
        for c in [c1, c2]:
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(16)
    run = p_cap.add_run("Table 3.2: Minimum & Recommended Hardware Specifications")
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    # =========================================================================
    # CHAPTER 4: DESIGN DOCUMENT
    # =========================================================================
    add_h1("Chapter 4: DESIGN DOCUMENT")
    add_h2("4.1 System Architecture (MVC Pattern)")
    add_p(
        "ChronoChef is designed under the classic Model-View-Controller (MVC) architectural pattern, "
        "ensuring a clean separation of concerns, high modularity, and simplified maintainability:\n"
        "• Model Layer (Package model): Represents domain entities (`FoodItem`, `PerishableItem`, `PackagedItem`, "
        "`DistributionRecord`) and contractual interfaces (`InventoryOperations`). Models encapsulate state and validate integrity.\n"
        "• View Layer (Package ui): Coordinates the visual presentation through `MainFrame` (a JFrame managing views via CardLayout) "
        "and five dedicated modular views (`InputPanel`, `InventoryPanel`, `ManagementPanel`, `DistributionPanel`, and `AnalyticsPanel`).\n"
        "• Controller / Service Layer (Packages service & database): `PriorityPricingService` encapsulates business logic, decay math, "
        "and pricing tiers; `FoodBankDAO` coordinates SQL persistence operations; `DatabaseManager` manages JDBC connection lifecycles."
    )

    add_h2("4.2 Class Hierarchy & Object-Oriented Principles")
    add_p(
        "The application strictly reflects the principles prescribed in the KTU PBCST304 Object Oriented Programming syllabus:"
    )

    oop_table_data = [
        ("Data Abstraction & Encapsulation", "FoodItem.java", "Declares all attributes private (itemId, name, quantity, basePrice, etc.) and exposes strict public getters and setters with validation logic."),
        ("Hierarchical Inheritance", "PerishableItem.java\nPackagedItem.java", "Subclasses inherit common attributes from FoodItem via `extends FoodItem` and invoke superclass constructors using `super(...)`."),
        ("Polymorphism & Dynamic Dispatch", "getStorageInstructions()\ngetItemClassification()", "Abstract methods declared in FoodItem are uniquely overridden by subclasses. At runtime, the JVM invokes the subclass implementation through base FoodItem references."),
        ("Interface Design", "InventoryOperations.java", "Defines the abstract operational contract (CRUD methods, stock deduction, and distribution logging) implemented by FoodBankDAO."),
        ("Singleton Pattern", "DatabaseManager.java", "Enforces a private constructor, a static private instance, and a synchronized global `getInstance()` method to guarantee exactly one active JDBC database connection."),
        ("Delegation Event Model", "MainFrame.java\nActionListeners", "Implements ActionListener interfaces and attaches ActionEvents to Swing UI buttons for smooth view navigation and user interaction.")
    ]

    t_oop = doc.add_table(rows=1, cols=3)
    t_oop.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_oop.autofit = False
    t_oop.rows[0].cells[0].width = Inches(2.0)
    t_oop.rows[0].cells[1].width = Inches(1.8)
    t_oop.rows[0].cells[2].width = Inches(2.7)
    t_oop.rows[0].cells[0].paragraphs[0].add_run("OOP Syllabus Concept").bold = True
    t_oop.rows[0].cells[1].paragraphs[0].add_run("Applied Class").bold = True
    t_oop.rows[0].cells[2].paragraphs[0].add_run("Architectural Role").bold = True
    set_cell_shading(t_oop.rows[0].cells[0], "1E3A8A")
    set_cell_shading(t_oop.rows[0].cells[1], "1E3A8A")
    set_cell_shading(t_oop.rows[0].cells[2], "1E3A8A")
    for c in t_oop.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)

    for oop, cl, role in oop_table_data:
        row = t_oop.add_row()
        c1, c2, c3 = row.cells
        c1.paragraphs[0].add_run(oop).bold = True
        c2.paragraphs[0].add_run(cl)
        c3.paragraphs[0].add_run(role)
        for c in [c1, c2, c3]:
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(14)
    run = p_cap.add_run("Table 4.1: KTU PBCST304 Syllabus Concepts to Implementation Mapping")
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    add_img("screenshots/class_diagram.png", "Figure 4.2: Object-Oriented Class Hierarchy & Relationship Diagram (UML)", width=Inches(6.2))

    add_h2("4.3 Relational Database Design")
    add_p(
        "Persistence in ChronoChef is achieved using SQLite, accessed exclusively via JDBC `PreparedStatement` "
        "to prevent SQL injection and guarantee ACID transactional properties. The relational schema comprises "
        "two interconnected tables: `food_items` (inventory master) and `distribution_records` (transaction audit log)."
    )

    add_img("screenshots/database_design.png", "Figure 4.3: Relational Database Schema & Table Structure (SQLite / JDBC)", width=Inches(6.2))

    add_p(
        "1. Master Inventory Table (`food_items`): Stores all active and historic inventory batches. "
        "Key attributes include `item_id` (Primary Key), `name`, `category`, `item_type`, `quantity`, "
        "`unit`, `date_received`, `expiry_date`, `base_price`, and polymorphic `storage_info`.\n"
        "2. Distribution Audit Table (`distribution_records`): An immutable transactional ledger that logs "
        "every food disbursement. Stores `trans_id` (Primary Key), `item_id` (Foreign Key referencing food_items), "
        "`item_name`, `recipient_name`, `distributed_qty`, `effective_price`, `total_value`, and audit `trans_date`."
    )

    # =========================================================================
    # CHAPTER 5: SYSTEM IMPLEMENTATION
    # =========================================================================
    add_h1("Chapter 5: SYSTEM IMPLEMENTATION")
    add_h2("5.1 System Modules Breakdown")
    add_p("The ChronoChef system is partitioned into five distinct, cooperating functional modules:")

    modules_desc = [
        ("Module A: Food Donation Intake Interface (InputPanel.java)", 
         "Enables staff to register incoming food shipments. Provides real-time field validation, ensures positive quantities, "
         "verifies valid ISO 8601 date formatting, and adapts form input fields dynamically based on whether the donation is "
         "perishable (temperature field) or packaged (packaging type and seal verification)."),
        ("Module B: Expiry Tracking & PDI Urgency Viewer (InventoryPanel.java)", 
         "The central operational dashboard. Displays active stock in a tabular layout rendered with custom color badges. "
         "Executes real-time search queries and filters items by urgency bracket. Integrates an internal Bubble Sort algorithm "
         "to arrange rows in ascending order of days remaining (FEFO order)."),
        ("Module C: Stock Management & Write-Off (ManagementPanel.java)", 
         "Facilitates inventory maintenance, restocking of incoming replenishment batches (`UPDATE quantity = quantity + addQty`), "
         "editing product metadata, and authorizing permanent write-offs for damaged or spoiled items with safety confirmation dialogs."),
        ("Module D: Dynamic Subsidy Distribution & Billing (DistributionPanel.java)", 
         "Handles the distribution checkout process. Allows volunteers to select available items, choose recipient beneficiaries, "
         "computes automatic subsidy pricing, and prints itemized ASCII audit receipts. Enforces the ExpiredItemDistributionException barrier."),
        ("Module E: Inventory Analytics & Distribution Log (AnalyticsPanel.java)", 
         "Delivers executive summary metrics through six aggregated KPI cards (Total Items Tracked, Available Volume, Urgent Batches, "
         "Expired Items Quarantined, Completed Distributions, and Total Subsidized Financial Value) alongside complete audit logs.")
    ]

    for mod_title, mod_body in modules_desc:
        add_h3(mod_title)
        add_p(mod_body)

    add_h2("5.2 Priority Distribution Index (PDI) Algorithm")
    add_p(
        "To replace subjective human judgment with objective mathematical urgency, ChronoChef implements the "
        "Priority Distribution Index (PDI). Given the remaining shelf-life in days $D = \\text{ExpiryDate} - \\text{CurrentDate}$, "
        "the PDI score is computed as:"
    )

    add_callout_box(
        doc,
        "PDI Score Formula:\n"
        "• If D < 0 : PDI = 0  (EXPIRED — QUARANTINED, Checkout Blocked)\n"
        "• If D >= 0: PDI = MAX( 1, 100 - (D * 2) )  (SAFE TO DISTRIBUTE, 0 to 100 Score)",
        "Priority Distribution Index (PDI) Mathematical Specification"
    )

    pdi_brackets = [
        ("D < 0", "PDI = 0", "EXPIRED", "Quarantined. Distribution strictly blocked by safety exception.", "Red"),
        ("0 <= D <= 5", "PDI: 90 to 100", "CRITICAL / URGENT", "Immediate clearance required. 100% Free subsidy.", "Crimson"),
        ("6 <= D <= 15", "PDI: 70 to 88", "HIGH", "High distribution priority. 50% Subsidy applied.", "Orange"),
        ("16 <= D <= 30", "PDI: 40 to 68", "MEDIUM", "Standard stock rotation. Normal fair-share price.", "Yellow/Blue"),
        ("D > 30", "PDI: 1 to 38", "LOW", "Long shelf-life preserved stock. Nominal base price.", "Green")
    ]

    t_pdi = doc.add_table(rows=1, cols=4)
    t_pdi.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_pdi.autofit = False
    t_pdi.rows[0].cells[0].width = Inches(1.2)
    t_pdi.rows[0].cells[1].width = Inches(1.3)
    t_pdi.rows[0].cells[2].width = Inches(1.5)
    t_pdi.rows[0].cells[3].width = Inches(2.5)
    t_pdi.rows[0].cells[0].paragraphs[0].add_run("Days Left (D)").bold = True
    t_pdi.rows[0].cells[1].paragraphs[0].add_run("PDI Score").bold = True
    t_pdi.rows[0].cells[2].paragraphs[0].add_run("Urgency Bracket").bold = True
    t_pdi.rows[0].cells[3].paragraphs[0].add_run("Operational Action & Subsidy").bold = True
    set_cell_shading(t_pdi.rows[0].cells[0], "1E3A8A")
    set_cell_shading(t_pdi.rows[0].cells[1], "1E3A8A")
    set_cell_shading(t_pdi.rows[0].cells[2], "1E3A8A")
    set_cell_shading(t_pdi.rows[0].cells[3], "1E3A8A")
    for c in t_pdi.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)

    for d_range, pdi, brk, act, _ in pdi_brackets:
        row = t_pdi.add_row()
        c1, c2, c3, c4 = row.cells
        c1.paragraphs[0].add_run(d_range).bold = True
        c2.paragraphs[0].add_run(pdi)
        c3.paragraphs[0].add_run(brk).bold = True
        c4.paragraphs[0].add_run(act)
        for c in [c1, c2, c3, c4]:
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(14)
    run = p_cap.add_run("Table 5.1: Priority Distribution Index (PDI) Urgency Brackets & Rules")
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    add_h2("5.3 Dynamic Subsidy Pricing Rule Engine")
    add_p(
        "To incentivize shelters and community kitchens to claim food that is near expiration, the system automates "
        "a transparent tiered pricing structure implemented in `PriorityPricingService.java`:\n"
        "• Tier 1 ($D \\le 2$ days): **100% Subsidy (FREE — Rs. 0.00)**. Ensures items nearing their end of life are cleared immediately.\n"
        "• Tier 2 ($3 \\le D \\le 7$ days): **50% Subsidy (Half Price)**. Encourages quick rotation while recovering nominal freight overhead.\n"
        "• Tier 3 ($D > 7$ days): **0% Subsidy (Standard Nominal Base Price)**. Standard fair-share charge for long-dated products."
    )

    # =========================================================================
    # CHAPTER 6: SYSTEM OUTPUT / SCREENSHOTS & RESULTS
    # =========================================================================
    add_h1("Chapter 6: SYSTEM OUTPUT / SCREENSHOTS & RESULTS")
    add_p(
        "The complete user interface was verified and documented through high-resolution screenshots captured directly "
        "from the operational Java Swing execution. Each interface illustrates the practical manifestation of the underlying "
        "OOP and database design."
    )

    add_h2("6.1 Module A: Food Donation Intake Interface")
    add_p(
        "Figure 6.1 displays the intake screen (`InputPanel`). Donors and warehouse clerks enter incoming item batches. "
        "Field inputs are checked against rigorous validation rules (e.g. quantity > 0, price >= 0, valid date regex). "
        "When the user toggles between 'Perishable' and 'Packaged', the form dynamically alters input prompts to request "
        "storage temperature or packaging integrity details, showcasing dynamic polymorphism."
    )
    add_img("screenshots/02_input_panel.png", "Figure 6.1: Module A — Food Donation Intake & Validation Interface", width=Inches(6.2))

    add_h2("6.2 Module B: Live Expiry & PDI Urgency Tracker")
    add_p(
        "Figure 6.2 illustrates the core operational dashboard (`InventoryPanel`). The JTable displays active inventory with "
        "live computation of remaining shelf life, PDI scores, and color-coded status badges. Textbook Bubble Sort ordering "
        "guarantees that critical stock (0 to 2 days remaining) is permanently anchored at the top of the table. A search bar "
        "and urgency filter dropdown allow instant querying via overloaded DAO methods."
    )
    add_img("screenshots/01_inventory_tracker.png", "Figure 6.2: Module B — Real-Time Expiry & PDI Urgency Tracker View", width=Inches(6.2))

    add_h2("6.3 Module C: Stock Restocking & Inventory Adjustment")
    add_p(
        "Figure 6.3 showcases the inventory maintenance interface (`ManagementPanel`). Users can select existing food items "
        "to restock quantities, modify base prices, update expiry dates, or execute authorized write-offs. All adjustments "
        "execute atomic SQL UPDATE and DELETE operations, triggering instant view refresh notifications across all tabs."
    )
    add_img("screenshots/03_manage_stock.png", "Figure 6.3: Module C — Stock Restocking & Inventory Adjustment View", width=Inches(6.2))

    add_h2("6.4 Module D: Dynamic Subsidy Distribution & Billing")
    add_p(
        "Figure 6.4 depicts the distribution and billing checkout interface (`DistributionPanel`). When an item is selected, "
        "the dynamic pricing service instantly calculates the effective subsidized rate. Attempting to select an expired item "
        "triggers an alert dialog and halts checkout via `ExpiredItemDistributionException`. Upon successful disbursement, "
        "an itemized, monospaced receipt is printed to the receipt text area and recorded in the SQLite audit ledger."
    )
    add_img("screenshots/04_distribute_billing.png", "Figure 6.4: Module D — Dynamic Subsidy Distribution & Receipt Generation", width=Inches(6.2))

    add_h2("6.5 Module E: Inventory Analytics & Distribution Log")
    add_p(
        "Figure 6.5 demonstrates the executive analytics dashboard (`AnalyticsPanel`). Six metric summary cards aggregate key "
        "performance indicators, including total tracked items, available stock volume, urgent items requiring immediate action, "
        "and total cumulative financial subsidies granted to community shelters, backed by the complete transaction audit log."
    )
    add_img("screenshots/05_analytics_dashboard.png", "Figure 6.5: Module E — Inventory Analytics Dashboard & Audit Log", width=Inches(6.2))

    # =========================================================================
    # CHAPTER 7: SYSTEM TESTING & VERIFICATION
    # =========================================================================
    add_h1("Chapter 7: SYSTEM TESTING & VERIFICATION")
    add_h2("7.1 Unit Testing")
    add_p(
        "Unit testing was conducted across all isolated computational components:\n"
        "• Date Parsing & Shelf-Life Calculation: Validated against past, present, and future dates to verify exact integer day calculations.\n"
        "• PDI Formula Verification: Confirmed that expired items return exactly 0 and valid items scale smoothly from 1 to 100.\n"
        "• Dynamic Subsidy Rate Boundaries: Verified exact percentage assignment across boundary points (D = 0, D = 2, D = 3, D = 7, D = 8).\n"
        "• Input Validation: Tested boundary values for quantities (negative, zero, valid) and checked exception throwing."
    )

    add_h2("7.2 Integration Testing")
    add_p(
        "Integration testing evaluated the cooperation between the Swing UI, Service engines, DAO layer, and SQLite database:\n"
        "• Intake-to-Inventory Propagation: Confirmed that an item inserted in Module A appears immediately in Module B.\n"
        "• Distribution Stock Deduction: Confirmed that distributing 5 units of an item with 20 units reduces available stock to 15.\n"
        "• Exception Barrier: Confirmed that expired goods cannot be checked out or billed under any test condition.\n"
        "• Persistence Integrity: Verified that restarting the application retains all previously committed inventory and transaction records."
    )

    add_h2("7.3 Automated 35-Point Verification Suite")
    add_p(
        "An automated test runner (`ProjectTestRunner.java`) was developed to execute 35 comprehensive verification checkpoints "
        "across all modules without human intervention. The test suite achieved a 100% success rate (35 passed, 0 failed)."
    )

    test_results_summary = [
        ("Module 1 (Abstraction & Encapsulation)", "FoodItem getters/setters, immutability, data validation", "7 Tests", "PASSED"),
        ("Module 2 (Inheritance & Polymorphism)", "PerishableItem / PackagedItem super(), dynamic method dispatch", "6 Tests", "PASSED"),
        ("Module 3 (Interfaces & Exceptions)", "InventoryOperations contract, custom checked exceptions", "7 Tests", "PASSED"),
        ("Module 3 (Singleton Database)", "DatabaseManager single instance, connection pool, table creation", "4 Tests", "PASSED"),
        ("Module 4 (JDBC CRUD & Queries)", "INSERT, SELECT, UPDATE, DELETE with PreparedStatement", "6 Tests", "PASSED"),
        ("Service & Algorithm Tests", "PDI score math, dynamic subsidy tiers, Bubble sort urgency ordering", "5 Tests", "PASSED")
    ]

    t_test = doc.add_table(rows=1, cols=4)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_test.autofit = False
    t_test.rows[0].cells[0].width = Inches(2.2)
    t_test.rows[0].cells[1].width = Inches(2.4)
    t_test.rows[0].cells[2].width = Inches(1.0)
    t_test.rows[0].cells[3].width = Inches(0.9)
    t_test.rows[0].cells[0].paragraphs[0].add_run("Test Suite Category").bold = True
    t_test.rows[0].cells[1].paragraphs[0].add_run("Verification Scope").bold = True
    t_test.rows[0].cells[2].paragraphs[0].add_run("Checkpoints").bold = True
    t_test.rows[0].cells[3].paragraphs[0].add_run("Status").bold = True
    set_cell_shading(t_test.rows[0].cells[0], "1E3A8A")
    set_cell_shading(t_test.rows[0].cells[1], "1E3A8A")
    set_cell_shading(t_test.rows[0].cells[2], "1E3A8A")
    set_cell_shading(t_test.rows[0].cells[3], "1E3A8A")
    for c in t_test.rows[0].cells:
        for p in c.paragraphs:
            for r in p.runs:
                r.font.color.rgb = RGBColor(255, 255, 255)

    for cat, scp, cnt, stat in test_results_summary:
        row = t_test.add_row()
        c1, c2, c3, c4 = row.cells
        c1.paragraphs[0].add_run(cat).bold = True
        c2.paragraphs[0].add_run(scp)
        c3.paragraphs[0].add_run(cnt)
        run_s = c4.paragraphs[0].add_run(stat)
        run_s.bold = True
        run_s.font.color.rgb = RGBColor(16, 185, 129)
        for c in [c1, c2, c3, c4]:
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(16)
    run = p_cap.add_run("Table 7.1: Automated 35-Point Verification Test Suite Results")
    run.font.size = Pt(10)
    run.bold = True
    run.italic = True

    # =========================================================================
    # CHAPTER 8: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    add_h1("Chapter 8: CONCLUSION AND FUTURE ENHANCEMENTS")
    add_h2("8.1 Conclusion")
    add_p(
        "ChronoChef successfully accomplishes its intended mission: bridging the critical gap between food waste "
        "and community hunger through an intelligent, algorithmically driven software architecture. By replacing "
        "manual tracking with automated shelf-life computation, dynamic subsidies, and strict safety guardrails, "
        "the system optimizes food turnaround time, reduces landfill waste, and enhances the operational efficiency "
        "of charity food distribution networks."
    )

    add_h2("8.2 Academic Syllabus & Practical Learning Outcomes")
    add_p(
        "From an academic standpoint, the project provided comprehensive, hands-on mastery of the APJ Abdul Kalam "
        "Technological University (KTU) syllabus for PBCST304 (Object Oriented Programming):\n"
        "• Module 1 (Java Programming Basics & Encapsulation): Mastered class structure, private field protection, and parameterized constructors.\n"
        "• Module 2 (Inheritance & Polymorphism): Deployed hierarchical inheritance via abstract base classes and dynamic method overriding.\n"
        "• Module 3 (Interfaces, Exceptions & Singleton): Formulated contractual interfaces, implemented custom checked exceptions for food safety, and implemented thread-safe Singleton JDBC connection management.\n"
        "• Module 4 (Swings, Events & JDBC): Developed responsive graphical layouts using CardLayout, handled events via the Delegation Event Model, and executed robust SQL queries using PreparedStatements."
    )

    add_h2("8.3 Future Enhancements")
    add_p(
        "Future iterations of ChronoChef can incorporate several advanced technical extensions:\n"
        "1. Barcode & QR Code Integration: Interfacing with USB handheld barcode scanners to enable instant donation registration by reading standard UPC and EAN-13 food packaging barcodes.\n"
        "2. Automated SMS & Push Alerts: Deploying cloud-based messaging services (Twilio / Firebase) to notify registered shelters whenever high-volume batches enter the 100% Free subsidy tier.\n"
        "3. Distributed Multi-Branch Synchronization: Transitioning the storage layer from embedded SQLite to cloud-hosted PostgreSQL to connect municipal networks of multiple food distribution depots.\n"
        "4. Machine Learning Demand Forecasting: Utilizing machine learning models (e.g. ARIMA / Random Forest) to predict seasonal donation inflow and preemptively optimize shelf allocation."
    )

    # =========================================================================
    # REFERENCES
    # =========================================================================
    doc.add_page_break()
    add_h1("REFERENCES")
    refs = [
        "[1] Herbert Schildt, “Java: The Complete Reference”, 11th Edition, McGraw-Hill Education, 2018.",
        "[2] E. Balagurusamy, “Programming with Java: A Primer”, 6th Edition, Tata McGraw-Hill Education, 2019.",
        "[3] APJ Abdul Kalam Technological University (KTU), “PBCST304: Object Oriented Programming Syllabus and Course Material”, Kerala, 2024.",
        "[4] Food and Agriculture Organization of the United Nations (FAO), “The State of Food and Agriculture: Moving Forward on Food Loss and Waste Reduction”, Rome, 2019.",
        "[5] United Nations Environment Programme (UNEP), “Food Waste Index Report 2024: Think Eat Save”, Nairobi, Kenya, 2024.",
        "[6] SQLite Consortium, “SQLite Documentation and System Architecture”, https://www.sqlite.org/docs.html, 2024.",
        "[7] Oracle Corporation, “Java Platform, Standard Edition (Java SE 17 / 21) API Specification”, Oracle Technology Network, 2023.",
        "[8] Joshua Bloch, “Effective Java”, 3rd Edition, Addison-Wesley Professional, 2018."
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(4)
        p.add_run(r)

    # =========================================================================
    # APPENDIX: CODE LISTING
    # =========================================================================
    doc.add_page_break()
    add_h1("APPENDIX: CODE LISTING")
    add_p(
        "Below are primary source code listings demonstrating the core object-oriented structures, interfaces, "
        "and algorithmic implementations in ChronoChef."
    )

    def add_code_snippet(title, filename):
        add_h2(title)
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                code_text = f.read()
            lines = code_text.split('\n')
            # Extract first 60-80 lines of interest
            snippet = '\n'.join(lines[:65])
            
            table = doc.add_table(rows=1, cols=1)
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = False
            c = table.cell(0, 0)
            c.width = Inches(6.5)
            set_cell_shading(c, "F8FAFC")
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(snippet)
            run.font.name = "Consolas"
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(30, 41, 59)
            doc.add_paragraph()

    add_code_snippet("1. PriorityPricingService.java (PDI Algorithm Engine)", "src/service/PriorityPricingService.java")
    add_code_snippet("2. FoodItem.java (Base Abstract Class - Encapsulation)", "src/model/FoodItem.java")
    add_code_snippet("3. InventoryOperations.java (Core Interface)", "src/model/InventoryOperations.java")
    add_code_snippet("4. DatabaseManager.java (Singleton JDBC Connection Manager)", "src/database/DatabaseManager.java")

    out_file = "ChronoChef_Project_Report.docx"
    doc.save(out_file)
    print(f"Project report successfully generated and saved to {out_file}!")

if __name__ == "__main__":
    build_project_report()
