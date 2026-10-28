import os
import json

root_dir = os.path.dirname(os.path.abspath(__file__))
codebase = {}

oop_tags = {
    'project code/src/Main.java': ['JVM Entry Point', 'Event Dispatch Thread (EDT)', 'SwingUtilities.invokeLater'],
    'project code/src/model/FoodItem.java': ['Abstract Base Class', 'Encapsulation & Data Hiding', 'Abstract Method (getStorageInstructions)', 'Constructor Overloading'],
    'project code/src/model/PerishableItem.java': ['Hierarchical Inheritance (extends FoodItem)', 'Dynamic Method Dispatch (@Override getStorageInstructions)', 'Cold-Chain Refrigeration Validation'],
    'project code/src/model/PackagedItem.java': ['Hierarchical Inheritance (extends FoodItem)', 'Dynamic Method Dispatch (@Override getStorageInstructions)', 'Ambient Dry Storage Packaging'],
    'project code/src/model/DistributionRecord.java': ['Encapsulation', 'Relief Transaction Tracking', 'Audit Logging'],
    'project code/src/model/InventoryOperations.java': ['Contractual Interface', 'Method Overloading (searchItems)', 'Abstract Method Signatures'],
    'project code/src/exception/ExpiredItemDistributionException.java': ['Custom Checked Exception', 'Food Safety Guardrail', 'Public Health Protection'],
    'project code/src/exception/InvalidQuantityException.java': ['Custom Checked Exception', 'Inventory Invariant Validation'],
    'project code/src/service/PriorityPricingService.java': ['PDI Mathematical Decay Formula', 'In-Memory Bubble Sort', 'Tiered Relief Subsidies'],
    'project code/src/database/DatabaseManager.java': ['Singleton Design Pattern', 'Thread-Safe Synchronized getInstance()', 'DDL Schema Creation', 'JDBC SQLite Connection'],
    'project code/src/database/FoodBankDAO.java': ['Interface Realization (implements InventoryOperations)', 'JDBC PreparedStatements (SQL Injection Defense)', 'ResultSet Mapping', 'Exception Propagation'],
    'project code/src/database/DataSeeder.java': ['Data Seeder Pattern', 'Polymorphic Collection Initialization'],
    'project code/src/ui/MainFrame.java': ['Master Window (JFrame)', 'CardLayout Deck Navigation', 'Delegation Event Model', 'Menu & Theme Management'],
    'project code/src/ui/InputPanel.java': ['Swing JPanel', 'CardLayout View (Module A)', 'Input Validation & Dynamic Field Toggling'],
    'project code/src/ui/InventoryPanel.java': ['Swing JPanel', 'CardLayout View (Module B)', 'Real-Time PDI Urgency Badges', 'FEFO Prioritized Sorting Table'],
    'project code/src/ui/ManagementPanel.java': ['Swing JPanel', 'CardLayout View (Module C)', 'Stock Restocking & Write-Off', 'JOptionPane Dialogs'],
    'project code/src/ui/DistributionPanel.java': ['Swing JPanel', 'CardLayout View (Module D)', 'Dynamic Subsidy Billing', 'Safety Exception Interception', 'ASCII Receipt Generator'],
    'project code/src/ui/AnalyticsPanel.java': ['Swing JPanel', 'CardLayout View (Module E)', 'Social Impact Metrics', 'Audit History Log'],
    'project code/src/test/ProjectTestRunner.java': ['Automated Verification Harness', '35-Point Assertion Suite', 'Boundary Condition Verification'],
    'project code/src/test/CaptureScreenshots.java': ['Headless & Interactive Screenshot Generation', 'Visual Verification']
}

def get_file_type(fname):
    ext = os.path.splitext(fname)[1].lower()
    mapping = {
        '.java': 'Java Source',
        '.py': 'Python Script',
        '.js': 'JavaScript',
        '.html': 'HTML5',
        '.css': 'CSS3',
        '.bat': 'Batch Script',
        '.md': 'Markdown Documentation',
        '.json': 'JSON Configuration'
    }
    return mapping.get(ext, 'Source File')

# 1. Add all Java files in project code/src
src_dir = os.path.join(root_dir, 'project code', 'src')
for root, dirs, files in os.walk(src_dir):
    for f in sorted(files):
        if f.endswith('.java'):
            full_p = os.path.join(root, f)
            rel_from_root = os.path.relpath(full_p, root_dir).replace('\\', '/')
            with open(full_p, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            lines = content.splitlines()

            pkg = ''
            cls_name = f.replace('.java', '')
            cls_type = 'Java Class'
            for line in lines[:30]:
                if line.startswith('package '):
                    pkg = line.replace('package ', '').replace(';', '').strip()
                if 'abstract class ' in line:
                    cls_type = 'Abstract Class'
                elif 'interface ' in line:
                    cls_type = 'Interface'
                elif 'extends Exception' in line:
                    cls_type = 'Custom Exception'
                elif 'extends JFrame' in line:
                    cls_type = 'Swing JFrame'
                elif 'extends JPanel' in line:
                    cls_type = 'Swing JPanel'

            codebase[rel_from_root] = {
                'path': rel_from_root,
                'fileName': f,
                'category': 'Java Codebase',
                'package': pkg or 'default',
                'className': cls_name,
                'classType': cls_type,
                'linesCount': len(lines),
                'size': len(content),
                'oopTags': oop_tags.get(rel_from_root, ['Core Java OOP']),
                'content': content
            }

# 2. Add Project scripts & Batch runners
extra_files = [
    ('compile.bat', 'Automation & Build Scripts', 'Batch Script'),
    ('run.bat', 'Automation & Build Scripts', 'Batch Script'),
    ('run_tests.bat', 'Automation & Build Scripts', 'Batch Script'),
    ('generate_project_report.py', 'Academic Report Generators', 'Python Script'),
    ('generate_oop_concepts_pdf.py', 'Academic Report Generators', 'Python Script'),
    ('convert_to_pdf.py', 'Academic Report Generators', 'Python Script'),
    ('app.js', 'Web Application Runtime', 'JavaScript'),
    ('index.html', 'Web Application Runtime', 'HTML5'),
    ('index.css', 'Web Application Runtime', 'CSS3'),
    ('vercel.json', 'Deployment Configuration', 'JSON Configuration'),
    ('README.md', 'Documentation', 'Markdown Documentation'),
    ('PROJECT_EXPLANATION_AND_VIVA_GUIDE.md', 'Documentation', 'Markdown Documentation')
]

for fname, category, ftype in extra_files:
    full_p = os.path.join(root_dir, fname)
    if os.path.exists(full_p):
        with open(full_p, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        lines = content.splitlines()
        codebase[fname] = {
            'path': fname,
            'fileName': fname,
            'category': category,
            'package': category,
            'className': fname,
            'classType': ftype,
            'linesCount': len(lines),
            'size': len(content),
            'oopTags': [category, ftype],
            'content': content
        }

js_output = 'const CHRONOCHEF_CODEBASE = ' + json.dumps(codebase, indent=2) + ';\n'
with open(os.path.join(root_dir, 'project_codebase.js'), 'w', encoding='utf-8') as fh:
    fh.write(js_output)

print(f"Generated complete project_codebase.js with {len(codebase)} files!")
total_lines = sum(f['linesCount'] for f in codebase.values())
print(f"Total lines across all files: {total_lines:,} lines")
