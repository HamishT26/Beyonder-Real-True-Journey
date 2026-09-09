from pathlib import Path
import hashlib,html,json,os
from fractions import Fraction

BANK=Path(__file__).parent
os.environ['MPLCONFIGDIR']=str(BANK/'plot-cache')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from pypdf import PdfReader

BASE=Path('D:/GHC-Archives/worktrees/rowan-ash-main/docs/rowan-ash/v689-v5')
OUT=BASE/'final';FIG=OUT/'figures';FIG.mkdir(exist_ok=True)
receipt=json.loads((BASE/'x2/interpretation-receipt.json').read_bytes())
baton=json.loads((OUT/'baton-module-index.json').read_bytes())
navy='#163449';teal='#1d7a74';rust='#a44332';muted='#506675'

pages=[
{'title':'Finite structures, visible assumptions','subtitle':'Rowan Ash | v689-v5 | GHC Family research',
 'lead':'Both execution tranches are complete. The 200 explicit main contracts produced 180 completed, 10 represented, five open-gap and five exact-gate outcomes. The larger scientific and authority verdict remains NOT_READY_FOR_STAGE_20.',
 'paragraphs':[
 ('What the work adds','The new evaluator works on supplied vertices, edges, facets, coefficients and potentials. It computes exact simplicial boundaries, graph structure, rational Betti numbers, cochain pairings, weighted Laplacians and boundary-value solutions. Frozen expected values are separate from the implementation.'),
 ('An inspectable execution record','Each session also ran 100 candidate rejection probes and 100 lossless source-record refinements. The rejected subjects receive zero success credit. The refinements reorganize inherited records; they are not new source experiments or host cleanups.'),
 ('Separate lifecycle boundaries','Planning, x1, x2 and final closeout are distinct commits. The source is Elaren final d0707cbb9949; Rowan planning is b1fd358f5197, x1 is 6ea658e58077 and x2 is 53f60df33797. The external final receipt binds the later exact final and canonical outcome.'),
 ('Scope','The work is finite, synthetic and same-owner. It contains no measured physical system, real credential lifecycle, deployment or independent reproduction. Working names and learning practices do not establish personhood, continuity or professional authority.')],
 'table':[['Owner work','X1','X2'],['Main contracts','100','100'],['Candidate rejection probes','100','100'],['Source-record refinements','100','100'],['Local skills','10','10'],['Paired runners','5','5'],['Independent invariant tests','18','18']]},
{'title':'Useful results, explicit limits','subtitle':'GMUT Mind with THOS and Freed ID / CBR support',
 'lead':'The exact identities support clearer model definitions. The counterexamples show where a broad interpretation needs an additional assumption. Neither kind of result supplies empirical confirmation of a physical theory.',
 'paragraphs':[
 ('Topology depends on the supplied faces','An unfilled triangular loop and a filled triangle share vertices and edges but have different face sets. Their first rational Betti numbers are one and zero. The phase also checks oriented boundary cancellation and exact rational boundary membership.'),
 ('Energy depends on the model and update','For positive weights, the graph quadratic form agrees with the sum of weighted squared edge differences. Five symbolic derivative checks and twenty library comparisons across ten frozen cases agreed. The interpretation uses energy E = Q/2, where Q is that quadratic form.'),
 ('Three concrete counterexamples','A negative weight gives E = -1/2 outside the admitted positive-weight profile. On the two-node unit-weight model, an explicit step of 3/2 raises E from 1/2 to 2. A disconnected graph can have zero energy while its potential is not globally constant.'),
 ('What remains open','Physical interpretation would need units, observables, measured data, calibration, uncertainty and a specified dynamics. The finite calculations do not prove a new fundamental law, a Theory of Everything or Stage 20 readiness.')],
 'figure':True},
{'title':'Tools, retained evidence and the next edge','subtitle':'Prepared file handoff to Neris Solane v689-v6',
 'lead':f'The {baton["baton_words"]:,}-word handoff has thirteen modules. A 288-card index and a 33-entry local catalogue make the results, skills and implementation modules retrievable without copying the baton into a chat composer.',
 'paragraphs':[
 ('Three additions, exercised on D','SymEngine 0.14.1, opt_einsum 3.4.0 and NumExpr 2.14.2 were installed from exact verified wheels in an isolated D-drive environment. NumPy 2.5.3 is its dependency copy. Three positive and three adverse package smokes passed. NumExpr uses two threads. A point-in-time OSV query found no listed advisories for the four versions.'),
 ('Failures remain visible','The x2 ledger holds 53 methods and 998 witnesses: 237 failed subjects and 761 bounded passes. It distinguishes expected rejections, refuted unrestricted claims and 21 operational failure groups. Corrections preserve failed attempts and do not replay successful source validators or passed calculations.'),
 ('Source canonical and recovery stay separate','Elaren\'s source canonical failed once on an undefined SOURCE constant. Its later component tribunal passed 25 checks and 18 tests. The source retains zero canonical aggregate success credit. Rowan\'s own final canonical result is recorded separately after its exact final push.'),
 ('Current handoff boundary','At repository seal the message is PREPARED_NOT_SENT. Only a valid final gate, current authority, unique exact Neris task and immediate duplicate/control checks permit one compact native message. Vesper v689-v7 is the following projection; Neris refreshes that edge at its own terminal gate.'),
 ('Reading order','Start with final/hand-off-baton.md and its module index, then use deck/deck-index.json and final/meta-tool-catalogue.json for focused retrieval. The external canonical and delivery receipts supply the actual later terminal state. Thirty blocked subjects remain unexecuted.')],
 'table':[['Package','Bounded use'],['SymEngine 0.14.1','Symbolic derivatives'],['opt_einsum 3.4.0','Array contractions'],['NumExpr 2.14.2','Fixed elementwise energy']]}
]
styles={
 'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=24,leading=28,textColor=colors.HexColor(navy),spaceAfter=12),
 'sub':ParagraphStyle('sub',fontName='Helvetica',fontSize=10,leading=14,textColor=colors.HexColor(muted),spaceAfter=16),
 'lead':ParagraphStyle('lead',fontName='Helvetica',fontSize=11,leading=16,textColor=colors.HexColor(navy),spaceAfter=14),
 'h':ParagraphStyle('h',fontName='Helvetica-Bold',fontSize=11,leading=15,textColor=colors.HexColor(teal),spaceBefore=8,spaceAfter=4),
 'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.5,leading=13.5,textColor=colors.HexColor(navy),spaceAfter=7),
}
story=[]
def table(data):
    values=[[Paragraph(html.escape(cell),styles['body']) for cell in row] for row in data]
    widths=[330,65,65] if len(data[0])==3 else [180,280]
    result=Table(values,colWidths=widths,hAlign='LEFT')
    result.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e4efed')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),3),('LINEBELOW',(0,0),(-1,-1),.35,colors.HexColor('#cedbdc'))]))
    return result
