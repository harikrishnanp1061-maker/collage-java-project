import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette Definitions
    DARK_BG = RGBColor(15, 23, 42)      # #0F172A
    NAVY_PRIMARY = RGBColor(30, 58, 138) # #1E3A8A
    TEAL_ACCENT = RGBColor(13, 148, 136) # #0D9488
    AMBER_GOLD = RGBColor(245, 158, 11)  # #F59E0B
    LIGHT_BG = RGBColor(248, 250, 252)  # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)   # #FFFFFF
    CARD_BORDER = RGBColor(203, 213, 225) # #CBD5E1
    TEXT_MAIN = RGBColor(30, 41, 59)    # #1E293B
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    TEXT_LIGHT = RGBColor(241, 245, 249) # #F1F5F9
    TAG_BG = RGBColor(238, 242, 255)    # #EEF2FF
    SUCCESS_GREEN = RGBColor(16, 185, 129)

    blank_layout = prs.slide_layouts[6]

    # Helper: Set slide background color
    def set_slide_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # Helper: Add Standard Header
    def add_header(slide, kicker, title, slide_num=None):
        # Kicker / Category tag
        tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = kicker.upper()
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEAL_ACCENT

        # Main Title
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Arial"
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = NAVY_PRIMARY

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        if slide_num:
            num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.0), Inches(1.0), Inches(0.3))
            np = num_box.text_frame.paragraphs[0]
            np.text = f"{slide_num:02d} / 10"
            np.alignment = PP_ALIGN.RIGHT
            np.font.size = Pt(10)
            np.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 1: FRONT PAGE (TITLE SLIDE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1, DARK_BG)

    # Decorative header band
    band = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.15))
    band.fill.solid()
    band.fill.fore_color.rgb = AMBER_GOLD
    band.line.fill.background()

    # Official College Logos
    if os.path.exists("assets/college_logo.png"):
        s1.shapes.add_picture("assets/college_logo.png", Inches(0.8), Inches(0.55), height=Inches(0.75))
    if os.path.exists("assets/college_emblem.png"):
        s1.shapes.add_picture("assets/college_emblem.png", Inches(10.5), Inches(0.55), height=Inches(0.75))

    # College & Department Banner
    college_box = s1.shapes.add_textbox(Inches(2.8), Inches(0.65), Inches(7.733), Inches(1.0))
    tf1 = college_box.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "MARIAN ENGINEERING COLLEGE, THIRUVANANTHAPURAM"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER_GOLD
    p.alignment = PP_ALIGN.CENTER

    p_dept = tf1.add_paragraph()
    p_dept.text = "DEPARTMENT OF ARTIFICIAL INTELLIGENCE & MACHINE LEARNING"
    p_dept.font.name = "Arial"
    p_dept.font.size = Pt(11)
    p_dept.font.color.rgb = RGBColor(148, 163, 184)
    p_dept.alignment = PP_ALIGN.CENTER

    # Project Title Card (Center Glassmorphism style)
    title_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(2.0), Inches(11.333), Inches(2.6))
    title_card.fill.solid()
    title_card.fill.fore_color.rgb = RGBColor(23, 37, 84) # Deep Blue
    title_card.line.color.rgb = RGBColor(59, 130, 246)
    title_card.line.width = Pt(1.5)

    tt_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.15), Inches(10.933), Inches(2.3))
    ttf = tt_box.text_frame
    ttf.word_wrap = True
    
    tp1 = ttf.paragraphs[0]
    tp1.text = "CHRONOCHEF: SMART DYNAMIC PRICING &\nEXPIRY TRACKER FOR FOOD BANKS"
    tp1.font.name = "Arial"
    tp1.font.size = Pt(28)
    tp1.font.bold = True
    tp1.font.color.rgb = RGBColor(255, 255, 255)
    tp1.alignment = PP_ALIGN.CENTER

    tp2 = ttf.add_paragraph()
    tp2.text = "Course: PBCST304 — Object Oriented Programming (Third Semester B.Tech Project)"
    tp2.font.name = "Arial"
    tp2.font.size = Pt(13)
    tp2.font.bold = True
    tp2.font.color.rgb = AMBER_GOLD
    tp2.alignment = PP_ALIGN.CENTER

    tp3 = ttf.add_paragraph()
    tp3.text = "Prescribed by APJ Abdul Kalam Technological University (KTU), Kerala | Academic Year 2025–2026"
    tp3.font.name = "Arial"
    tp3.font.size = Pt(11)
    tp3.font.color.rgb = RGBColor(203, 213, 225)
    tp3.alignment = PP_ALIGN.CENTER

    # Left Card: Student Credentials
    s_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.9), Inches(5.4), Inches(1.9))
    s_card.fill.solid()
    s_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    s_card.line.color.rgb = CARD_BORDER
    s_card.line.width = Pt(1)

    s_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.0), Inches(5.0), Inches(1.7))
    stf = s_box.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "SUBMITTED BY:"
    sp1.font.name = "Arial"
    sp1.font.size = Pt(11)
    sp1.font.bold = True
    sp1.font.color.rgb = AMBER_GOLD

    sp2 = stf.add_paragraph()
    sp2.text = "• Harikrishnan & Project Batch Members\n• Third Semester, B.Tech AI & ML\n• Marian Engineering College"
    sp2.font.name = "Arial"
    sp2.font.size = Pt(11)
    sp2.font.color.rgb = TEXT_LIGHT

    # Right Card: Project Guidance & Faculty
    g_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.933), Inches(4.9), Inches(5.4), Inches(1.9))
    g_card.fill.solid()
    g_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    g_card.line.color.rgb = CARD_BORDER
    g_card.line.width = Pt(1)

    g_box = s1.shapes.add_textbox(Inches(7.133), Inches(5.0), Inches(5.0), Inches(1.7))
    gtf = g_box.text_frame
    gtf.word_wrap = True
    gp1 = gtf.paragraphs[0]
    gp1.text = "UNDER THE SUPERVISION & GUIDANCE OF:"
    gp1.font.name = "Arial"
    gp1.font.size = Pt(11)
    gp1.font.bold = True
    gp1.font.color.rgb = AMBER_GOLD

    gp2 = gtf.add_paragraph()
    gp2.text = "Ms. Renetha J B\nAssistant Professor, Dept. of Computer Science & Engineering\nMarian Engineering College, Thiruvananthapuram"
    gp2.font.name = "Arial"
    gp2.font.size = Pt(11)
    gp2.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 2: CONTENTS PAGE (AGENDA)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2, LIGHT_BG)
    add_header(s2, "Overview & Roadmap", "Table of Contents", 2)

    contents_items = [
        ("01", "Introduction", "Problem statement, food bank challenges, and modern software-driven solutions"),
        ("02", "Objectives", "Core goals: automated inventory tracking, zero food waste, and food safety guarantees"),
        ("03", "Requirement Specification", "Detailed hardware platform parameters, OS, Java Runtime, SQLite, and libraries"),
        ("04", "Design Document", "System MVC architecture, Object-Oriented Class Hierarchy, and SQLite Database ER schema"),
        ("05", "Results & Outputs", "Comprehensive visual walkthrough across all 5 Swing modules with output screenshots"),
        ("06", "Conclusion & Future Work", "Summary of achievements, KTU OOP syllabus mapping, social impact, and future vision")
    ]

    card_coords = [
        (Inches(0.8), Inches(1.6), Inches(5.6), Inches(1.5)),
        (Inches(6.9), Inches(1.6), Inches(5.6), Inches(1.5)),
        (Inches(0.8), Inches(3.4), Inches(5.6), Inches(1.5)),
        (Inches(6.9), Inches(3.4), Inches(5.6), Inches(1.5)),
        (Inches(0.8), Inches(5.2), Inches(5.6), Inches(1.5)),
        (Inches(6.9), Inches(5.2), Inches(5.6), Inches(1.5)),
    ]

    for (num, title, desc), (x, y, w, h) in zip(contents_items, card_coords):
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)

        # Number badge
        badge = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), y + Inches(0.25), Inches(0.9), Inches(0.9))
        badge.fill.solid()
        badge.fill.fore_color.rgb = NAVY_PRIMARY
        badge.line.fill.background()
        bp = badge.text_frame.paragraphs[0]
        bp.text = num
        bp.font.name = "Arial"
        bp.font.size = Pt(20)
        bp.font.bold = True
        bp.font.color.rgb = RGBColor(255, 255, 255)
        bp.alignment = PP_ALIGN.CENTER

        # Text box
        tb = s2.shapes.add_textbox(x + Inches(1.3), y + Inches(0.2), w - Inches(1.5), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = tf.margin_left = tf.margin_right = tf.margin_bottom = 0
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_PRIMARY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: 1 INTRODUCTION
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3, LIGHT_BG)
    add_header(s3, "Section 1", "1. Introduction: Problem Statement & Solution", 3)

    # 3 Key Insight Cards
    # Card 1: Problem Background
    c1 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.6), Inches(3.6), Inches(5.1))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = RGBColor(239, 68, 68) # Red alert border
    c1.line.width = Pt(1.5)

    tb1 = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.2), Inches(4.7))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "THE PROBLEM"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(220, 38, 38)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Food Insecurity vs Waste\n"
    p_sub.font.name = "Arial"
    p_sub.font.size = Pt(16)
    p_sub.font.bold = True
    p_sub.font.color.rgb = NAVY_PRIMARY

    bullets1 = [
        "Millions of tons of edible food are discarded annually due to unorganized manual tracking in charity food banks.",
        "Static pricing creates bottlenecks: items sit on shelves until expiration instead of being subsidized.",
        "Manual paper or spreadsheet logs lead to accidental distribution of expired products.",
        "Lack of real-time inventory visibility and automated prioritization mechanisms."
    ]
    for b in bullets1:
        pb = tf1.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_MAIN
        pb.space_after = Pt(6)

    # Card 2: The Solution - ChronoChef
    c2 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.6), Inches(3.7), Inches(5.1))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = NAVY_PRIMARY
    c2.line.width = Pt(1.5)

    tb2 = s3.shapes.add_textbox(Inches(5.0), Inches(1.8), Inches(3.3), Inches(4.7))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "THE SOLUTION"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    p_sub2 = tf2.add_paragraph()
    p_sub2.text = "ChronoChef Platform\n"
    p_sub2.font.name = "Arial"
    p_sub2.font.size = Pt(16)
    p_sub2.font.bold = True
    p_sub2.font.color.rgb = NAVY_PRIMARY

    bullets2 = [
        "A desktop-based Java application developed using Model-View-Controller (MVC) architecture.",
        "Centralized SQLite Database serving as the single source of truth for food donations.",
        "Priority Distribution Index (PDI) algorithm that ranks items continuously based on urgency.",
        "Automated Dynamic Subsidy Pricing Tier making expiring food 50% subsidized or 100% Free."
    ]
    for b in bullets2:
        pb = tf2.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_MAIN
        pb.space_after = Pt(6)

    # Card 3: Key Innovations & Impact
    c3 = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.9), Inches(1.6), Inches(3.6), Inches(5.1))
    c3.fill.solid()
    c3.fill.fore_color.rgb = CARD_BG
    c3.line.color.rgb = TEAL_ACCENT
    c3.line.width = Pt(1.5)

    tb3 = s3.shapes.add_textbox(Inches(9.1), Inches(1.8), Inches(3.2), Inches(4.7))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "KEY INNOVATIONS"
    p.font.name = "Arial"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT

    p_sub3 = tf3.add_paragraph()
    p_sub3.text = "Core Innovations\n"
    p_sub3.font.name = "Arial"
    p_sub3.font.size = Pt(16)
    p_sub3.font.bold = True
    p_sub3.font.color.rgb = NAVY_PRIMARY

    bullets3 = [
        "Algorithmic Sorting: Bubble Sort prioritizes critical batches at the top of the interface.",
        "Food Safety Guard: Custom Java Exception strictly blocks checkout of expired goods.",
        "Instant Subsidy Billing: Generates itemized transparent distribution receipts for shelters.",
        "Sustainability Impact: Direct contribution to UN Sustainable Development Goal (SDG 12.3: Zero Hunger & Reduced Food Waste)."
    ]
    for b in bullets3:
        pb = tf3.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(11)
        pb.font.color.rgb = TEXT_MAIN
        pb.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: 2 OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4, LIGHT_BG)
    add_header(s4, "Section 2", "2. Aim and Specific Objectives", 4)

    # Central Aim Banner
    aim_card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(11.733), Inches(1.2))
    aim_card.fill.solid()
    aim_card.fill.fore_color.rgb = RGBColor(238, 242, 255)
    aim_card.line.color.rgb = RGBColor(199, 210, 254)
    aim_card.line.width = Pt(1)

    atb = s4.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.333), Inches(1.0))
    atf = atb.text_frame
    atf.word_wrap = True
    ap1 = atf.paragraphs[0]
    ap1.text = "PROJECT AIM:"
    ap1.font.name = "Arial"
    ap1.font.size = Pt(11)
    ap1.font.bold = True
    ap1.font.color.rgb = NAVY_PRIMARY
    ap2 = atf.add_paragraph()
    ap2.text = "To design and implement an intelligent, object-oriented desktop application for community food banks that tracks food shelf-life, automates dynamic pricing subsidies, and prevents food wastage while upholding strict food safety."
    ap2.font.name = "Arial"
    ap2.font.size = Pt(13)
    ap2.font.bold = True
    ap2.font.color.rgb = TEXT_MAIN

    # 4 Specific Objective Cards in 2x2 grid
    objectives = [
        ("1. Centralized Inventory Management", 
         "Develop an intuitive Java Swing GUI backed by SQLite to record, validate, update, and categorize perishable and packaged food donations with full transactional integrity."),
        ("2. Real-Time Expiry & PDI Computation", 
         "Formulate and deploy the Priority Distribution Index (PDI) scoring formula (0–100) to classify food urgency into Immediate/Urgent, High, Medium, and Low tiers dynamically."),
        ("3. Rule-Based Dynamic Subsidy Engine", 
         "Automate a tiered discount framework: <= 2 days left (100% Free / Rs. 0.00), 3-7 days left (50% Subsidy), and > 7 days left (0% Subsidy / Standard Price) to incentivize swift distribution."),
        ("4. Strict Food Safety & Exception Handling", 
         "Enforce an unbypassable safety barrier preventing expired food from being distributed, leveraging custom exceptions (ExpiredItemDistributionException) and robust validation.")
    ]

    coords_4 = [
        (Inches(0.8), Inches(2.9), Inches(5.7), Inches(1.85)),
        (Inches(6.8), Inches(2.9), Inches(5.7), Inches(1.85)),
        (Inches(0.8), Inches(4.95), Inches(5.7), Inches(1.85)),
        (Inches(6.8), Inches(4.95), Inches(5.7), Inches(1.85))
    ]

    for (title, text), (x, y, w, h) in zip(objectives, coords_4):
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tb = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_ACCENT

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 5: 3 REQUIREMENT SPECIFICATION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5, LIGHT_BG)
    add_header(s5, "Section 3", "3. Requirement Specification", 5)

    # Left Column: Software Requirements
    sw_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.2))
    sw_card.fill.solid()
    sw_card.fill.fore_color.rgb = CARD_BG
    sw_card.line.color.rgb = NAVY_PRIMARY
    sw_card.line.width = Pt(1.5)

    # Header badge inside
    sw_badge = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(1.7), Inches(5.0), Inches(0.5))
    sw_badge.fill.solid()
    sw_badge.fill.fore_color.rgb = NAVY_PRIMARY
    sw_badge.line.fill.background()
    sw_bp = sw_badge.text_frame.paragraphs[0]
    sw_bp.text = "SOFTWARE REQUIREMENTS"
    sw_bp.font.name = "Arial"
    sw_bp.font.size = Pt(12)
    sw_bp.font.bold = True
    sw_bp.font.color.rgb = RGBColor(255, 255, 255)
    sw_bp.alignment = PP_ALIGN.CENTER

    sw_tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(5.0), Inches(4.2))
    sw_tf = sw_tb.text_frame
    sw_tf.word_wrap = True

    sw_items = [
        ("Operating System", "Microsoft Windows 10 / 11 (64-bit), Linux, macOS"),
        ("Programming Language", "Java Standard Edition (Java SE 17 / 21 LTS)"),
        ("GUI Framework", "Java Swing (JFrame, CardLayout, JTable, AWT Events)"),
        ("Database Engine", "SQLite 3.42+ (Zero-configuration file-based DB)"),
        ("Database Connectivity", "JDBC (sqlite-jdbc-3.42.0.0.jar driver)"),
        ("Architecture Pattern", "Model-View-Controller (MVC)"),
        ("Development IDE", "VS Code / Android Studio / IntelliJ IDEA / NetBeans"),
        ("Build Tooling", "Native batch scripts (compile.bat, run.bat)")
    ]

    for label, val in sw_items:
        p = sw_tf.add_paragraph() if sw_tf.paragraphs[0].text else sw_tf.paragraphs[0]
        p.text = f"{label}: "
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_PRIMARY

        run = p.add_run()
        run.text = val
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.bold = False
        run.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(4)

    # Right Column: Hardware Requirements
    hw_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.2))
    hw_card.fill.solid()
    hw_card.fill.fore_color.rgb = CARD_BG
    hw_card.line.color.rgb = TEAL_ACCENT
    hw_card.line.width = Pt(1.5)

    hw_badge = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.7), Inches(5.0), Inches(0.5))
    hw_badge.fill.solid()
    hw_badge.fill.fore_color.rgb = TEAL_ACCENT
    hw_badge.line.fill.background()
    hw_bp = hw_badge.text_frame.paragraphs[0]
    hw_bp.text = "HARDWARE REQUIREMENTS"
    hw_bp.font.name = "Arial"
    hw_bp.font.size = Pt(12)
    hw_bp.font.bold = True
    hw_bp.font.color.rgb = RGBColor(255, 255, 255)
    hw_bp.alignment = PP_ALIGN.CENTER

    hw_tb = s5.shapes.add_textbox(Inches(7.2), Inches(2.35), Inches(5.0), Inches(4.2))
    hw_tf = hw_tb.text_frame
    hw_tf.word_wrap = True

    hw_items = [
        ("Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 or higher (Min 2.0 GHz)"),
        ("System Memory (RAM)", "Minimum: 4 GB RAM | Recommended: 8 GB RAM"),
        ("Storage (Disk Space)", "Minimum 500 MB free space (Project + SQLite DB < 50 MB)"),
        ("Display Resolution", "1280 x 720 (Standard HD) or 1920 x 1080 (Full HD)"),
        ("Input Devices", "Standard QWERTY Keyboard and Mouse / Touchpad"),
        ("Network Requirements", "None (Fully offline standalone desktop operational capability)"),
        ("Portability", "Cross-platform bytecode runnable on any compliant JVM")
    ]

    for label, val in hw_items:
        p = hw_tf.add_paragraph() if hw_tf.paragraphs[0].text else hw_tf.paragraphs[0]
        p.text = f"{label}: "
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL_ACCENT

        run = p.add_run()
        run.text = val
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.bold = False
        run.font.color.rgb = TEXT_MAIN
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 6: 4 DESIGN DOCUMENT - CLASS DIAGRAM
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6, LIGHT_BG)
    add_header(s6, "Section 4.1", "4. Design Document: Object-Oriented Class Diagram", 6)

    # Diagram Image on Left/Center
    if os.path.exists("screenshots/class_diagram.png"):
        s6.shapes.add_picture("screenshots/class_diagram.png", Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.2))

    # Right Side Callout Card: OOP Principles Mapping
    oop_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), Inches(1.5), Inches(3.533), Inches(5.2))
    oop_card.fill.solid()
    oop_card.fill.fore_color.rgb = CARD_BG
    oop_card.line.color.rgb = NAVY_PRIMARY
    oop_card.line.width = Pt(1.5)

    otb = s6.shapes.add_textbox(Inches(9.15), Inches(1.65), Inches(3.2), Inches(4.9))
    otf = otb.text_frame
    otf.word_wrap = True

    p = otf.paragraphs[0]
    p.text = "OOP CONCEPTS APPLIED"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p.space_after = Pt(8)

    concepts = [
        ("Encapsulation", "FoodItem.java: Private fields with validated getters and setters."),
        ("Inheritance", "PerishableItem and PackagedItem extend abstract FoodItem via super()."),
        ("Polymorphism", "Dynamic Method Dispatch in getStorageInstructions() & getItemClassification()."),
        ("Interfaces", "InventoryOperations interface defines contract implemented by FoodBankDAO."),
        ("Singleton Pattern", "DatabaseManager restricts JDBC connection to a single instance."),
        ("Exception Handling", "Custom checked exceptions: ExpiredItemDistributionException.")
    ]

    for title, desc in concepts:
        p1 = otf.add_paragraph()
        p1.text = f"• {title}: "
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEAL_ACCENT

        run = p1.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MAIN
        p1.space_after = Pt(4)

    # =========================================================================
    # SLIDE 7: 4 DESIGN DOCUMENT - DATABASE DESIGN
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7, LIGHT_BG)
    add_header(s7, "Section 4.2", "4. Design Document: Relational Database Schema", 7)

    # Diagram Image
    if os.path.exists("screenshots/database_design.png"):
        s7.shapes.add_picture("screenshots/database_design.png", Inches(0.8), Inches(1.5), Inches(8.0), Inches(5.2))

    # Right Side Callout Card: DB Architecture Highlights
    db_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.0), Inches(1.5), Inches(3.533), Inches(5.2))
    db_card.fill.solid()
    db_card.fill.fore_color.rgb = CARD_BG
    db_card.line.color.rgb = TEAL_ACCENT
    db_card.line.width = Pt(1.5)

    dtb = s7.shapes.add_textbox(Inches(9.15), Inches(1.65), Inches(3.2), Inches(4.9))
    dtf = dtb.text_frame
    dtf.word_wrap = True

    p = dtf.paragraphs[0]
    p.text = "DATABASE HIGHLIGHTS"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p.space_after = Pt(8)

    db_points = [
        ("Zero-Configuration", "Serverless SQLite engine requires no external installation or daemon setup."),
        ("Normalized Tables", "1-to-Many relation connects food_items master table with distribution_records transaction log."),
        ("Atomic Transactions", "When food is distributed, stock reduction and audit receipt logging execute in tandem."),
        ("PreparedStatement", "All queries use parameterized PreparedStatements preventing SQL injection attacks."),
        ("Audit Integrity", "Distribution transactions capture immutable historical price and recipient records.")
    ]

    for title, desc in db_points:
        p1 = dtf.add_paragraph()
        p1.text = f"• {title}: "
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = NAVY_PRIMARY

        run = p1.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MAIN
        p1.space_after = Pt(6)

    # =========================================================================
    # SLIDE 8: 5 RESULTS (SLIDE 1 OF 2 - INTAKE & EXPIRY TRACKING)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8, LIGHT_BG)
    add_header(s8, "Section 5.1", "5. Results: Intake & Live Expiry Tracking (Output Screenshots)", 8)

    # Two Screenshots Side-by-Side: 02_input_panel.png and 01_inventory_tracker.png
    # Image 1: Input Panel
    if os.path.exists("screenshots/02_input_panel.png"):
        s8.shapes.add_picture("screenshots/02_input_panel.png", Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.7))
    
    # Label for Image 1
    l1 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.45), Inches(5.6), Inches(1.3))
    l1.fill.solid()
    l1.fill.fore_color.rgb = CARD_BG
    l1.line.color.rgb = CARD_BORDER
    tb_l1 = s8.shapes.add_textbox(Inches(0.9), Inches(5.5), Inches(5.4), Inches(1.2))
    tf_l1 = tb_l1.text_frame
    tf_l1.word_wrap = True
    p = tf_l1.paragraphs[0]
    p.text = "Module A — Food Donation Intake Interface"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf_l1.add_paragraph()
    p2.text = "Features rigorous input validation (dates, quantities, pricing), item category dropdowns, and dynamic fields based on Perishable vs Packaged item type."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN

    # Image 2: Inventory Panel
    if os.path.exists("screenshots/01_inventory_tracker.png"):
        s8.shapes.add_picture("screenshots/01_inventory_tracker.png", Inches(6.9), Inches(1.6), Inches(5.6), Inches(3.7))

    # Label for Image 2
    l2 = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(5.45), Inches(5.6), Inches(1.3))
    l2.fill.solid()
    l2.fill.fore_color.rgb = CARD_BG
    l2.line.color.rgb = CARD_BORDER
    tb_l2 = s8.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.4), Inches(1.2))
    tf_l2 = tb_l2.text_frame
    tf_l2.word_wrap = True
    p = tf_l2.paragraphs[0]
    p.text = "Module B — Live Expiry & PDI Urgency Tracker"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p2 = tf_l2.add_paragraph()
    p2.text = "Displays color-coded badges for Urgency (CRITICAL / URGENT, HIGH, MEDIUM, LOW, EXPIRED), computes PDI Score (0-100), and auto-orders by shelf-life using Bubble Sort."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 9: 5 RESULTS (SLIDE 2 OF 2 - DISTRIBUTION & ANALYTICS)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9, LIGHT_BG)
    add_header(s9, "Section 5.2", "5. Results: Distribution Billing & Analytics (Output Screenshots)", 9)

    # Two Screenshots Side-by-Side: 04_distribute_billing.png and 05_analytics_dashboard.png
    # Image 1: Distribution & Billing
    if os.path.exists("screenshots/04_distribute_billing.png"):
        s9.shapes.add_picture("screenshots/04_distribute_billing.png", Inches(0.8), Inches(1.6), Inches(5.6), Inches(3.7))

    l3 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.45), Inches(5.6), Inches(1.3))
    l3.fill.solid()
    l3.fill.fore_color.rgb = CARD_BG
    l3.line.color.rgb = CARD_BORDER
    tb_l3 = s9.shapes.add_textbox(Inches(0.9), Inches(5.5), Inches(5.4), Inches(1.2))
    tf_l3 = tb_l3.text_frame
    tf_l3.word_wrap = True
    p = tf_l3.paragraphs[0]
    p.text = "Module D — Dynamic Subsidy Distribution & Billing"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf_l3.add_paragraph()
    p2.text = "Automates tiered subsidy calculation (100% Free / 50% Subsidy / Standard), enforces safety guard blocking expired goods, and renders formatted audit receipts."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN

    # Image 2: Analytics Dashboard
    if os.path.exists("screenshots/05_analytics_dashboard.png"):
        s9.shapes.add_picture("screenshots/05_analytics_dashboard.png", Inches(6.9), Inches(1.6), Inches(5.6), Inches(3.7))

    l4 = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(5.45), Inches(5.6), Inches(1.3))
    l4.fill.solid()
    l4.fill.fore_color.rgb = CARD_BG
    l4.line.color.rgb = CARD_BORDER
    tb_l4 = s9.shapes.add_textbox(Inches(7.0), Inches(5.5), Inches(5.4), Inches(1.2))
    tf_l4 = tb_l4.text_frame
    tf_l4.word_wrap = True
    p = tf_l4.paragraphs[0]
    p.text = "Module E — Inventory Analytics & Distribution Log"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TEAL_ACCENT
    p2 = tf_l4.add_paragraph()
    p2.text = "Aggregates 6 key performance indicator cards (Total Items, Available Stock, Urgent Batches, Expired Volume, Total Subsidy Granted) and full audit history."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN

    # =========================================================================
    # SLIDE 10: 6 CONCLUSION & FUTURE ENHANCEMENTS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10, DARK_BG)

    # Header in dark theme
    tx_box = s10.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SECTION 6"
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = AMBER_GOLD

    p2 = tf.add_paragraph()
    p2.text = "6. Conclusion, Syllabus Mapping & Future Enhancements"
    p2.font.name = "Arial"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(255, 255, 255)

    line = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.02))
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(51, 65, 85)
    line.line.fill.background()

    # 4 Achievement Metric Cards
    metrics = [
        ("100%", "Zero-Waste Clearance", "Near-expiry goods distributed rapidly at 100% subsidy / Rs. 0.00."),
        ("35 / 35", "Test Verification", "All 35 automated unit and integration tests passing successfully."),
        ("0 Expired", "Food Safety Barrier", "Zero expired items distributed due to strict exception enforcement."),
        ("Full MVC", "KTU Syllabus Alignment", "Demonstrates Modules 1-4: Abstraction, OOP, Swings, and JDBC.")
    ]

    m_x = Inches(0.8)
    for num, title, desc in metrics:
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m_x, Inches(1.5), Inches(2.75), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(30, 41, 59)
        card.line.color.rgb = RGBColor(71, 85, 105)

        tb = s10.shapes.add_textbox(m_x + Inches(0.15), Inches(1.6), Inches(2.45), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = num
        p1.font.name = "Arial"
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = AMBER_GOLD

        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = RGBColor(255, 255, 255)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Arial"
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = RGBColor(148, 163, 184)

        m_x += Inches(2.99)

    # Bottom Two Large Cards: Key Learnings vs Future Enhancements
    # Left Bottom Card
    c_learn = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(5.7), Inches(3.4))
    c_learn.fill.solid()
    c_learn.fill.fore_color.rgb = RGBColor(23, 37, 84) # Deep Blue
    c_learn.line.color.rgb = RGBColor(59, 130, 246)
    c_learn.line.width = Pt(1)

    tb_l = s10.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(5.3), Inches(3.1))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "ACADEMIC & PRACTICAL LEARNINGS"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.space_after = Pt(6)

    learnings = [
        "Rigorous application of OOP Principles: Abstraction, Hierarchical Inheritance, and Dynamic Method Overriding.",
        "Practical JDBC mastery with SQLite, transactions, and robust Resource Management (try-catch-finally).",
        "Clean GUI design using Java Swing CardLayout, custom JTable cell renderers, and Delegation Event handling.",
        "Algorithmic thinking: Priority Distribution Index (PDI) scoring directly solving real-world food logistics waste."
    ]
    for b in learnings:
        pb = tf_l.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(10)
        pb.font.color.rgb = RGBColor(241, 245, 249)
        pb.space_after = Pt(4)

    # Right Bottom Card
    c_future = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.3), Inches(5.7), Inches(3.4))
    c_future.fill.solid()
    c_future.fill.fore_color.rgb = RGBColor(19, 78, 74) # Deep Teal
    c_future.line.color.rgb = RGBColor(45, 212, 191)
    c_future.line.width = Pt(1)

    tb_f = s10.shapes.add_textbox(Inches(7.0), Inches(3.45), Inches(5.3), Inches(3.1))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    p = tf_f.paragraphs[0]
    p.text = "FUTURE ENHANCEMENTS"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(94, 234, 212)
    p.space_after = Pt(6)

    futures = [
        "Barcode & QR Code Scanning: Integration with USB barcode readers for instant donation intake.",
        "SMS & Push Notifications: Automated alerts to partner charities when items enter the 100% Free tier.",
        "Cloud Sync & Multi-Branch Support: Migration to cloud database (PostgreSQL) for multi-location food banks.",
        "AI-Driven Demand Forecasting: Machine learning models predicting demand cycles to optimize inventory."
    ]
    for b in futures:
        pb = tf_f.add_paragraph()
        pb.text = "• " + b
        pb.font.size = Pt(10)
        pb.font.color.rgb = RGBColor(241, 245, 249)
        pb.space_after = Pt(4)

    out_path = "ChronoChef_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation successfully saved to {out_path}!")

if __name__ == "__main__":
    build_presentation()
