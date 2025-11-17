"""
캡스톤디자인 전시 판넬 생성
Neural Pathways 디자인 철학 기반
"""

from reportlab.lib.pagesizes import A1
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math

# A1 사이즈 (594mm x 841mm)
WIDTH, HEIGHT = A1

# 색상 정의 (Neural Pathways 철학)
DEEP_BLUE = colors.HexColor('#0A1929')
TECH_TEAL = colors.HexColor('#00D9FF')
NEURAL_BLUE = colors.HexColor('#1E88E5')
WARM_ACCENT = colors.HexColor('#FF6B35')
LIGHT_GRAY = colors.HexColor('#E8EAF6')
WHITE = colors.white

def draw_network_node(c, x, y, radius, fill_color, stroke_color=None):
    """네트워크 노드 그리기"""
    c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(2)
    else:
        c.setStrokeColor(fill_color)
    c.circle(x, y, radius, fill=1, stroke=1)

def draw_connection_line(c, x1, y1, x2, y2, color, width=1):
    """연결선 그리기"""
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

def draw_gradient_rect(c, x, y, w, h, color1, color2):
    """그라디언트 사각형 (간단 버전)"""
    steps = 50
    for i in range(steps):
        ratio = i / steps
        r = color1.red * (1 - ratio) + color2.red * ratio
        g = color1.green * (1 - ratio) + color2.green * ratio
        b = color1.blue * (1 - ratio) + color2.blue * ratio
        c.setFillColor(colors.Color(r, g, b))
        c.rect(x, y + (h * i / steps), w, h / steps, fill=1, stroke=0)

def create_capstone_poster():
    """캡스톤 포스터 생성"""

    # PDF 생성
    pdf_path = "/home/jjyeom/ollama-company-chatbot/docs/capstone_poster_draft.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A1)

    # 배경
    c.setFillColor(DEEP_BLUE)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)

    # 상단 헤더 영역
    header_height = 120*mm
    c.setFillColor(colors.HexColor('#0D2137'))
    c.rect(0, HEIGHT - header_height, WIDTH, header_height, fill=1, stroke=0)

    # 메인 타이틀
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 56)
    title = "Ollama 기반 회사 소개 ChatBot"
    c.drawCentredString(WIDTH/2, HEIGHT - 60*mm, title)

    c.setFont("Helvetica", 32)
    c.drawCentredString(WIDTH/2, HEIGHT - 85*mm, "RAG 기반 지능형 정보 응답 시스템")

    # 소속 정보
    c.setFont("Helvetica", 18)
    c.setFillColor(TECH_TEAL)
    c.drawCentredString(WIDTH/2, HEIGHT - 105*mm, "동서울대학교 AI융합소프트웨어학과 | ㈜퓨쳐시스템")

    # 좌측 패널 - 프로젝트 정보
    left_x = 50*mm
    info_y = HEIGHT - 160*mm

    c.setFillColor(TECH_TEAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(left_x, info_y, "프로젝트 개요")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 16)
    info_y -= 15*mm

    info_text = [
        "기간: 2025.08.30 ~ 2025.11.28",
        "팀원: 염재준",
        "지도교수: 조민양 교수",
        "현장교사: 김인태 선임"
    ]

    for text in info_text:
        c.drawString(left_x, info_y, text)
        info_y -= 10*mm

    # 기술 스택
    tech_y = info_y - 15*mm
    c.setFillColor(TECH_TEAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(left_x, tech_y, "기술 스택")

    tech_y -= 15*mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 16)

    techs = [
        "Streamlit - 웹 UI",
        "Ollama - LLM 엔진",
        "LangChain - RAG 프레임워크",
        "FAISS - 벡터 스토어",
        "Sentence Transformers - 임베딩"
    ]

    for tech in techs:
        c.drawString(left_x, tech_y, tech)
        tech_y -= 10*mm

    # 중앙 - 시스템 아키텍처 (네트워크 다이어그램)
    center_x = WIDTH / 2
    arch_y = HEIGHT - 200*mm

    c.setFillColor(WARM_ACCENT)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(center_x, arch_y + 120*mm, "시스템 아키텍처")

    # 네트워크 노드들
    nodes = [
        # (x, y, radius, color, label)
        (center_x - 150*mm, arch_y + 80*mm, 15*mm, TECH_TEAL, "사용자"),
        (center_x, arch_y + 80*mm, 20*mm, NEURAL_BLUE, "Streamlit UI"),
        (center_x + 150*mm, arch_y + 80*mm, 15*mm, TECH_TEAL, "응답"),

        (center_x - 80*mm, arch_y + 20*mm, 18*mm, WARM_ACCENT, "RAG Pipeline"),
        (center_x + 80*mm, arch_y + 20*mm, 18*mm, WARM_ACCENT, "LLM (Ollama)"),

        (center_x - 80*mm, arch_y - 40*mm, 15*mm, NEURAL_BLUE, "Vector Store"),
        (center_x + 80*mm, arch_y - 40*mm, 15*mm, NEURAL_BLUE, "임베딩"),

        (center_x, arch_y - 100*mm, 20*mm, TECH_TEAL, "데이터 소스"),
    ]

    # 연결선 그리기
    connections = [
        (0, 1), (1, 2),  # 사용자 -> UI -> 응답
        (1, 3), (1, 4),  # UI -> RAG, LLM
        (3, 4),          # RAG <-> LLM
        (3, 5), (4, 6),  # RAG -> Vector, LLM -> 임베딩
        (5, 7), (6, 7),  # Vector -> 데이터, 임베딩 -> 데이터
    ]

    for i, j in connections:
        x1, y1 = nodes[i][0], nodes[i][1]
        x2, y2 = nodes[j][0], nodes[j][1]
        draw_connection_line(c, x1, y1, x2, y2, LIGHT_GRAY, 2)

    # 노드 그리기
    for x, y, r, color, label in nodes:
        draw_network_node(c, x, y, r, color, WHITE)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x, y - 3*mm, label)

    # 우측 패널 - 주요 기능
    right_x = WIDTH - 220*mm
    feature_y = HEIGHT - 160*mm

    c.setFillColor(WARM_ACCENT)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(right_x, feature_y, "주요 기능")

    feature_y -= 15*mm
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 16)

    features = [
        "회사 정보 기반 질의응답",
        "RAG 기반 정확한 답변",
        "실시간 대화 인터페이스",
        "벡터 검색 기술",
        "대화 이력 관리",
        "다중 모델 지원"
    ]

    for i, feature in enumerate(features):
        # 작은 노드 아이콘
        node_x = right_x - 8*mm
        node_y = feature_y + 3*mm
        draw_network_node(c, node_x, node_y, 3*mm, TECH_TEAL)

        c.drawString(right_x, feature_y, feature)
        feature_y -= 12*mm

    # 하단 - 기대효과
    bottom_y = 100*mm

    c.setFillColor(TECH_TEAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(WIDTH/2, bottom_y + 40*mm, "기대 효과")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 16)

    effects = [
        "24/7 자동 응답으로 고객 만족도 향상",
        "정확한 정보 제공으로 업무 효율성 증대",
        "오픈소스 기반으로 비용 절감"
    ]

    effect_y = bottom_y + 20*mm
    for effect in effects:
        c.drawCentredString(WIDTH/2, effect_y, effect)
        effect_y -= 12*mm

    # 푸터
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 14)
    c.drawCentredString(WIDTH/2, 30*mm, "2025 Capstone Design Project")

    # 저장
    c.save()
    print(f"✓ 포스터 초안 생성 완료: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_capstone_poster()
