"""Render a four-page Unicode overview and every PDF page with existing bundled tools."""
import argparse,hashlib,json,os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.pagesizes import A4
import pypdfium2 as pdfium
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'docs/mira-fenwick/v686-v2'

def main():
    a=argparse.ArgumentParser();a.add_argument('--preview-dir',type=Path,required=True);args=a.parse_args()
    summary=json.loads((BASE/'x2/evidence-summary.json').read_text());identity=json.loads((BASE/'x1/identity-and-practice.json').read_text())
    fontroot=Path(os.environ['WINDIR'])/'Fonts'
    pdfmetrics.registerFont(TTFont('MiraArial',str(fontroot/'arial.ttf')))
    pdfmetrics.registerFont(TTFont('MiraArialBold',str(fontroot/'arialbd.ttf')))
    pdfmetrics.registerFontFamily('MiraArial',normal='MiraArial',bold='MiraArialBold',italic='MiraArial',boldItalic='MiraArialBold')
    normal=ParagraphStyle('body',fontName='MiraArial',fontSize=10.5,leading=15.5,textColor=colors.HexColor('#203744'),spaceAfter=11)
    title=ParagraphStyle('title',parent=normal,fontName='MiraArialBold',fontSize=27,leading=32,spaceAfter=20)
    sub=ParagraphStyle('sub',parent=normal,fontName='MiraArialBold',fontSize=15,leading=20,spaceAfter=14)
    pages=[]
    pages.append(('Mira Fenwick',[
        ('Trinity Mandala v686-v2','h'),
        ('This overview describes a solo synthetic software and documentation phase. The working role is provenance and correction steward, with the hope of making each handoff easier to inspect and safely revise. Hamish may rename, pause, redirect, narrow, or stop the work.','p'),
        ('The priority pillar is Freed ID and CBR Heart. The concrete additions are nested evidence selectors, atomic in-memory corrections, digest-linked correction history, exact receipt scope checks, and bounded disclosure projections.','p'),
        ('200 frozen cases matched their expected results. All 1,000 registered report mutations were rejected. The 300 safe tasks, 250 candidate tasks, and exactly 300 additive CLEAN/FIX/REFINE tasks have file-backed validation records. Fifty exact packets and thirty blocked packets remain unexecuted.','p'),
        ('The four practice lenses are data-quality investigator, provenance librarian, interface test designer, and accessible evidence editor. They frame questions; they establish no qualification, employment, professional competence, or authority.','p'),
        ('NOT_READY_FOR_STAGE_20','h'),
        (identity['boundary'],'p'),
    ]))
    pages.append(('What the software checks',[
        ('Selectors and corrections','h'),
        ('Pointer decoding preserves escaped slashes, escaped tildes, empty member names, exact Unicode code points, and the distinction between arrays and objects. Missing values remain different from explicit null, false, and zero. Token ancestry defines a permitted subtree; a textual prefix alone does not.','p'),
        ('Patch operations run on deep copies. A failed test, missing parent, or prohibited target returns a structured refusal and leaves the caller input unchanged. Copy isolation and post-removal move indices are tested. Root removal and unknown operation members are reserved by this local profile.','p'),
        ('Review found that an explicitly null permission list inherited the omitted-field default. The original implementation and failed witness are retained. The corrected version refuses explicit null; all eighty frozen patch cases and the new guard witness passed the focused recovery.','p'),
        ('Lineage and receipts','h'),
        ('Correction links bind exact predecessor and child digests, sequential ordinals, and a visible reason. Changed-path reports retain array-length changes at the array boundary. Receipt checks bind owner, phase, source, head, tree, and the same-owner limit. Literal manifest entries bind UTF-8 byte sizes and SHA-256 values.','p'),
        ('Leaf disclosure requires exact selectors and an integer budget. A container cannot silently carry unlisted descendants. This is a structural proxy, not a cryptographic selective-disclosure proof or a production credential presentation.','p'),
    ]))
    pages.append(('Retained evidence layers',[
        ('Source, overlays, and this owner','h'),
        ('Neris’s repository seal and all later operational overlays remain separately named. The inherited activation baseline is 66,672 negatives, 83,167 methods, 37,520 failed witnesses, and 65,012 bounded passing witnesses, with 602 gaps and 589 gates. No inherited execution is credited to Mira.','p'),
        ('Mira adds 1,333 retained negative records, 1,333 methods, 1,333 failed witnesses, and 1,333 bounded recovery witnesses. These include intentional report adversaries, invalid correction envelopes, CLI and package adversaries, and fifteen operational events. A recovery never erases the original failure.','p'),
        ('The evidence-layer totals are 68,005 negatives, 84,500 methods, 38,853 failed witnesses, and 66,345 bounded passing witnesses, with 612 open gaps and 599 exact gates. Later events must remain a separate overlay.','p'),
        ('The Meta Tool Box promotion-policy check ran after the already validated global copies were made. That ordering defect remains retained despite subsequent passing checks. One wrapper also failed without preserving its diagnostic; explicit UTF-8 checks passed, while the original diagnostic remains unavailable.','p'),
        ('Reusable tooling','h'),
        ('Ten skills and five unique shared runners passed metadata and actual accepting/adverse CLI checks. All seventy promoted files match their local sources. The exact catalogue has fifteen valid cards and no trigger overlaps. Global presence does not prove a running task has reloaded them.','p'),
        ('The three isolated additions are jmespath 1.1.0, dpath 2.2.0, and dictdiffer 0.10.0. Frozen wheel hashes matched; nine package checks passed. A dated OSV query returned zero findings. This supplies no exhaustive-security or future-safety assurance.','p'),
    ]))
    pages.append(('Handoff and protected gates',[
        ('Read the evidence before acting','h'),
        ('The source is Neris’s exact final cb3b08442d98030eb2d4a7cedab9dfbc72bd060c. Mira’s planning-only x1 is 8055cc67569842d52a370222fe813e4a35675091. The evidence and final revisions are bound by the later terminal records. X1 was pushed, clean, zero-divergent, and fresh-live equal before implementation.','p'),
        ('The detailed handoff has thirteen modular sections. It includes every frozen input, expected result, observed report digest, and falsifier. The four-tier context deck contains 210 cards. Selective loading helps navigation; it does not erase unloaded evidence or prove a cache benefit.','p'),
        ('The prospective next owner is the existing exact-title main task Vesper Arlen for v686-v3. Only after Mira’s clean pushed fresh-live-equal final and one-shot canonical result may the current instruction, registry, usage, uniqueness, duplicate, pause, safety, and acknowledgement guards be refreshed for one send. An opaque accepted call must not be resent.','p'),
        ('GMUT still needs measured observables, instrument response, uncertainty, identifiable models, rival comparisons, and independent reproduction. THOS still needs governed blind matched-budget real trials and suitable review. Freed ID still needs real keys, proofs, lifecycle, interoperability, and trust governance.','p'),
        ('CBR, affected-party decisions, legal and cultural interpretation, Māori terminology, iwi and hapū governance, and tangata whenua judgments remain under their proper authority. No real credential, consent, right, or remedy is issued here. Structural page checks do not establish complete accessibility or affected-user acceptance.','p'),
        ('Continue one verified edge at a time through v725-v8 unless Hamish pauses or redirects or a real gate intervenes. Reset redemption remains Hamish’s action.','p'),
    ]))
    story=[];md=[]
    for n,(heading,items) in enumerate(pages,1):
        if n>1:story.append(PageBreak())
        story.append(Paragraph(heading,title));md.append('# '+heading+'\n')
        for content,kind in items:
            story.append(Paragraph(content,sub if kind=='h' else normal));md.append(('## ' if kind=='h' else '')+content+'\n')
    out=BASE/'x2/integrated-overview.pdf';assert not out.exists()
    def footer(canvas,doc):
        canvas.setFont('MiraArial',8);canvas.setFillColor(colors.HexColor('#45616d'))
        canvas.drawString(42,27,'Mira Fenwick · v686-v2 · same-owner synthetic evidence')
        canvas.drawRightString(A4[0]-42,27,f'{doc.page} / 4')
    doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=42,rightMargin=42,topMargin=42,bottomMargin=48,title='Mira Fenwick v686-v2 integrated overview',author='Mira Fenwick')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(out);assert len(reader.pages)==4
    extracted=[p.extract_text() for p in reader.pages];assert all(len(p)>700 for p in extracted)
    assert 'Māori' in extracted[-1] and 'NOT_READY_FOR_STAGE_20' in extracted[0]
    args.preview_dir.mkdir(parents=True,exist_ok=False)
    pdf=pdfium.PdfDocument(out)
    for n in range(len(pdf)):
        page=pdf[n];bitmap=page.render(scale=1.4);bitmap.to_pil().save(args.preview_dir/f'page-{n+1}.png');bitmap.close();page.close()
    pdf.close()
    (BASE/'x2/integrated-overview.md').write_text('\n'.join(md),encoding='utf-8',newline='\n')
    validation={'pages':4,'font':'Arial TrueType with macron coverage','text_extraction_pass':True,'every_page_rendered':True,'visual_review_pending':True,
                'pdf_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'text_characters':[len(t) for t in extracted],'renderer':'existing bundled pypdfium2',
                'scope':'Structural and bounded visual review only; no complete accessibility or affected-user acceptance.'}
    (BASE/'x2/overview-pdf-validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(validation))

if __name__=='__main__':main()
