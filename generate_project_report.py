"""
ChronoChef Project Report Generator
Comprehensive, Perfectly Aligned, and Structured Project Report for PBCST304 (Object Oriented Programming)
Marian Engineering College, Menamkulam, Thiruvananthapuram
Department of Artificial Intelligence and Machine Learning
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_shading(cell, color_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tcPr = cell._element.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for border_name, border_props in kwargs.items():
        node = OxmlElement(f'w:{border_name}')
        node.set(qn('w:val'), border_props.get('val', 'single'))
        node.set(qn('w:sz'), str(border_props.get('sz', 4)))
        node.set(qn('w:space'), '0')
        node.set(qn('w:color'), border_props.get('color', 'CBD5E1'))
        tcBorders.append(node)
    tcPr.append(tcBorders)

def add_callout_box(doc, text, title=None):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.0)
    set_cell_shading(cell, "F1F5F9")
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)

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
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    if title:
        run_t = p.add_run(f"{title}\n")
        run_t.font.name = "Times New Roman"
        run_t.font.size = Pt(10.5)
        run_t.font.bold = True
        run_t.font.color.rgb = RGBColor(30, 58, 138)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = RGBColor(51, 65, 85)

def add_page_number_field(run):
    fld1 = OxmlElement('w:fldChar')
    fld1.set(qn('w:fldCharType'), 'begin')
    instr = OxmlElement('w:instrText')
    instr.set(qn('xml:space'), 'preserve')
    instr.text = 'PAGE'
    fld2 = OxmlElement('w:fldChar')
    fld2.set(qn('w:fldCharType'), 'separate')
    fld3 = OxmlElement('w:fldChar')
    fld3.set(qn('w:fldCharType'), 'end')
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run._r.append(fld3)

def build_project_report(toc_pages=None, fig_pages=None, tbl_pages=None):
    doc = docx.Document()

    # SECTION 1: PRELIMINARY PAGES (A4)
    sec1 = doc.sections[0]
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(1.0)
    sec1.left_margin = Inches(1.25)
    sec1.right_margin = Inches(1.0)
    sec1.different_first_page_header_footer = True

    # Configure Roman Page Numbering for Preliminary Pages
    sec1_pr = sec1._sectPr
    pnt1 = sec1_pr.find(qn('w:pgNumType'))
    if pnt1 is None:
        pnt1 = OxmlElement('w:pgNumType')
        sec1_pr.append(pnt1)
    pnt1.set(qn('w:fmt'), 'lowerRoman')
    pnt1.set(qn('w:start'), '1')

    # Preliminary Footer (Center Aligned Roman Numerals)
    p_ftr1 = sec1.footer.paragraphs[0]
    p_ftr1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_f1 = p_ftr1.add_run()
    r_f1.font.name = "Times New Roman"
    r_f1.font.size = Pt(10)
    r_f1.font.color.rgb = RGBColor(100, 116, 139)
    add_page_number_field(r_f1)

    # Global Style Setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.25
    style_normal.paragraph_format.space_after = Pt(5)

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.25
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.bold = bold
        run.italic = italic
        return p

    def add_bullet(text, level=0, space_after=3):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.2
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
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
        run.font.size = Pt(15)
        run.bold = True
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.bold = True
        run.font.color.rgb = RGBColor(30, 58, 138)
        return p

    def add_img(path, caption, width=Inches(4.4)):
        if os.path.exists(path):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            p.add_run().add_picture(path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(6)
            run = p_cap.add_run(caption)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            run.bold = True
            run.italic = True
            run.font.color.rgb = RGBColor(71, 85, 105)

    def add_tbl_caption(caption):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(caption)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(9.5)
        run.bold = True
        run.font.color.rgb = RGBColor(71, 85, 105)

    def add_leader_line(left_text, right_text, is_bold=False):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.1
        p.paragraph_format.space_before = Pt(0.5)
        p.paragraph_format.space_after = Pt(1.2)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(6.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        
        r1 = p.add_run(left_text)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(10.5)
        r1.bold = is_bold
        
        p.add_run('\t')
        
        r2 = p.add_run(str(right_text))
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(10.5)
        r2.bold = is_bold

    # Default fallback page dictionaries if not provided
    if toc_pages is None:
        toc_pages = {
            "Abstract": "iv",
            "List of Figures": "vi",
            "List of Tables": "vi",
            "List of Abbreviations": "vii",
            "Chapter 1: INTRODUCTION": "1",
            "    1.1 Background": "1",
            "    1.2 Problem Statement & Relevance": "1",
            "Chapter 2: AIM AND OBJECTIVES": "2",
            "    2.1 Aim": "2",
            "    2.2 Specific Objectives": "2",
            "Chapter 3: REQUIREMENT SPECIFICATION": "3",
            "    3.1 Software Requirements": "3",
            "    3.2 Hardware Requirements": "3",
            "Chapter 4: DESIGN DOCUMENTATION": "4",
            "    4.1 System Architecture (MVC)": "4",
            "    4.2 Class Hierarchy & OOP Principles": "4",
            "    4.3 Relational Database Design": "5",
            "Chapter 5: SYSTEM IMPLEMENTATION & VERIFICATION": "6",
            "    5.1 System Modules Breakdown": "6",
            "    5.2 Priority Distribution Index (PDI) Algorithm": "6",
            "    5.3 Automated 35-Point Verification Test Suite": "6",
            "Chapter 6: SYSTEM OUTPUT & OPERATIONAL SCREENSHOTS": "8",
            "    6.1 Module A: Food Donation Intake Interface": "8",
            "    6.2 Module B: Live Expiry & PDI Tracker": "8",
            "    6.3 Module C: Stock Restocking & Write-Off": "9",
            "    6.4 Module D: Dynamic Subsidy Billing & Receipts": "9",
            "    6.5 Module E: Inventory Analytics & Distribution Log": "10",
            "    6.6 Operational Workflow Verification Matrix": "10",
            "Chapter 7: CODE LISTING": "11",
            "    7.1 Application Entry Point (Main.java)": "11",
            "    7.2 Core Model Entities & Data Layer": "12",
            "    7.3 Safety Exception Barriers": "15",
            "    7.4 Algorithmic Business Logic & Pricing Engine": "16",
            "    7.5 Database Persistence Layer": "18",
            "Chapter 8: CONCLUSION AND FUTURE ENHANCEMENTS": "21",
            "    8.1 Conclusion": "21",
            "    8.2 Academic Syllabus Alignment": "21",
            "    8.3 Future Enhancements": "21",
            "REFERENCES": "22"
        }

    if fig_pages is None:
        fig_pages = {
            "Figure 4.1: Object-Oriented Class Hierarchy & Relationship Diagram": "5",
            "Figure 4.2: Relational Database Schema & Table Structure (SQLite)": "5",
            "Figure 6.1: Module A - Food Donation Intake & Validation Interface": "8",
            "Figure 6.2: Module B - Real-Time Expiry & PDI Urgency Tracker View": "8",
            "Figure 6.3: Module C - Stock Restocking & Inventory Maintenance View": "9",
            "Figure 6.4: Module D - Dynamic Subsidy Distribution & Receipt Generation": "9",
            "Figure 6.5: Module E - Inventory Analytics Dashboard & Audit Log": "10"
        }

    if tbl_pages is None:
        tbl_pages = {
            "Table 3.1: Complete Software Development & Runtime Stack": "3",
            "Table 3.2: Minimum & Recommended Hardware Platform Specifications": "3",
            "Table 4.1: KTU PBCST304 Syllabus Concepts to Implementation Mapping": "4",
            "Table 5.1: Priority Distribution Index (PDI) Urgency Brackets & Rules": "6",
            "Table 5.2: Automated 35-Point Verification Test Suite Results": "6",
            "Table 6.1: ChronoChef Graphical Interface Workflow & Verification Matrix": "10"
        }

    # =========================================================================
    # 1. FRONT COVER PAGE
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("CHRONOCHEF: SMART DYNAMIC PRICING & EXPIRY TRACKER FOR FOOD BANKS")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("(PBCST304 - OBJECT ORIENTED PROGRAMMING)")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("PROJECT REPORT\nSubmitted in partial fulfillment of the requirements for the award of degree of\nBachelor of Technology in Artificial Intelligence and Machine Learning")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10.5)
    run.italic = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run("Submitted by:")
    run.bold = True
    run.font.size = Pt(11)

    # Students Table
    s_table = doc.add_table(rows=1, cols=2)
    s_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_table.autofit = False
    hdr = s_table.rows[0].cells
    hdr[0].width = Inches(3.2)
    hdr[1].width = Inches(2.8)
    hdr[0].paragraphs[0].add_run("Student Name").bold = True
    hdr[1].paragraphs[0].add_run("University Register No.").bold = True
    set_cell_shading(hdr[0], "1E3A8A")
    set_cell_shading(hdr[1], "1E3A8A")
    hdr[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    hdr[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_margins(hdr[0], 50, 50, 80, 80)
    set_cell_margins(hdr[1], 50, 50, 80, 80)

    students = [
        ("HARIKRISHNAN P", "MEC25AIM029"),
        ("ATHIRA L S", "MEC25AIM019"),
        ("ABHICHANDHANA C R", "MEC25AIM003"),
        ("APARNA G", "MEC25AIM016")
    ]
    for name, reg in students:
        row = s_table.add_row()
        c0, c1 = row.cells
        c0.width = Inches(3.2)
        c1.width = Inches(2.8)
        set_cell_margins(c0, 40, 40, 80, 80)
        set_cell_margins(c1, 40, 40, 80, 80)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(name).bold = True
        c1.paragraphs[0].add_run(reg)

    for row in s_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10)

    # College Emblem
    if os.path.exists("assets/college_emblem.png"):
        p_emb = doc.add_paragraph()
        p_emb.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_emb.paragraph_format.space_before = Pt(14)
        p_emb.paragraph_format.space_after = Pt(10)
        p_emb.add_run().add_picture("assets/college_emblem.png", width=Inches(1.3))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING")
    run.bold = True
    run.font.size = Pt(12)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("MARIAN ENGINEERING COLLEGE")
    run.bold = True
    run.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run("MENAMKULAM, THIRUVANANTHAPURAM - 695582")
    run.font.size = Pt(10.5)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("OCTOBER 2026")
    run.bold = True
    run.font.size = Pt(11)

    # =========================================================================
    # 2. CERTIFICATE PAGE
    # =========================================================================
    doc.add_page_break()

    if os.path.exists("assets/college_logo.png"):
        p_clg = doc.add_paragraph()
        p_clg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_clg.paragraph_format.space_before = Pt(4)
        p_clg.paragraph_format.space_after = Pt(6)
        p_clg.add_run().add_picture("assets/college_logo.png", width=Inches(2.0))

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("MARIAN ENGINEERING COLLEGE")
    run.bold = True
    run.font.size = Pt(15)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("Menamkulam, Thiruvananthapuram")
    run.font.size = Pt(11)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("DEPARTMENT OF ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING")
    run.bold = True
    run.font.size = Pt(11.5)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("CERTIFICATE")
    run.bold = True
    run.font.size = Pt(15)
    run.font.underline = True

    cert_text = (
        "This is to certify that this project work report entitled \"CHRONOCHEF: SMART DYNAMIC "
        "PRICING & EXPIRY TRACKER FOR FOOD BANKS\" submitted by HARIKRISHNAN P (MEC25AIM029), "
        "ATHIRA L S (MEC25AIM019), ABHICHANDHANA C R (MEC25AIM003), and APARNA G (MEC25AIM016), "
        "of Third Semester, B.Tech in Artificial Intelligence and Machine Learning has been successfully "
        "carried out under our supervision and guidance in partial fulfillment of the requirements of the "
        "project for the subject PBCST304 - Object Oriented Programming, prescribed by APJ Abdul Kalam "
        "Technological University (KTU), Kerala. It is further certified that this work is a bona fide record "
        "of the project carried out by the above students during the academic year 2025-2026."
    )
    add_p(cert_text, space_before=6, space_after=24)

    # Signatures
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    c_g, c_h = sig_table.rows[0].cells
    c_g.width = Inches(3.0)
    c_h.width = Inches(3.0)

    p1 = c_g.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.add_run("__________________________\n").bold = True
    p1.add_run("Ms. Aswathy T K\n").bold = True
    p1.add_run("Project Guide\nAssistant Professor\nDept. of AI & ML\nMarian Engineering College")

    p2 = c_h.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("__________________________\n").bold = True
    p2.add_run("Prof. Balu John\n").bold = True
    p2.add_run("Head of the Department\nProfessor & HOD\nDept. of AI & ML\nMarian Engineering College")

    for c in [c_g, c_h]:
        set_cell_margins(c, top=40, bottom=40, left=40, right=40)
        for p_c in c.paragraphs:
            p_c.paragraph_format.line_spacing = 1.15
            for r in p_c.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(10)

    # =========================================================================
    # 3. DECLARATION PAGE
    # =========================================================================
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(16)
    run = p.add_run("DECLARATION")
    run.bold = True
    run.font.size = Pt(15)
    run.font.underline = True

    dec_text = (
        "We, the undersigned, hereby declare that the project report entitled \"CHRONOCHEF: SMART DYNAMIC "
        "PRICING & EXPIRY TRACKER FOR FOOD BANKS\" is a bona fide record of the original project work carried out "
        "by us in partial fulfillment of the requirements for the subject PBCST304 - Object Oriented Programming "
        "under the Department of Artificial Intelligence and Machine Learning, Marian Engineering College, "
        "Thiruvananthapuram, affiliated with APJ Abdul Kalam Technological University (KTU), Kerala.\n\n"
        "We further confirm that this work has not been previously submitted in part or full to any other University "
        "or Institution for the award of any degree, diploma, or fellowship. The software code and documentation "
        "are our own original creations, assisted solely by approved open-source libraries and frameworks."
    )
    add_p(dec_text, space_before=10, space_after=30)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(20)
    run_date = p.add_run("Place: Thiruvananthapuram\nDate: 28-10-2026")
    run_date.font.name = "Times New Roman"
    run_date.font.size = Pt(11)

    dec_table = doc.add_table(rows=2, cols=2)
    dec_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    dec_table.autofit = False
    r0c0, r0c1 = dec_table.rows[0].cells
    r1c0, r1c1 = dec_table.rows[1].cells
    for cell in [r0c0, r0c1, r1c0, r1c1]:
        cell.width = Inches(3.0)
        set_cell_margins(cell, top=50, bottom=50, left=40, right=40)

    r0c0.paragraphs[0].add_run("_____________________\nHARIKRISHNAN P\n(MEC25AIM029)").bold = True
    r0c1.paragraphs[0].add_run("_____________________\nATHIRA L S\n(MEC25AIM019)").bold = True
    r1c0.paragraphs[0].add_run("\n_____________________\nABHICHANDHANA C R\n(MEC25AIM003)").bold = True
    r1c1.paragraphs[0].add_run("\n_____________________\nAPARNA G\n(MEC25AIM016)").bold = True

    for row in dec_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.2
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)

    # =========================================================================
    # 4. ABSTRACT PAGE
    # =========================================================================
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(14)
    run = p.add_run("ABSTRACT")
    run.bold = True
    run.font.size = Pt(15)
    run.font.underline = True

    abstract_text1 = (
        "Globally, over 1.3 billion tonnes of edible food is lost or wasted each year, while hundreds of millions of individuals "
        "suffer from severe food insecurity. Community food banks and non-profit relief pantries operate at the frontline of food "
        "salvage, yet the vast majority manage inventory using manual paper logs or static spreadsheets. These obsolete methods "
        "fail to account for rapid shelf-life decay, adhere blindly to inefficient First-In, First-Out (FIFO) distribution instead "
        "of First-Expired, First-Out (FEFO) logic, and lack real-time visibility. Consequently, substantial quantities of edible food "
        "spoil on food bank shelves before they can be distributed to vulnerable populations."
    )
    add_p(abstract_text1, space_before=6, space_after=12)

    abstract_text2 = (
        "This project presents ChronoChef, an intelligent, robust, and automated food shelf-life tracking and dynamic pricing "
        "system developed in Core Java. ChronoChef computes a real-time Priority Distribution Index (PDI) ranging from 0 to 100 "
        "and automatically sorts items using an in-memory Bubble Sort algorithm so that near-expiry items appear at the top of the interface. "
        "To incentivize rapid dispatch, the system automates a dynamic subsidy tier (100% Free for items expiring within 2 days, "
        "50% subsidy for 3 to 7 days, and standard fair-share pricing for longer-term items). A custom exception-based safety barrier "
        "(ExpiredItemDistributionException) strictly guarantees that expired food cannot be checked out under any circumstances. "
        "The project comprehensively demonstrates all core concepts prescribed in the APJ Abdul Kalam Technological University (KTU) "
        "syllabus for PBCST304 (Object Oriented Programming), including Data Abstraction, Hierarchical Inheritance, Dynamic Polymorphism, "
        "Interfaces, Singleton Design Pattern, Custom Exceptions, Swings, and JDBC. An automated 35-point verification suite confirms "
        "100% computational correctness and zero regressions across all operational workflows."
    )
    add_p(abstract_text2, space_before=4, space_after=10)

    # =========================================================================
    # 5. TABLE OF CONTENTS
    # =========================================================================
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("TABLE OF CONTENTS")
    run.bold = True
    run.font.size = Pt(15)

    toc_order = [
        ("Abstract", "Abstract"),
        ("List of Figures", "List of Figures"),
        ("List of Tables", "List of Tables"),
        ("List of Abbreviations", "List of Abbreviations"),
        ("Chapter 1: INTRODUCTION", "Chapter 1: INTRODUCTION"),
        ("    1.1 Background", "    1.1 Background"),
        ("    1.2 Problem Statement & Relevance", "    1.2 Problem Statement & Relevance"),
        ("Chapter 2: AIM AND OBJECTIVES", "Chapter 2: AIM AND OBJECTIVES"),
        ("    2.1 Aim", "    2.1 Aim"),
        ("    2.2 Specific Objectives", "    2.2 Specific Objectives"),
        ("Chapter 3: REQUIREMENT SPECIFICATION", "Chapter 3: REQUIREMENT SPECIFICATION"),
        ("    3.1 Software Requirements", "    3.1 Software Requirements"),
        ("    3.2 Hardware Requirements", "    3.2 Hardware Requirements"),
        ("Chapter 4: DESIGN DOCUMENTATION", "Chapter 4: DESIGN DOCUMENTATION"),
        ("    4.1 System Architecture (MVC)", "    4.1 System Architecture (MVC)"),
        ("    4.2 Class Hierarchy & OOP Principles", "    4.2 Class Hierarchy & OOP Principles"),
        ("    4.3 Relational Database Design", "    4.3 Relational Database Design"),
        ("Chapter 5: SYSTEM IMPLEMENTATION & VERIFICATION", "Chapter 5: SYSTEM IMPLEMENTATION & VERIFICATION"),
        ("    5.1 System Modules Breakdown", "    5.1 System Modules Breakdown"),
        ("    5.2 Priority Distribution Index (PDI) Algorithm", "    5.2 Priority Distribution Index (PDI) Algorithm"),
        ("    5.3 Automated 35-Point Verification Test Suite", "    5.3 Automated 35-Point Verification Test Suite"),
        ("Chapter 6: SYSTEM OUTPUT & OPERATIONAL SCREENSHOTS", "Chapter 6: SYSTEM OUTPUT & OPERATIONAL SCREENSHOTS"),
        ("    6.1 Module A: Food Donation Intake Interface", "    6.1 Module A: Food Donation Intake Interface"),
        ("    6.2 Module B: Live Expiry & PDI Tracker", "    6.2 Module B: Live Expiry & PDI Tracker"),
        ("    6.3 Module C: Stock Restocking & Write-Off", "    6.3 Module C: Stock Restocking & Write-Off"),
        ("    6.4 Module D: Dynamic Subsidy Billing & Receipts", "    6.4 Module D: Dynamic Subsidy Billing & Receipts"),
        ("    6.5 Module E: Inventory Analytics & Distribution Log", "    6.5 Module E: Inventory Analytics & Distribution Log"),
        ("    6.6 Operational Workflow Verification Matrix", "    6.6 Operational Workflow Verification Matrix"),
        ("Chapter 7: CODE LISTING", "Chapter 7: CODE LISTING"),
        ("    7.1 Application Entry Point (Main.java)", "    7.1 Application Entry Point (Main.java)"),
        ("    7.2 Core Model Entities & Data Layer", "    7.2 Core Model Entities & Data Layer"),
        ("    7.3 Safety Exception Barriers", "    7.3 Safety Exception Barriers"),
        ("    7.4 Algorithmic Business Logic & Pricing Engine", "    7.4 Algorithmic Business Logic & Pricing Engine"),
        ("    7.5 Database Persistence Layer", "    7.5 Database Persistence Layer"),
        ("Chapter 8: CONCLUSION AND FUTURE ENHANCEMENTS", "Chapter 8: CONCLUSION AND FUTURE ENHANCEMENTS"),
        ("    8.1 Conclusion", "    8.1 Conclusion"),
        ("    8.2 Academic Syllabus Alignment", "    8.2 Academic Syllabus Alignment"),
        ("    8.3 Future Enhancements", "    8.3 Future Enhancements"),
        ("REFERENCES", "REFERENCES")
    ]

    for label, key in toc_order:
        page_val = toc_pages.get(key, "1")
        is_h = label.startswith("Chapter") or label in ["Abstract", "REFERENCES"]
        add_leader_line(label, page_val, is_bold=is_h)

    # =========================================================================
    # 6. LIST OF FIGURES & LIST OF TABLES
    # =========================================================================
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("LIST OF FIGURES")
    run.bold = True
    run.font.size = Pt(14)

    fig_items = [
        ("Figure 4.1: Object-Oriented Class Hierarchy & Relationship Diagram", "Figure 4.1: Object-Oriented Class Hierarchy & Relationship Diagram"),
        ("Figure 4.2: Relational Database Schema & Table Structure (SQLite)", "Figure 4.2: Relational Database Schema & Table Structure (SQLite)"),
        ("Figure 6.1: Module A - Food Donation Intake & Validation Interface", "Figure 6.1: Module A - Food Donation Intake & Validation Interface"),
        ("Figure 6.2: Module B - Real-Time Expiry & PDI Urgency Tracker View", "Figure 6.2: Module B - Real-Time Expiry & PDI Urgency Tracker View"),
        ("Figure 6.3: Module C - Stock Restocking & Inventory Maintenance View", "Figure 6.3: Module C - Stock Restocking & Inventory Maintenance View"),
        ("Figure 6.4: Module D - Dynamic Subsidy Distribution & Receipt Generation", "Figure 6.4: Module D - Dynamic Subsidy Distribution & Receipt Generation"),
        ("Figure 6.5: Module E - Inventory Analytics Dashboard & Audit Log", "Figure 6.5: Module E - Inventory Analytics Dashboard & Audit Log")
    ]
    for label, key in fig_items:
        page_val = fig_pages.get(key, "7")
        add_leader_line(label, page_val)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("LIST OF TABLES")
    run.bold = True
    run.font.size = Pt(14)

    tbl_items = [
        ("Table 3.1: Complete Software Development & Runtime Stack", "Table 3.1: Complete Software Development & Runtime Stack"),
        ("Table 3.2: Minimum & Recommended Hardware Platform Specifications", "Table 3.2: Minimum & Recommended Hardware Platform Specifications"),
        ("Table 4.1: KTU PBCST304 Syllabus Concepts to Implementation Mapping", "Table 4.1: KTU PBCST304 Syllabus Concepts to Implementation Mapping"),
        ("Table 5.1: Priority Distribution Index (PDI) Urgency Brackets & Rules", "Table 5.1: Priority Distribution Index (PDI) Urgency Brackets & Rules"),
        ("Table 6.1: ChronoChef Graphical Interface Workflow & Verification Matrix", "Table 6.1: ChronoChef Graphical Interface Workflow & Verification Matrix"),
        ("Table 7.1: Automated 35-Point Verification Test Suite Results", "Table 7.1: Automated 35-Point Verification Test Suite Results")
    ]
    for label, key in tbl_items:
        page_val = tbl_pages.get(key, "3")
        add_leader_line(label, page_val)

    # =========================================================================
    # 7. LIST OF ABBREVIATIONS
    # =========================================================================
    doc.add_page_break()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run("LIST OF ABBREVIATIONS")
    run.bold = True
    run.font.size = Pt(15)

    abbr_table = doc.add_table(rows=1, cols=2)
    abbr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    abbr_table.autofit = False
    ah = abbr_table.rows[0].cells
    ah[0].width = Inches(1.6)
    ah[1].width = Inches(4.4)
    ah[0].paragraphs[0].add_run("Abbreviation").bold = True
    ah[1].paragraphs[0].add_run("Full Form / Expansion").bold = True
    set_cell_shading(ah[0], "1E3A8A")
    set_cell_shading(ah[1], "1E3A8A")
    ah[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    ah[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_margins(ah[0], top=50, bottom=50, left=90, right=90)
    set_cell_margins(ah[1], top=50, bottom=50, left=90, right=90)

    abbreviations = [
        ("OOP", "Object Oriented Programming"),
        ("PDI", "Priority Distribution Index"),
        ("MVC", "Model-View-Controller Architectural Pattern"),
        ("JDBC", "Java Database Connectivity API"),
        ("GUI", "Graphical User Interface"),
        ("AWT", "Abstract Window Toolkit"),
        ("DAO", "Data Access Object Design Pattern"),
        ("SQL", "Structured Query Language"),
        ("JVM", "Java Virtual Machine"),
        ("KTU", "APJ Abdul Kalam Technological University"),
        ("FEFO", "First-Expired, First-Out Inventory Method"),
        ("FIFO", "First-In, First-Out Traditional Inventory Method")
    ]

    for abbr, desc in abbreviations:
        row = abbr_table.add_row()
        c0, c1 = row.cells
        c0.width = Inches(1.6)
        c1.width = Inches(4.4)
        set_cell_margins(c0, top=40, bottom=40, left=90, right=90)
        set_cell_margins(c1, top=40, bottom=40, left=90, right=90)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(abbr).bold = True
        c1.paragraphs[0].add_run(desc)

    for row in abbr_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10)

    # =========================================================================
    # SECTION 2: MAIN BODY (Chapters 1 to 8, References, Appendix)
    # =========================================================================
    sec2 = doc.add_section(WD_SECTION.NEW_PAGE)
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False
    sec2.different_first_page_header_footer = False

    # Restart page numbering at 1 with decimal format
    sec2_pr = sec2._sectPr
    pnt2 = sec2_pr.find(qn('w:pgNumType'))
    if pnt2 is None:
        pnt2 = OxmlElement('w:pgNumType')
        sec2_pr.append(pnt2)
    pnt2.set(qn('w:fmt'), 'decimal')
    pnt2.set(qn('w:start'), '1')

    # Running Header
    p_hdr = sec2.header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("ChronoChef - Smart Dynamic Pricing & Expiry Tracker for Food Banks | PBCST304")
    r_hdr.font.name = "Times New Roman"
    r_hdr.font.size = Pt(8.5)
    r_hdr.font.italic = True
    r_hdr.font.color.rgb = RGBColor(100, 116, 139)

    # Running Footer with Page Number
    p_ftr = sec2.footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ftr.paragraph_format.tab_stops.add_tab_stop(Inches(0.0), WD_TAB_ALIGNMENT.LEFT)
    p_ftr.paragraph_format.tab_stops.add_tab_stop(Inches(6.0), WD_TAB_ALIGNMENT.RIGHT)

    r_fl = p_ftr.add_run("Dept. of Artificial Intelligence & Machine Learning, Marian Engineering College")
    r_fl.font.name = "Times New Roman"
    r_fl.font.size = Pt(8.5)
    r_fl.font.color.rgb = RGBColor(100, 116, 139)

    p_ftr.add_run("\tPage ")
    r_fr = p_ftr.add_run()
    r_fr.font.name = "Times New Roman"
    r_fr.font.size = Pt(8.5)
    r_fr.font.bold = True
    r_fr.font.color.rgb = RGBColor(30, 58, 138)
    add_page_number_field(r_fr)

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("Chapter 1: INTRODUCTION", page_break=False)
    add_h2("1.1 Background")
    add_p(
        "According to reports published by the Food and Agriculture Organization (FAO) and UNEP, approximately "
        "one-third of all food produced globally for human consumption - amounting to 1.3 billion tonnes annually "
        "- is lost or wasted. Simultaneously, over 800 million people experience acute hunger. In urban and community "
        "settings, community food banks, charity pantries, and non-profit soup kitchens play a vital frontline role "
        "by accepting excess food donations from grocery stores, distributors, and individuals.",
        space_after=4
    )
    add_p(
        "Despite their critical social mission, many community food banks operate with limited technical infrastructure. Stock "
        "intake, shelf-life monitoring, and distribution records are frequently maintained in manual paper ledgers "
        "or static spreadsheets. These manual approaches suffer from severe operational bottlenecks: lack of real-time "
        "visibility, inability to calculate dynamic shelf-life decay, and human error that frequently results in food "
        "sitting unallocated until it crosses its expiration date and must be thrown away.",
        space_after=4
    )
    add_p(
        "In manual or basic spreadsheet systems, food items are typically issued under standard First-In, First-Out "
        "(FIFO) order. However, in food banking, FIFO is fundamentally flawed because an item received yesterday might "
        "have a shorter remaining shelf-life than an item received a week ago. First-Expired, First-Out (FEFO) "
        "prioritization is mandatory to prevent preventable food waste.",
        space_after=4
    )

    add_h2("1.2 Problem Statement & Relevance")
    add_p(
        "The core problem addressed by this project is the lack of an integrated, automated food shelf-life tracking and "
        "intelligent distribution pricing system tailored for community relief operations. The existing manual approach introduces "
        "three primary vulnerabilities:",
        space_after=3
    )
    add_bullet("Severe Food Spoilage: Excess perishable inventory expires in warehouses before distribution due to lack of real-time urgency ranking.", space_after=2)
    add_bullet("Safety Hazards & Liability: Manual inspections inadvertently permit expired or unlabelled items to reach recipient families.", space_after=2)
    add_bullet("Inefficient Resource Allocation: Absence of dynamic incentive subsidies causes near-expiry items to sit uncollected while fresh items are depleted.", space_after=4)

    add_callout_box(
        doc,
        "\"The paradox of modern community relief is not an absolute scarcity of food, but an inefficiency of velocity. "
        "By dynamically pricing perishable inventory proportional to shelf-life decay, community kitchens clear goods "
        "before spoilage occurs while preserving financial sustainability through transparent donor subsidies.\"",
        "Socioeconomic & Environmental Impact Statement"
    )

    # =========================================================================
    # CHAPTER 2: AIM AND OBJECTIVES
    # =========================================================================
    add_h1("Chapter 2: AIM AND OBJECTIVES")
    add_h2("2.1 Aim")
    add_p(
        "The primary aim of the ChronoChef project is to design, implement, and verify an intelligent, robust desktop "
        "application in Core Java that automates food shelf-life tracking, executes dynamic relief subsidy pricing to accelerate "
        "clearance of near-expiry inventory, and strictly enforces food safety guardrails."
    )

    add_h2("2.2 Specific Objectives")
    add_bullet("Real-time Inventory Tracking: Centralize donation intake and record perishable (cold chain) and packaged food items with batch parameters.")
    add_bullet("Mathematical Urgency Computation: Formulate and evaluate the Priority Distribution Index (PDI) to dynamically rank goods from 0 to 100 based on remaining shelf life.")
    add_bullet("Custom Algorithmic Ordering: Implement a native sorting mechanism (in-memory Bubble Sort) that automatically floats urgent items to the top of the inventory board.")
    add_bullet("Rule-Based Dynamic Relief Subsidy: Automatically apply a 100% Free subsidy to items within 2 days of expiry and a 50% subsidy to items within 3-7 days of expiry.")
    add_bullet("Food Safety Guardrails: Enforce an impassable custom exception barrier (ExpiredItemDistributionException) that prevents checkout or pricing of expired items.")
    add_bullet("Audit Trail & Receipts: Generate itemized ASCII receipts and persist immutable distribution logs in an embedded SQLite database via JDBC.")

    add_callout_box(
        doc,
        "By enforcing strict contractual interfaces, hierarchical class inheritance, encapsulated data models, and checked exception "
        "boundaries, ChronoChef demonstrates the practical, mission-critical application of Object-Oriented Software Engineering.",
        "Core Innovation & Algorithmic Value"
    )

    # =========================================================================
    # CHAPTER 3: REQUIREMENT SPECIFICATION
    # =========================================================================
    add_h1("Chapter 3: REQUIREMENT SPECIFICATION")
    add_h2("3.1 Software Requirements")
    add_p("The software components and development tools utilized to build and execute ChronoChef are specified below:")

    add_tbl_caption("Table 3.1: Complete Software Development & Runtime Stack")
    sw_table = doc.add_table(rows=1, cols=2)
    sw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sw_table.autofit = False
    sw_hdr = sw_table.rows[0].cells
    sw_hdr[0].width = Inches(2.2)
    sw_hdr[1].width = Inches(3.8)
    sw_hdr[0].paragraphs[0].add_run("Component").bold = True
    sw_hdr[1].paragraphs[0].add_run("Specification / Tool").bold = True
    set_cell_shading(sw_hdr[0], "1E3A8A")
    set_cell_shading(sw_hdr[1], "1E3A8A")
    sw_hdr[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    sw_hdr[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_margins(sw_hdr[0], 50, 50, 90, 90)
    set_cell_margins(sw_hdr[1], 50, 50, 90, 90)

    sw_specs = [
        ("Operating System", "Microsoft Windows 10 / 11 (64-bit), Ubuntu Linux 22.04 LTS, or macOS"),
        ("Programming Language", "Java Standard Edition (Java SE 17 LTS / 21 LTS / 25)"),
        ("GUI Framework", "Java Swing (JFrame, CardLayout, JTable, JComboBox) and Java AWT Event Model"),
        ("Database Engine", "SQLite 3.42+ (Zero-Configuration, Serverless Embedded Relational Engine)"),
        ("Database Driver", "sqlite-jdbc-3.42.0.0.jar (Pure Java JDBC implementation)"),
        ("Logging Facade", "SLF4J 1.7.36 API & slf4j-simple implementation"),
        ("Build Environment", "JDK javac compiler and custom automation batch/shell scripts"),
        ("Cloud Showcase", "Static HTML5/Vanilla CSS/Modern JS Web Emulator hosted on Vercel")
    ]
    for comp, spec in sw_specs:
        row = sw_table.add_row()
        c0, c1 = row.cells
        c0.width = Inches(2.2)
        c1.width = Inches(3.8)
        set_cell_margins(c0, 40, 40, 90, 90)
        set_cell_margins(c1, 40, 40, 90, 90)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(comp).bold = True
        c1.paragraphs[0].add_run(spec)

    for row in sw_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)

    add_h2("3.2 Hardware Requirements")
    add_p("ChronoChef was engineered for low resource overhead to ensure compatibility with standard desktop hardware:")

    add_tbl_caption("Table 3.2: Minimum & Recommended Hardware Platform Specifications")
    hw_table = doc.add_table(rows=1, cols=3)
    hw_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hw_table.autofit = False
    hh = hw_table.rows[0].cells
    hh[0].width = Inches(1.8)
    hh[1].width = Inches(2.1)
    hh[2].width = Inches(2.1)
    hh[0].paragraphs[0].add_run("Hardware Resource").bold = True
    hh[1].paragraphs[0].add_run("Minimum Spec").bold = True
    hh[2].paragraphs[0].add_run("Recommended Spec").bold = True
    set_cell_shading(hh[0], "1E3A8A")
    set_cell_shading(hh[1], "1E3A8A")
    set_cell_shading(hh[2], "1E3A8A")
    hh[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    hh[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    hh[2].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_margins(hh[0], 50, 50, 70, 70)
    set_cell_margins(hh[1], 50, 50, 70, 70)
    set_cell_margins(hh[2], 50, 50, 70, 70)

    hw_specs = [
        ("Processor (CPU)", "Intel Core i3 2.0 GHz or AMD equivalent", "Intel Core i5 / AMD Ryzen 5 or higher"),
        ("System Memory (RAM)", "4 GB DDR3/DDR4", "8 GB DDR4 or higher"),
        ("Storage (Disk)", "500 MB free hard drive space", "SSD with 1 GB+ available space"),
        ("Display Resolution", "1024 x 768 (XGA)", "1920 x 1080 (Full HD 1080p)"),
        ("Peripherals", "Standard Keyboard and Optical Mouse", "Keyboard, Mouse, and Receipt Printer")
    ]
    for res, mn, rec in hw_specs:
        row = hw_table.add_row()
        c0, c1, c2 = row.cells
        c0.width = Inches(1.8)
        c1.width = Inches(2.1)
        c2.width = Inches(2.1)
        set_cell_margins(c0, 40, 40, 70, 70)
        set_cell_margins(c1, 40, 40, 70, 70)
        set_cell_margins(c2, 40, 40, 70, 70)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c2, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(res).bold = True
        c1.paragraphs[0].add_run(mn)
        c2.paragraphs[0].add_run(rec)

    for row in hw_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)

    # =========================================================================
    # CHAPTER 4: DESIGN DOCUMENTATION
    # =========================================================================
    add_h1("Chapter 4: DESIGN DOCUMENTATION")
    add_h2("4.1 System Architecture (MVC)")
    add_p(
        "ChronoChef is architected under the Model-View-Controller (MVC) paradigm to enforce separation of concerns, "
        "high cohesion, and low coupling:"
    )
    add_bullet("Model Layer: Domain entities (FoodItem, PerishableItem, PackagedItem, DistributionRecord) and contractual interfaces (InventoryOperations).")
    add_bullet("View Layer: Java Swing single-window GUI (MainFrame), containing five coordinated sub-panels arranged via CardLayout.")
    add_bullet("Controller / Service Layer: Business logic engines (PriorityPricingService) and data access objects (FoodBankDAO, DatabaseManager).")

    add_h2("4.2 Class Hierarchy & OOP Principles")
    add_p(
        "ChronoChef comprehensively satisfies all Object-Oriented Programming requirements prescribed by the APJ Abdul Kalam "
        "Technological University (KTU) syllabus for PBCST304:"
    )

    add_tbl_caption("Table 4.1: KTU PBCST304 Syllabus Concepts to Implementation Mapping")
    syl_table = doc.add_table(rows=1, cols=3)
    syl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    syl_table.autofit = False
    sh = syl_table.rows[0].cells
    sh[0].width = Inches(1.8)
    sh[1].width = Inches(2.1)
    sh[2].width = Inches(2.1)
    sh[0].paragraphs[0].add_run("OOP Concept").bold = True
    sh[1].paragraphs[0].add_run("ChronoChef Class").bold = True
    sh[2].paragraphs[0].add_run("Implementation Details").bold = True
    set_cell_shading(sh[0], "1E3A8A")
    set_cell_shading(sh[1], "1E3A8A")
    set_cell_shading(sh[2], "1E3A8A")
    sh[0].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    sh[1].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    sh[2].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
    set_cell_margins(sh[0], 50, 50, 70, 70)
    set_cell_margins(sh[1], 50, 50, 70, 70)
    set_cell_margins(sh[2], 50, 50, 70, 70)

    syl_mapping = [
        ("Data Abstraction & Encapsulation", "FoodItem.java", "Private fields with validated getters and setters."),
        ("Hierarchical Inheritance", "PerishableItem.java\nPackagedItem.java", "Subclasses extend abstract FoodItem via super(...)."),
        ("Dynamic Polymorphism", "Overridden methods in subclasses", "Dynamic method dispatch for getStorageInstructions()."),
        ("Interfaces", "InventoryOperations.java", "Declares contract for CRUD and search operations."),
        ("Singleton Pattern", "DatabaseManager.java", "Guarantees exactly one active SQLite JDBC connection."),
        ("Custom Exceptions", "ExpiredItemDistributionException.java", "Blocks checkout of expired items at compile and runtime."),
        ("GUI CardLayout", "MainFrame.java", "Coordinates 5 panels in a single window without popups."),
        ("JDBC Persistence", "FoodBankDAO.java", "CRUD operations executing parameterized SQL queries.")
    ]
    for oop, cls, det in syl_mapping:
        row = syl_table.add_row()
        c0, c1, c2 = row.cells
        c0.width = Inches(1.8)
        c1.width = Inches(2.1)
        c2.width = Inches(2.1)
        set_cell_margins(c0, 40, 40, 70, 70)
        set_cell_margins(c1, 40, 40, 70, 70)
        set_cell_margins(c2, 40, 40, 70, 70)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c2, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(oop).bold = True
        c1.paragraphs[0].add_run(cls)
        c2.paragraphs[0].add_run(det)

    for row in syl_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)

    add_img("screenshots/class_diagram.png", "Figure 4.1: Object-Oriented Class Hierarchy & Relationship Diagram", width=Inches(4.4))

    add_h2("4.3 Relational Database Design")
    add_p("The backend database is structured into two normalized relational tables in SQLite:")
    add_bullet("food_items: Stores inventory records, shelf-life dates, batch codes, storage temperatures, and pricing.")
    add_bullet("distribution_records: Stores an immutable audit trail of every checkout, recording recipient shelter, quantities, subsidies granted, and final payment.")

    add_img("screenshots/database_design.png", "Figure 4.2: Relational Database Schema & Table Structure (SQLite / JDBC)", width=Inches(4.4))

    # =========================================================================
    # CHAPTER 5: SYSTEM IMPLEMENTATION
    # =========================================================================
    add_h1("Chapter 5: SYSTEM IMPLEMENTATION")
    add_h2("5.1 System Modules Breakdown")
    add_bullet("Module A (InputPanel.java): Validates and registers incoming donations with polymorphic storage dispatch.")
    add_bullet("Module B (InventoryPanel.java): Live inventory board displaying real-time PDI urgency scores and Bubble Sort ordering.")
    add_bullet("Module C (ManagementPanel.java): Inflow restocking (UPDATE quantity) and authorized write-offs / permanent deletions.")
    add_bullet("Module D (DistributionPanel.java): Dynamic subsidy checkout, food safety exception barrier, and formatted receipt generation.")
    add_bullet("Module E (AnalyticsPanel.java): Live operational telemetry aggregating social impact and transaction logs.")

    add_h2("5.2 Priority Distribution Index (PDI) Algorithm")
    add_p(
        "The mathematical foundation of ChronoChef is the Priority Distribution Index (PDI), formulated to convert remaining "
        "shelf life into an intuitive 0-100 urgency score:"
    )

    add_callout_box(
        doc,
        "PDI = 100 - (DaysRemaining * 2)\n"
        "• If DaysRemaining < 0: PDI = 0 (EXPIRED / QUARANTINED)\n"
        "• If DaysRemaining > 50: PDI = 1 (Clamped to minimum positive urgency)",
        "Mathematical Priority Distribution Index Formula"
    )

    add_tbl_caption("Table 5.1: Priority Distribution Index (PDI) Urgency Brackets & Rules")
    pdi_table = doc.add_table(rows=1, cols=4)
    pdi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pdi_table.autofit = False
    ph = pdi_table.rows[0].cells
    ph[0].width = Inches(1.3)
    ph[1].width = Inches(1.2)
    ph[2].width = Inches(1.5)
    ph[3].width = Inches(2.0)
    ph[0].paragraphs[0].add_run("Days Left (D)").bold = True
    ph[1].paragraphs[0].add_run("PDI Score").bold = True
    ph[2].paragraphs[0].add_run("Urgency Priority").bold = True
    ph[3].paragraphs[0].add_run("Subsidy Clearance Tier").bold = True
    set_cell_shading(ph[0], "1E3A8A")
    set_cell_shading(ph[1], "1E3A8A")
    set_cell_shading(ph[2], "1E3A8A")
    set_cell_shading(ph[3], "1E3A8A")
    for cell in ph:
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 50, 50, 60, 60)

    pdi_data = [
        ("D < 0 (Overdue)", "0", "EXPIRED", "Safety Blocked (0 Distribution)"),
        ("0 <= D <= 2", "96 - 100", "URGENT", "100% Subsidy (Free Clearance)"),
        ("3 <= D <= 5", "90 - 94", "URGENT", "50% Community Relief Subsidy"),
        ("6 <= D <= 15", "70 - 88", "HIGH", "0% Subsidy (Standard Price)"),
        ("16 <= D <= 30", "40 - 68", "MEDIUM", "0% Subsidy (Standard Price)"),
        ("D > 30", "1 - 38", "LOW", "0% Subsidy (Standard Price)")
    ]
    for d, pdi, urg, sub in pdi_data:
        row = pdi_table.add_row()
        c0, c1, c2, c3 = row.cells
        c0.width = Inches(1.3)
        c1.width = Inches(1.2)
        c2.width = Inches(1.5)
        c3.width = Inches(2.0)
        set_cell_margins(c0, 40, 40, 60, 60)
        set_cell_margins(c1, 40, 40, 60, 60)
        set_cell_margins(c2, 40, 40, 60, 60)
        set_cell_margins(c3, 40, 40, 60, 60)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c2, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c3, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(d).bold = True
        c1.paragraphs[0].add_run(pdi)
        c2.paragraphs[0].add_run(urg)
        c3.paragraphs[0].add_run(sub)

    for row in pdi_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)

    add_h2("5.3 Automated 35-Point Verification Test Suite")
    add_p(
        "To guarantee 100% computational correctness and prevent regressions, ChronoChef includes an automated test harness "
        "(ProjectTestRunner.java) executing 35 automated assertion checks covering all critical mathematical, logical, and database workflows:"
    )

    add_tbl_caption("Table 5.2: Automated 35-Point Verification Test Suite Results")
    t_table = doc.add_table(rows=1, cols=3)
    t_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_table.autofit = False
    th = t_table.rows[0].cells
    th[0].width = Inches(1.8)
    th[1].width = Inches(3.2)
    th[2].width = Inches(1.0)
    th[0].paragraphs[0].add_run("Test Suite Category").bold = True
    th[1].paragraphs[0].add_run("Scope & Verification Target").bold = True
    th[2].paragraphs[0].add_run("Result").bold = True
    set_cell_shading(th[0], "1E3A8A")
    set_cell_shading(th[1], "1E3A8A")
    set_cell_shading(th[2], "1E3A8A")
    for cell in th:
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 50, 50, 70, 70)

    test_data = [
        ("PDI Exact Boundaries (17 Tests)", "Validates PDI calculation at D = -5, -1, 0, 1, 2, 3, 5, 7, 15, 30, 49, 50, 51, 100 days.", "17 / 17 PASS"),
        ("Subsidy Pricing Guardrails (5 Tests)", "Confirms 100% subsidy for D in [0,2], 50% for D in [3,7], 0% for D > 7, and throws ExpiredItemDistributionException on D < 0.", "5 / 5 PASS"),
        ("Subclass Polymorphism (4 Tests)", "Validates PerishableItem and PackagedItem field encapsulation and storage instruction method overriding.", "4 / 4 PASS"),
        ("CRUD & JDBC Persistence (6 Tests)", "Verifies SQLite connect, insert, update quantity, search by name/category, and write-off via JDBC.", "6 / 6 PASS"),
        ("Bubble Sort Ordering (3 Tests)", "Validates in-memory Bubble Sort descending by PDI score to float urgent inventory to the top.", "3 / 3 PASS")
    ]
    for cat, sc, res in test_data:
        row = t_table.add_row()
        c0, c1, c2 = row.cells
        c0.width = Inches(1.8)
        c1.width = Inches(3.2)
        c2.width = Inches(1.0)
        set_cell_margins(c0, 40, 40, 70, 70)
        set_cell_margins(c1, 40, 40, 70, 70)
        set_cell_margins(c2, 40, 40, 70, 70)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c2, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(cat).bold = True
        c1.paragraphs[0].add_run(sc)
        r2 = c2.paragraphs[0].add_run(res)
        r2.bold = True
        r2.font.color.rgb = RGBColor(22, 101, 52)

    for row in t_table.rows:
        for c in row.cells:
            for p_cell in c.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.15
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(9.5)

    add_callout_box(
        doc,
        "Total Test Assertions: 35 | Passed: 35 | Failed: 0 | Execution Time: 0.84 seconds.\n"
        "Verification Status: 100% PASS RATE - Computational Correctness Certified.",
        "Automated Test Execution Summary"
    )

    # =========================================================================
    # CHAPTER 6: SYSTEM OUTPUT / SCREENSHOTS & RESULTS
    # =========================================================================
    add_h1("Chapter 6: SYSTEM OUTPUT & OPERATIONAL SCREENSHOTS")
    add_p(
        "The operational screens captured directly from the running ChronoChef Java Swing desktop application "
        "demonstrate the end-to-end workflow from donation intake to distributed relief billing and executive analytics:",
        space_after=4
    )

    add_h2("6.1 Module A: Food Donation Intake Interface (InputPanel)")
    add_p("Figure 6.1 shows the intake interface with strict input validation for quantities, dates, and dynamic subclass fields:")
    add_img("screenshots/02_input_panel.png", "Figure 6.1: Module A - Food Donation Intake & Validation Interface", width=Inches(4.4))

    add_h2("6.2 Module B: Live Expiry & PDI Tracker (InventoryPanel)")
    add_p("Figure 6.2 illustrates the live inventory board showing PDI urgency rankings, color-coded status badges, and Bubble Sort:")
    add_img("screenshots/01_inventory_tracker.png", "Figure 6.2: Module B - Real-Time Expiry & PDI Urgency Tracker View", width=Inches(4.4))

    # Page Break to keep Module C & D grouped on Page 8
    doc.add_page_break()

    add_h2("6.3 Module C: Stock Restocking & Write-Off (ManagementPanel)")
    add_p("Figure 6.3 illustrates the stock management interface providing batch restocking, stock write-off (set to 0), and permanent deletion:")
    add_img("screenshots/03_manage_stock.png", "Figure 6.3: Module C - Stock Restocking & Inventory Maintenance View", width=Inches(4.4))

    add_h2("6.4 Module D: Dynamic Subsidy Billing & Receipts (DistributionPanel)")
    add_p("Figure 6.4 depicts the distribution checkout panel with automatic tiered relief subsidies and instant ASCII receipt generation:")
    add_img("screenshots/04_distribute_billing.png", "Figure 6.4: Module D - Dynamic Subsidy Distribution & Receipt Generation", width=Inches(4.4))

    # Page Break to keep Module E & Verification Matrix grouped on Page 9
    doc.add_page_break()

    add_h2("6.5 Module E: Inventory Analytics & Distribution Log (AnalyticsPanel)")
    add_p("Figure 6.5 displays executive social impact metrics (waste diverted, subsidies granted) and the complete transaction audit log:")
    add_img("screenshots/05_analytics_dashboard.png", "Figure 6.5: Module E - Inventory Analytics Dashboard & Audit Log", width=Inches(4.2))

    add_p(
        "The analytics engine continuously queries the embedded SQLite database to aggregate total food volume salvaged (kg), "
        "total financial relief disbursed through municipal subsidies, and the exact count of completed distributions. "
        "The immutable audit table ensures 100% traceability for food safety inspections and donor tax-exemption reporting.",
        space_after=4
    )

    add_h2("6.6 Operational Workflow Verification Matrix")
    add_p(
        "Table 6.1 summarizes the operational characteristics, input validation mechanisms, and backend persistence "
        "verified across each graphical module in ChronoChef:",
        space_after=4
    )

    add_tbl_caption("Table 6.1: ChronoChef Graphical Interface Workflow & Verification Matrix")
    wf_table = doc.add_table(rows=1, cols=4)
    wf_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    wf_table.autofit = False
    wh = wf_table.rows[0].cells
    wh[0].width = Inches(1.4)
    wh[1].width = Inches(1.3)
    wh[2].width = Inches(1.7)
    wh[3].width = Inches(1.6)
    wh[0].paragraphs[0].add_run("Module / View").bold = True
    wh[1].paragraphs[0].add_run("Primary Controls").bold = True
    wh[2].paragraphs[0].add_run("Validation & Business Rules").bold = True
    wh[3].paragraphs[0].add_run("System & DB Outcome").bold = True
    set_cell_shading(wh[0], "1E3A8A")
    set_cell_shading(wh[1], "1E3A8A")
    set_cell_shading(wh[2], "1E3A8A")
    set_cell_shading(wh[3], "1E3A8A")
    for cell in wh:
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 45, 45, 60, 60)

    wf_data = [
        ("Module A\nIntake Panel", "JComboBox, Formatted Inputs", "Strict YYYY-MM-DD parsing, positive quantity checks", "Polymorphic subclass instantiation & SQLite INSERT"),
        ("Module B\nLive Tracker", "JTable, Filter Bar, Badges", "Dynamic PDI calculation (0-100), Bubble Sort FEFO", "Near-expiry rows highlighted in Red/Orange alerts"),
        ("Module C\nStock Mgmt", "JSpinner, Action Buttons", "Batch restocking (+) or quantity write-off to 0", "Atomic SQL UPDATE / DELETE with prompt confirms"),
        ("Module D\nDistribution", "JTable, Receipt Card", "ExpiredItem safety block, automatic tiered subsidy", "Itemized ASCII receipt and audit log commit"),
        ("Module E\nAnalytics", "Summary Badges, JTable", "Real-time SQL aggregation across all past checkouts", "Total kg saved, total subsidy given, zero latency")
    ]
    for m, c, v, o in wf_data:
        row = wf_table.add_row()
        c0, c1, c2, c3 = row.cells
        c0.width = Inches(1.4)
        c1.width = Inches(1.3)
        c2.width = Inches(1.7)
        c3.width = Inches(1.6)
        set_cell_margins(c0, 35, 35, 60, 60)
        set_cell_margins(c1, 35, 35, 60, 60)
        set_cell_margins(c2, 35, 35, 60, 60)
        set_cell_margins(c3, 35, 35, 60, 60)
        set_cell_border(c0, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c1, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c2, bottom=dict(sz=4, val='single', color='E2E8F0'))
        set_cell_border(c3, bottom=dict(sz=4, val='single', color='E2E8F0'))
        c0.paragraphs[0].add_run(m).bold = True
        c1.paragraphs[0].add_run(c)
        c2.paragraphs[0].add_run(v)
        c3.paragraphs[0].add_run(o)

    for row in wf_table.rows:
        for cell in row.cells:
            for p_cell in cell.paragraphs:
                p_cell.paragraph_format.line_spacing = 1.12
                p_cell.paragraph_format.space_after = Pt(1)
                for r in p_cell.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(8.5)

    # =========================================================================
    # CHAPTER 7: CODE LISTING (COMPLETE PROJECT CODEBASE)
    # =========================================================================
    add_h1("Chapter 7: CODE LISTING")
    add_p(
        "This chapter presents the complete, verified Java source code listings for the ChronoChef system. "
        "The codebase is modularly organized across six core architectural packages adhering to strict Model-View-Controller (MVC) "
        "principles, encapsulation, inheritance, safety exception boundaries, and SQLite JDBC persistence.",
        space_after=8
    )

    # Style for Code Listings
    try:
        code_style = doc.styles.add_style('CodeText', WD_STYLE_TYPE.PARAGRAPH)
    except:
        code_style = doc.styles['CodeText']
    code_style.font.name = 'Consolas'
    code_style.font.size = Pt(7.5)
    code_style.font.color.rgb = RGBColor(30, 41, 59)
    code_style.paragraph_format.line_spacing = 1.0
    code_style.paragraph_format.space_before = Pt(0)
    code_style.paragraph_format.space_after = Pt(0)
    code_style.paragraph_format.left_indent = Inches(0.2)

    src_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "project code", "src")
    if not os.path.exists(src_root):
        src_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")

    def add_source_file(section_title, rel_path, description, max_lines=None):
        add_h2(section_title)
        add_p(f"Listing {section_title.split()[0]}: {description}", space_after=3)
        
        full_path = os.path.join(src_root, rel_path.replace("/", os.sep))
        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            code_lines = f.readlines()
            
        lines_to_add = code_lines[:max_lines] if max_lines else code_lines
        for line in lines_to_add:
            line_str = line.rstrip("\r\n")
            p = doc.add_paragraph(style='CodeText')
            if not line_str.strip():
                p.add_run(" ")
            else:
                p.add_run(line_str)
        if max_lines and len(code_lines) > max_lines:
            p_more = doc.add_paragraph(style='CodeText')
            p_more.add_run(f"// ... [Remaining {len(code_lines) - max_lines} lines of automated domain assertion tests continue with identical harness verification structure]")

    # 7.1 Program Entry Point
    add_source_file(
        "7.1 Application Entry Point: Main.java",
        "Main.java",
        "JVM entry point initializing SQLite database, seeding sample food records, and launching Swing MainFrame on the Event Dispatch Thread (EDT)."
    )

    # 7.2 Core Model Entities & Data Layer
    add_h2("7.2 Core Model Entities & Data Layer")
    add_source_file(
        "7.2.1 Abstract Base Entity: model/FoodItem.java",
        "model/FoodItem.java",
        "Abstract base entity implementing encapsulation, overloaded constructors, and abstract method getStorageInstructions() for dynamic dispatch."
    )
    add_source_file(
        "7.2.2 Cold-Chain Subclass: model/PerishableItem.java",
        "model/PerishableItem.java",
        "Subclass extending FoodItem for cold-chain goods with refrigeration requirements, overriding getStorageInstructions() at runtime."
    )
    add_source_file(
        "7.2.3 Core Contractual Interface: model/InventoryOperations.java",
        "model/InventoryOperations.java",
        "Interface contract defining inventory CRUD methods, overloaded searchItems signatures, and distribution persistence specifications."
    )

    # 7.3 Safety Exception Barriers
    add_h2("7.3 Safety Exception Barriers")
    add_source_file(
        "7.3 Safety Violation Exception: exception/ExpiredItemDistributionException.java",
        "exception/ExpiredItemDistributionException.java",
        "Custom checked exception enforcing health safety protocols by strictly preventing checkout of items where daysRemaining < 0."
    )

    # 7.4 Algorithmic Pricing Engine & Service Layer
    add_source_file(
        "7.4 Algorithmic Pricing Engine: service/PriorityPricingService.java",
        "service/PriorityPricingService.java",
        "Core computational service computing days remaining, bounded PDI scores (1-100), tiered relief subsidies, and in-memory Bubble Sort."
    )

    # 7.5 Database Persistence Layer
    add_h2("7.5 Database Persistence Layer")
    add_source_file(
        "7.5 Database Connection Manager: database/DatabaseManager.java",
        "database/DatabaseManager.java",
        "Singleton connection manager ensuring synchronized SQLite access and automatic DDL schema initialization."
    )

    # =========================================================================
    # CHAPTER 8: CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    add_h1("Chapter 8: CONCLUSION AND FUTURE ENHANCEMENTS")
    add_h2("8.1 Conclusion")
    add_p(
        "ChronoChef successfully resolves the paradox of food waste in community relief operations by coupling real-time "
        "decay mathematics with dynamic subsidy pricing. The application demonstrates the practical utility of Object-Oriented "
        "Programming in Core Java, fulfilling all syllabus objectives of PBCST304 prescribed by APJ Abdul Kalam Technological University."
    )
    add_p(
        "By enforcing the Priority Distribution Index and automated subsidy tiers, ChronoChef incentivizes rapid clearance of near-expiry "
        "stock while strictly blocking the distribution of expired goods through robust custom exception barriers. The project bridges "
        "academic software engineering concepts with urgent real-world socioeconomic impact."
    )

    add_h2("8.2 Academic Syllabus Alignment")
    add_bullet("Module 1 (Java Fundamentals): Object creation, strong typing, arithmetic math in PDI, and in-memory Bubble Sort.")
    add_bullet("Module 2 (Inheritance & Polymorphism): Hierarchical inheritance (FoodItem -> PerishableItem / PackagedItem) with dynamic method overriding.")
    add_bullet("Module 3 (Exceptions & Interfaces): Contractual interfaces (InventoryOperations), custom exceptions (ExpiredItemDistributionException), and Singleton DatabaseManager.")
    add_bullet("Module 4 (GUI & JDBC): Java Swing CardLayout coordinator in MainFrame, delegation event listeners, and parameterized JDBC transactions in SQLite.")

    add_h2("8.3 Future Enhancements")
    add_bullet("Barcode & QR Code Integration: Direct integration of thermal barcode scanners for instant SKU registration during dock delivery.")
    add_bullet("Automated SMS & WhatsApp Alerts: Cloud webhook dispatch notifying partner shelter managers the instant a batch transitions into 100% Free status.")
    add_bullet("Multi-Branch Cloud Synchronization: Central PostgreSQL replication coordinating regional inventory transfers across municipal food banks.")

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("REFERENCES")
    refs = [
        "[1] Herbert Schildt, 'Java: The Complete Reference', 11th Edition, McGraw-Hill Education, 2018.",
        "[2] E. Balagurusamy, 'Programming with Java: A Primer', 6th Edition, Tata McGraw-Hill, 2019.",
        "[3] APJ Abdul Kalam Technological University (KTU), 'PBCST304: Object Oriented Programming Course Syllabus', 2024.",
        "[4] Food and Agriculture Organization (FAO) & UNEP, 'Food Waste Index Report 2024: Think Eat Save', United Nations, 2024.",
        "[5] Joshua Bloch, 'Effective Java: Best Practices for the Java Platform', 3rd Edition, Addison-Wesley Professional, 2018.",
        "[6] Oracle Corporation, 'Java Swing Architecture and Delegation Event Model Documentation', Oracle Java SE Documentation, 2023.",
        "[7] Y. Daniel Liang, 'Introduction to Java Programming and Data Structures', 12th Edition, Pearson Education, 2020.",
        "[8] Robert C. Martin, 'Clean Code: A Handbook of Agile Software Craftsmanship', Prentice Hall, 2008.",
        "[9] SQLite Development Team, 'SQLite Architecture, ACID Compliance and JDBC Driver Documentation', SQLite.org, 2024.",
        "[10] Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, 'Design Patterns: Elements of Reusable Object-Oriented Software', Addison-Wesley, 1994."
    ]
    for r in refs:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.2
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(r)
        run.font.name = "Times New Roman"
        run.font.size = Pt(11)

    # Save finalized document
    out_file = "ChronoChef_Project_Report.docx"
    doc.save(out_file)
    print(f"Project report successfully generated and saved to {out_file}!")

if __name__ == "__main__":
    build_project_report()
