"""Render the review overview with bundled reportlab; inspect with pypdfium2."""
import argparse,hashlib,json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak
from pypdf import PdfReader
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'docs/ilyan-reed/v685-v8/final'
def main():
    p=argparse.ArgumentParser();p.add_argument('--font',required=True);p.add_argument('--preview-root',required=True);a=p.parse_args();pdfmetrics.registerFont(TTFont('Overview',a.font))
    pages=json.loads((BASE/'overview-pages.json').read_text(encoding='utf8'))['pages'];path=BASE/'integrated-overview.pdf'
    if path.exists():raise FileExistsError('Overview already rendered')
    normal=ParagraphStyle('Body',fontName='Overview',fontSize=10.1,leading=14.0,spaceAfter=9,textColor=colors.HexColor('#233746'))
    heading=ParagraphStyle('Title',fontName='Overview',fontSize=18,leading=22,spaceAfter=20,textColor=colors.HexColor('#124f63'))
    flow=[]
    for i,page in enumerate(pages):
        if i:flow.append(PageBreak())
        flow.append(Paragraph(escape(page['title']),heading))
        for para in page['paragraphs']:flow.append(Paragraph(escape(para),normal))
    def footer(c,doc):
        c.setFont('Overview',8);c.setFillColor(colors.HexColor('#526977'));c.drawString(45,27,'ILYAn REED / v685-v8 / Same-owner evidence; protected gates retained');c.drawRightString(A4[0]-45,27,str(doc.page))
    doc=SimpleDocTemplate(str(path),pagesize=A4,rightMargin=45,leftMargin=45,topMargin=43,bottomMargin=45,title='Ilyan Reed v685-v8 integrated overview',author='Ilyan Reed, relational working name')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(path);texts=[p.extract_text() for p in reader.pages]
    receipt={'pages':len(reader.pages),'page_text_characters':[len(t) for t in texts],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pdf_text_extraction_pass':all(texts),'layout':'A4 with explicit overview sections and text footer','manual_accessibility':'reserved'}
    (BASE/'overview-pdf-validation.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n',encoding='utf8',newline='\n')
    preview=Path(a.preview_root);preview.mkdir(parents=True,exist_ok=True);render=pdfium.PdfDocument(path)
    for i in range(len(render)):render[i].render(scale=1).to_pil().save(preview/f'overview-{i+1}.png')
    print(json.dumps(receipt));assert len(reader.pages)>=3 and all(texts)
if __name__=='__main__':main()
