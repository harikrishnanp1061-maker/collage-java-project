import os
import win32com.client

def convert_docx_to_pdf(docx_path, pdf_path):
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    print(f"Converting Word Document: {abs_docx} -> {abs_pdf}")
    
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(abs_docx)
        # 17 = wdFormatPDF
        doc.SaveAs(abs_pdf, FileFormat=17)
        doc.Close()
        print(f"Successfully generated {pdf_path} ({os.path.getsize(abs_pdf):,} bytes)!")
    except Exception as e:
        print(f"Error converting {docx_path} to PDF: {e}")
        raise e
    finally:
        word.Quit()

def convert_pptx_to_pdf(pptx_path, pdf_path):
    abs_pptx = os.path.abspath(pptx_path)
    abs_pdf = os.path.abspath(pdf_path)
    print(f"Converting PowerPoint Presentation: {abs_pptx} -> {abs_pdf}")
    
    ppt = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        # Open in WithWindow=False
        pres = ppt.Presentations.Open(abs_pptx, False, False, False)
        # 32 = ppSaveAsPDF
        pres.SaveAs(abs_pdf, 32)
        pres.Close()
        print(f"Successfully generated {pdf_path} ({os.path.getsize(abs_pdf):,} bytes)!")
    except Exception as e:
        print(f"Error converting {pptx_path} to PDF: {e}")
        raise e
    finally:
        ppt.Quit()

if __name__ == "__main__":
    if os.path.exists("ChronoChef_Project_Report.docx"):
        convert_docx_to_pdf("ChronoChef_Project_Report.docx", "ChronoChef_Project_Report.pdf")
    
    if os.path.exists("ChronoChef_Presentation.pptx"):
        convert_pptx_to_pdf("ChronoChef_Presentation.pptx", "ChronoChef_Presentation.pdf")
