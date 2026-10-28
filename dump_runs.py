import docx

doc = docx.Document(r'reference formate\PROJECT REPORT PBCST304_Projectreport FormatDemo.docx')
for i in range(65):
    p = doc.paragraphs[i]
    runs_info = []
    for r in p.runs:
        img = "[IMG]" if "drawing" in r._element.xml else ""
        runs_info.append(f"{img}{repr(r.text)}({r.font.name},{r.font.size},{'B' if r.bold else ''})")
    print(f"P{i:02d} [{p.style.name}] (align={p.alignment}): {' '.join(runs_info)}")
