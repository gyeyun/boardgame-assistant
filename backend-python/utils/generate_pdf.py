from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os

# 출력 폴더 설정
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../generated_pdfs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 한글 폰트 등록
FONT_PATH = os.path.join(os.path.dirname(__file__), "../assets/fonts/NotoSansKR-Regular.ttf")
pdfmetrics.registerFont(TTFont('NotoSansKR', FONT_PATH))

# 스타일 정의
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Korean', fontName='NotoSansKR', fontSize=11, leading=14))

# ✅ [기존 함수] 룰북 PDF 생성
def render_rulebook_to_pdf(context: dict, filename: str):
    filepath = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []

    for key, value in context.items():
        story.append(Paragraph(f"<b>{key}</b>", styles["Korean"]))
        story.append(Spacer(1, 6))
        for line in value.strip().split("\n"):
            story.append(Paragraph(line.strip(), styles["Korean"]))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 12))

    doc.build(story)
    return filepath

# ✅ [추가할 함수] 설명 스크립트 PDF 생성
def render_description_to_pdf(script: str, filename: str):
    filepath = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []

    story.append(Paragraph("<b>보드게임 설명 스크립트</b>", styles["Korean"]))
    story.append(Spacer(1, 12))

    for line in script.strip().split("\n"):
        story.append(Paragraph(line.strip(), styles["Korean"]))
        story.append(Spacer(1, 6))

    doc.build(story)
    return filepath
