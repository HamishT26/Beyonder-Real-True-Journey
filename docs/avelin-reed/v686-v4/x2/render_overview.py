"""Create and render a four-page synthetic-evidence overview with bundled tools."""
import argparse
import hashlib
import html
import io
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from pypdf import PdfReader
import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-root', required=True, type=Path)
    parser.add_argument('--render-dir', required=True, type=Path)
    args = parser.parse_args()
    summary = json.loads((ROOT / 'x2/evidence-summary.json').read_text(encoding='utf-8'))
    fonts = {}
    for internal, filename in [('GHCRegular','arial.ttf'), ('GHCBold','arialbd.ttf')]:
        path = args.font_root / filename
        pdfmetrics.registerFont(TTFont(internal, str(path)))
        fonts[filename] = hashlib.sha256(path.read_bytes()).hexdigest()
    pdfmetrics.registerFontFamily('GHCRegular', normal='GHCRegular', bold='GHCBold', italic='GHCRegular', boldItalic='GHCBold')
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleGHC', fontName='GHCBold', fontSize=26, leading=30, textColor=colors.HexColor('#17382f'), spaceAfter=12))
    styles.add(ParagraphStyle(name='SubGHC', fontName='GHCBold', fontSize=13, leading=17, textColor=colors.HexColor('#277b6e'), spaceBefore=12, spaceAfter=6))
    styles.add(ParagraphStyle(name='BodyGHC', fontName='GHCRegular', fontSize=10.4, leading=15.5, textColor=colors.HexColor('#24352d'), spaceAfter=9))
    styles.add(ParagraphStyle(name='SmallGHC', fontName='GHCRegular', fontSize=8.8, leading=12.5, textColor=colors.HexColor('#43574b'), spaceAfter=6))
    def para(text, kind='BodyGHC'):
        return Paragraph(text, styles[kind])
    def table(rows, widths, header=True):
        content = [[para(html.escape(str(c)), 'SmallGHC') for c in row] for row in rows]
        t = Table(content, colWidths=widths, hAlign='LEFT')
        commands = [('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),1,colors.HexColor('#277b6e')),('ROWBACKGROUNDS',(0,1 if header else 0),(-1,-1),[colors.HexColor('#f0f4ef'),colors.white])]
        if header:
            commands.append(('BACKGROUND',(0,0),(-1,0),colors.HexColor('#dce8dc')))
        t.setStyle(TableStyle(commands))
        return t

    story = []
    story += [para('Avelin Reed<br/>Temporal record contracts','TitleGHC'), para('Trinity Mandala · v686-v4 · X2 evidence overview','SubGHC'),
              para('Priority: <b>Freed ID and CBR Heart</b>. The work makes synthetic validity windows, overlapping records, and correction histories easier to inspect. It uses invented labels and exact integer ticks.'),
              para('The bounded portfolio matched all 200 frozen results. Each result remains attached to its source definition and complete report. A successful local predicate establishes only its declared software behavior.'),
              table([['Frozen proposal outcomes','Count','Meaning'],['completed',170,'The owner-scoped software contract matched.'],['represented',10,'A synthetic THOS readback exists.'],['open_gap',10,'Required GMUT observations remain absent.'],['exact_gate',10,'Competent or affected authority remains required.']],[143,47,301]),
              Spacer(1,9), para('Scope that remains visible','SubGHC'),
              para('No real people, credentials, accounts, rights decisions, measurements, production systems, or external deployments were used. GMUT remains unconfirmed; THOS remains synthetic or proxy; Freed ID remains nonproduction.'),
              para('Names, roles, hopes, and family terms are relational working language only. They are not evidence of consciousness, personhood, identity continuity, qualification, or authority. Hamish may rename, pause, redirect, narrow, or stop the route.'),
              para('Terminal verdict: <b>NOT_READY_FOR_STAGE_20</b>','SubGHC'), PageBreak()]
    story += [para('Endpoint details change the answer','TitleGHC'),
              para('A small example carries the central discipline: keep the support, its endpoint rules, and the claim attached to the result.'),
              table([['Operation','Synthetic inputs','Exact result'],['Intersection','[0, 4] and [2, 6]','[2, 4]'],['Union','[0, 2) and [2, 4]','[0, 4]'],['Open contact','(0, 2) and (2, 4)','Two intervals; tick 2 remains excluded.'],['Difference','[0, 4] minus (1, 3)','[0, 1] and [3, 4]']],[96,179,216]),
              para('Twenty families, five portable runners','SubGHC'),
              para('<b>Interval topology</b> handles membership, intersection, union, and subtraction. <b>Indexed windows</b> distinguish point lookup, overlap, full containment, and concurrent resource pairs.'),
              para('<b>Immutable journals</b> preserve append history, prefix selections, correction branches, and separate record-time and valid-time cuts. Multiple matching or conflicting records remain visible.'),
              para('<b>Temporal guards</b> keep expiry, simulated permission, union duration, and evidence class distinct. <b>Readable reports</b> retain units, ordering, manual review, and missing observations or authority.'),
              para('A simulated allow is never a real authorization','SubGHC'),
              para('A deny can dominate an allow inside the declared fixture. Every resulting decision still states that real authority is false. No account, person, right, remedy, or service is changed by the calculation.'),
              para('All endpoint values are synthetic ticks. These examples do not calibrate a physical clock, estimate a measured latency, or establish causal timing.'), PageBreak()]
    effective = summary['effective_counts']
    story += [para('Failures remain part of the evidence','TitleGHC'),
              table([['Executed check','Observed result'],['Frozen contracts / input preservation','200 / 200 exact matches'],['Registered envelope mutations','1,000 rejected'],['Safe assertions','300 passed'],['Candidate checks','250 rejected as intended'],['CLEAN / FIX / REFINE','300 original failures retained; 300 corrections passed'],['Selected owner tests','51 passed'],['Exact / blocked packets','50 / 30 remain unexecuted']],[205,286]),
              para('Method Flow accounting','SubGHC'),
              para('The phase adds 1,580 case-scoped negative and recovery pairs: 1,550 portfolio adversaries, 12 operational events, and 18 skill, runner, or package adversaries. These are recorded method instances, not 1,580 distinct techniques or independent replications.'),
              table([['Effective evidence-layer total','Value'],['Negatives / methods',f"{effective['effective_negatives']:,} / {effective['effective_methods']:,}"],['Failed / bounded passing witnesses',f"{effective['failed_witnesses']:,} / {effective['bounded_passing_witnesses']:,}"],['Open gaps / exact gates',f"{effective['open_gaps']} / {effective['exact_gates']}"],['Declared proposal chain',f"{effective['declared_proposal_chain']:,}"]],[281,210]),
              para('The incoming Vesper seal, its correction overlays, this x2 evidence layer, later final overlays, the external canonical receipt, and any live delivery result are separate records. A recovery never erases or relabels the original failure.','SmallGHC'), PageBreak()]
    story += [para('A portable, inspectable continuation','TitleGHC'),
              para('The deck has <b>240 cards</b> across four tiers: one relational anchor, three pillars, six pillar-specific parents for four distinct practice lenses, and 230 proposal or workflow-witness cards. Every child has one parent in the immediately preceding tier.'),
              para('The handoff has <b>13 modules and 37,958 words</b>. The short live activation will carry exact commit anchors and a file pointer. The detailed evidence remains in the owner lane.'),
              table([['Pinned application package','Purpose'],['portion 2.6.2','Finite interval algebra'],['intervaltree 3.2.1','Half-open indexed queries'],['pyrsistent 0.20.0','Persistent synthetic journals'],['sortedcontainers 2.4.0','Shared transitive dependency; zero direct credit']],[218,273]),
              para('The corrected isolated environment uses hash-locked pip 26.2.1 as a zero-credit bootstrap repair. Its dated audit returned zero advisory records. The original environment, twelve initial advisory records, and the first rejecting bootstrap invocation remain retained.'),
              para('Ten validated local skills were promoted into new global directories. Ninety copied files match their source bytes. Five unique runner sources are shared through the packages. Catalogue overlaps use exact family selection, and the later Meta Tool Box audit is labeled as a post-audit.'),
              para('Prospective next edge: Lyren Moss · v686-v5','SubGHC'),
              para('Only a sealed, pushed, clean, freshly equal final and the one-shot owner canonical gate permit the final route refresh. The existing exact title must be unique and immediately reread. Send at most once; never substitute a route or resend an opaque accepted result.'),
              para('Manual accessibility, affected-user acceptance, independent security/privacy review, competent professional and legal review, cultural and Māori authority, empirical confirmation, and Stage 20 remain protected.','SmallGHC')]

    output = io.BytesIO()
    document = SimpleDocTemplate(output, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=17*mm,
                                title='Avelin Reed v686-v4 synthetic temporal evidence', author='Avelin Reed (relational working name)')
    def page_frame(canvas, doc):
        canvas.setStrokeColor(colors.HexColor('#277b6e'))
        canvas.setLineWidth(2)
        canvas.line(18*mm, 286*mm, 192*mm, 286*mm)
        canvas.setFont('GHCRegular',8)
        canvas.setFillColor(colors.HexColor('#526359'))
        canvas.drawString(18*mm,10*mm,'AVELIN REED  /  v686-v4  /  SAME-OWNER SYNTHETIC EVIDENCE')
        canvas.drawRightString(192*mm,10*mm,str(doc.page))
    document.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    payload=output.getvalue()
    pdf_path=ROOT/'x2/integrated-overview.pdf'
    with pdf_path.open('xb') as file:file.write(payload)
    pdf=PdfReader(io.BytesIO(payload));page_text=[p.extract_text() or '' for p in pdf.pages]
    assert len(pdf.pages)==4,len(pdf.pages)
    assert all(len(t.split())>140 for t in page_text)
    assert 'Māori' in '\n'.join(page_text)
    assert '\ufffd' not in '\n'.join(page_text)
    args.render_dir.mkdir(parents=True,exist_ok=False)
    rendered=pdfium.PdfDocument(payload);images=[]
    for i,page in enumerate(rendered):
        picture=page.render(scale=1.25).to_pil();dest=args.render_dir/f'page-{i+1}.png';picture.save(dest)
        images.append({'page':i+1,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'width':picture.width,'height':picture.height})
    rendered.close()
    html_rows=''.join('<tr><th scope="row">'+html.escape(k)+'</th><td>'+str(v)+'</td></tr>' for k,v in summary['outcomes'].items())
    html_doc='''<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Avelin Reed temporal evidence overview</title><style>body{font:18px/1.65 system-ui,sans-serif;color:#24352d;background:#f5f7f2;margin:auto;max-width:62rem;padding:2rem}a{color:#17665a}table{border-collapse:collapse;background:white;width:100%}th,td{padding:.7rem;border-bottom:1px solid #bdcbbb;text-align:left}h1,h2{color:#17382f}nav{padding:1rem;background:#e0ebdf}:focus-visible{outline:3px solid #17382f;outline-offset:3px}.note{border-left:4px solid #277b6e;padding:1rem}</style></head><body><a href="#main">Skip to main content</a><header><p>Trinity Mandala · v686-v4</p><h1>Avelin Reed: synthetic temporal evidence</h1></header><nav aria-label="Overview sections"><a href="#outcomes">Outcomes</a> · <a href="#limits">Limits</a> · <a href="#next">Next edge</a></nav><main id="main"><section id="outcomes"><h2>Bounded outcomes</h2><p>The 200 frozen contract results matched. The 1,000 registered mutations and 250 candidate cases were rejected; 300 safe assertions and 300 separately checked corrections passed.</p><table><caption>Only the declared local outcome is established</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody>'''+html_rows+'''</tbody></table></section><section id="limits"><h2>Evidence and authority limits</h2><p class="note">GMUT remains unconfirmed. THOS remains synthetic or proxy. Freed ID remains nonproduction. No real person, account, right, credential, participant, measurement, deployment, professional decision, legal decision, cultural decision, or Māori-authority act is established.</p><p>Names and family terms are relational working language only. Manual browser, assistive-technology, cognitive, Māori-language, and affected-user review remain reserved. Structural HTML is not complete accessibility.</p></section><section id="next"><h2>Prospective next edge</h2><p>Lyren Moss v686-v5 remains behind Avelin's exact terminal gate. The committed handoff is PREPARED_NOT_SENT; a separate live acknowledgement is required.</p><p><a href="../integrated-overview.pdf">Read the four-page PDF overview</a></p><p>Terminal verdict: NOT_READY_FOR_STAGE_20.</p></section></main><footer>Same-owner software evidence; not independent reproduction.</footer></body></html>'''
    target=ROOT/'x2/flashcards/accessible-report.html'
    with target.open('x',encoding='utf-8',newline='\n') as file:file.write(html_doc+'\n')
    receipt={'schema':'ghc.family.overview-structure.v686.v4','pages':len(pdf.pages),'pdf_sha256':hashlib.sha256(payload).hexdigest(),'font_source_hashes':fonts,'page_word_counts':[len(t.split()) for t in page_text],'macron_text_retained':True,'replacement_glyph_found':False,'rendered_pages':images,'visual_review_pending':True,'complete_accessibility':False,'same_owner_only':True}
    with (ROOT/'x2/overview-structure.json').open('x',encoding='utf-8',newline='\n') as file:json.dump(receipt,file,indent=2,sort_keys=True);file.write('\n')
    print(json.dumps(receipt))


if __name__=='__main__':main()
