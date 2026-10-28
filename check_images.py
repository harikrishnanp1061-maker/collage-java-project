import docx
import re

doc = docx.Document(r'reference formate\PROJECT REPORT PBCST304_Projectreport FormatDemo.docx')
for i in [22, 30]:
    p = doc.paragraphs[i]
    for r in p.runs:
        xml = r._element.xml
        if 'blip' in xml:
            embeds = re.findall(r'r:embed="([^"]+)"', xml)
            for emb in embeds:
                target = doc.part.rels[emb].target_ref
                print(f"Paragraph {i} uses {emb} -> {target}")