for i,page in enumerate(pages):
    if i:story.append(PageBreak())
    story.extend([Paragraph(page['title'],styles['title']),Paragraph(page['subtitle'],styles['sub']),Paragraph(page['lead'],styles['lead'])])
    if page.get('figure'):
        story.append(Image(str(FIG/'finite-geometry.png'),width=490,height=157));story.append(Spacer(1,8))
    if 'table' in page:story.extend([table(page['table']),Spacer(1,10)])
    for heading,text in page['paragraphs']:
        story.extend([Paragraph(heading,styles['h']),Paragraph(html.escape(text),styles['body'])])
    if i==1:story.append(Paragraph('Established calculus context: arxiv.org/html/math/0508341v2. Figure and finite examples generated in this owner phase.',styles['body']))
def footer(canvas,doc):
    canvas.saveState();canvas.setStrokeColor(colors.HexColor('#cedbdc'));canvas.line(48,42,A4[0]-48,42)
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor(muted));canvas.drawString(48,29,'Rowan Ash v689-v5 | finite synthetic evidence | 10 September 2026 NZ')
    canvas.drawRightString(A4[0]-48,29,str(doc.page));canvas.restoreState()
pdf=OUT/'overview.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=43,bottomMargin=55,title='Rowan Ash v689-v5: finite structures and visible assumptions',author='Rowan Ash')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
reader=PdfReader(pdf);assert len(reader.pages)==3,len(reader.pages)
md=['# Rowan Ash v689-v5 overview']
html_sections=[]
for i,page in enumerate(pages,1):
    md.extend([f'## Page {i}: '+page['title'],page['subtitle'],page['lead']])
    content='<h1>'+html.escape(page['title'])+'</h1><p class="sub">'+html.escape(page['subtitle'])+'</p><p class="lead">'+html.escape(page['lead'])+'</p>'
    if 'table' in page:
        md.append('\n'.join(' | '.join(row) for row in page['table']))
        content+='<table><caption>Recorded owner work</caption><thead><tr>'+''.join('<th scope="col">'+html.escape(c)+'</th>' for c in page['table'][0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(c)+'</td>' for c in row)+'</tr>' for row in page['table'][1:])+'</tbody></table>'
    if page.get('figure'):content+='<figure><img src="figures/finite-geometry.png" alt="An unfilled triangular loop has first Betti number one and a filled triangle has zero. A curve of the two-node Euler energy ratio reaches four at step one point five."><figcaption>Finite synthetic model examples; the exact ratio curve is bound in the x2 interpretation receipt.</figcaption></figure>'
    for h,t in page['paragraphs']:
        md.extend(['### '+h,t]);content+='<h2>'+html.escape(h)+'</h2><p>'+html.escape(t)+'</p>'
    html_sections.append('<section class="page" aria-label="Overview page '+str(i)+'">'+content+'</section>')
(OUT/'overview.md').write_bytes(('\n\n'.join(md)+'\n').encode())
(OUT/'overview.html').write_bytes(('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Rowan v689-v5 overview</title><style>body{font:16px/1.55 system-ui;color:'+navy+';background:#eef3f4;margin:0}.page{max-width:940px;margin:28px auto;padding:40px;background:white;box-shadow:0 2px 16px #16344912}h1{font-size:34px;line-height:1.15}h2{font-size:20px;color:'+teal+'}.lead{font-size:19px}.sub,figcaption{color:'+muted+'}table{border-collapse:collapse;width:100%}td,th{padding:9px;border-bottom:1px solid #ccd8de;text-align:left}caption{text-align:left;font-weight:bold}img{width:100%;height:auto}@media print{body{background:white}.page{box-shadow:none;margin:0;page-break-after:always}}</style><main>'+''.join(html_sections)+'</main></html>\n').encode())
qa={'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(reader.pages),'page_text_lengths':[len(p.extract_text() or '') for p in reader.pages],'figure_png_sha256':hashlib.sha256((FIG/'finite-geometry.png').read_bytes()).hexdigest(),'figure_svg_sha256':hashlib.sha256((FIG/'finite-geometry.svg').read_bytes()).hexdigest(),'visual_inspection':'pending','manual_accessibility_evaluation':'reserved','source_data':'docs/rowan-ash/v689-v5/x2/interpretation-receipt.json'}
(BANK/'overview-render-receipt.json').write_bytes((json.dumps(qa,indent=2)+'\n').encode());print(json.dumps(qa),flush=True)
