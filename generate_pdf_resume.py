import os
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon, String
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon, String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- REGISTER HANDWRITTEN FONT FAMILY ---
font_path = os.path.join(os.path.dirname(__file__), "ArchitectsDaughter-Regular.ttf")
pdfmetrics.registerFont(TTFont('ArchitectsDaughter', font_path))
pdfmetrics.registerFont(TTFont('ArchitectsDaughter-Bold', font_path))
pdfmetrics.registerFont(TTFont('ArchitectsDaughter-Oblique', font_path))
pdfmetrics.registerFont(TTFont('ArchitectsDaughter-BoldOblique', font_path))

pdfmetrics.registerFontFamily(
    'ArchitectsDaughter',
    normal='ArchitectsDaughter',
    bold='ArchitectsDaughter-Bold',
    italic='ArchitectsDaughter-Oblique',
    boldItalic='ArchitectsDaughter-BoldOblique'
)

# --- EXCALIDRAW SKETCHY DRAWING HELPERS ---
def draw_sketchy_line(canvas_obj, x1, y1, x2, y2, color, width=1.2):
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(color)
    canvas_obj.setLineWidth(width)
    
    for offset in [(-0.6, 0.4), (0.6, -0.4)]:
        dx = x2 - x1
        dy = y2 - y1
        x_mid1 = x1 + dx * 0.35 + random.uniform(-0.8, 0.8)
        y_mid1 = y1 + dy * 0.35 + random.uniform(-0.8, 0.8)
        x_mid2 = x1 + dx * 0.70 + random.uniform(-0.8, 0.8)
        y_mid2 = y1 + dy * 0.70 + random.uniform(-0.8, 0.8)
        
        p = canvas_obj.beginPath()
        p.moveTo(x1 + offset[0], y1 + offset[1])
        p.lineTo(x_mid1, y_mid1)
        p.lineTo(x_mid2, y_mid2)
        p.lineTo(x2 + offset[1], y2 + offset[0])
        canvas_obj.drawPath(p)
        
    canvas_obj.restoreState()

# --- CUSTOM SHARP VECTOR ICONS ---
def create_email_icon():
    d = Drawing(12, 12)
    d.add(Rect(1, 2, 10, 8, fillColor=None, strokeColor=HexColor('#14b8a6'), strokeWidth=0.8, rx=0.8, ry=0.8))
    d.add(Line(1, 2, 6, 6, strokeColor=HexColor('#14b8a6'), strokeWidth=0.8))
    d.add(Line(11, 2, 6, 6, strokeColor=HexColor('#14b8a6'), strokeWidth=0.8))
    return d

def create_linkedin_icon():
    d = Drawing(12, 12)
    d.add(Rect(0, 1, 11, 11, fillColor=HexColor('#6366f1'), strokeColor=None, rx=1.5, ry=1.5))
    d.add(String(2, 4.2, "in", fontName="ArchitectsDaughter-Bold", fontSize=8, fillColor=HexColor('#05050b')))
    return d

def create_github_icon():
    d = Drawing(12, 12)
    d.add(Circle(6, 6, 5.5, fillColor=HexColor('#14b8a6'), strokeColor=None))
    d.add(String(3.2, 4, "git", fontName="ArchitectsDaughter-Bold", fontSize=5.5, fillColor=HexColor('#05050b')))
    return d

def create_website_icon():
    d = Drawing(12, 12)
    d.add(Circle(6, 6, 5.5, fillColor=None, strokeColor=HexColor('#14b8a6'), strokeWidth=0.8))
    d.add(Line(0.5, 6, 11.5, 6, strokeColor=HexColor('#14b8a6'), strokeWidth=0.6))
    d.add(Circle(6, 6, 2.2, fillColor=None, strokeColor=HexColor('#14b8a6'), strokeWidth=0.6))
    return d

def create_medium_icon():
    d = Drawing(12, 12)
    d.add(Circle(2.5, 6, 2.5, fillColor=HexColor('#14b8a6'), strokeColor=None))
    d.add(Circle(7, 6, 2, fillColor=HexColor('#14b8a6'), strokeColor=None))
    d.add(Circle(10.5, 6, 1.5, fillColor=HexColor('#14b8a6'), strokeColor=None))
    return d

# --- VECTOR FLAG ICONS ---
def create_myanmar_flag():
    d = Drawing(16, 11)
    d.add(Rect(0, 7.3, 16, 3.7, fillColor=HexColor('#fecb00'), strokeColor=None))
    d.add(Rect(0, 3.7, 16, 3.7, fillColor=HexColor('#109856'), strokeColor=None))
    d.add(Rect(0, 0, 16, 3.7, fillColor=HexColor('#ea2839'), strokeColor=None))
    d.add(Rect(0, 0, 16, 11, fillColor=None, strokeColor=HexColor('#64748b'), strokeWidth=0.4))
    # white star
    d.add(Polygon([6,6.5, 7.5,6.5, 8,8.5, 8.5,6.5, 10,6.5, 8.8,5.5, 9.3,3.5, 8,4.5, 6.7,3.5, 7.2,5.5], fillColor=HexColor('#ffffff'), strokeColor=None))
    return d

def create_china_flag():
    d = Drawing(16, 11)
    d.add(Rect(0, 0, 16, 11, fillColor=HexColor('#de2910'), strokeColor=HexColor('#64748b'), strokeWidth=0.4))
    d.add(Polygon([3,8, 4,8, 4.5,9.5, 5,8, 6,8, 5.1,7, 5.5,5.5, 4.5,6.5, 3.5,5.5, 3.9,7], fillColor=HexColor('#ffde00'), strokeColor=None))
    return d

def create_uk_flag():
    d = Drawing(16, 11)
    d.add(Rect(0, 0, 16, 11, fillColor=HexColor('#00247d'), strokeColor=HexColor('#64748b'), strokeWidth=0.4))
    d.add(Line(0, 0, 16, 11, strokeColor=HexColor('#ffffff'), strokeWidth=2))
    d.add(Line(0, 11, 16, 0, strokeColor=HexColor('#ffffff'), strokeWidth=2))
    d.add(Line(0, 0, 16, 11, strokeColor=HexColor('#cf142b'), strokeWidth=0.9))
    d.add(Line(0, 11, 16, 0, strokeColor=HexColor('#cf142b'), strokeWidth=0.9))
    d.add(Rect(6.5, 0, 3, 11, fillColor=HexColor('#ffffff'), strokeColor=None))
    d.add(Rect(0, 4, 16, 3, fillColor=HexColor('#ffffff'), strokeColor=None))
    d.add(Rect(7.2, 0, 1.6, 11, fillColor=HexColor('#cf142b'), strokeColor=None))
    d.add(Rect(0, 4.7, 16, 1.6, fillColor=HexColor('#cf142b'), strokeColor=None))
    return d

def create_japan_flag():
    d = Drawing(16, 11)
    d.add(Rect(0, 0, 16, 11, fillColor=HexColor('#ffffff'), strokeColor=HexColor('#64748b'), strokeWidth=0.4))
    d.add(Circle(8, 5.5, 2.8, fillColor=HexColor('#bc002d'), strokeColor=None))
    return d

def make_lang_item(flag_func, text_val, style_obj):
    t = Table([[flag_func(), Paragraph(text_val, style_obj)]], colWidths=[22, None])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

# --- SKETCHY TIMELINE BULLET ICONS (EXCALIDRAW STYLE) ---
def create_sketchy_list_bullet():
    d = Drawing(14, 14)
    d.add(Circle(7, 7, 3, fillColor=HexColor('#14b8a6'), strokeColor=None))
    return d

def create_sketchy_sub_bullet():
    d = Drawing(14, 14)
    d.add(Circle(7, 7, 2, fillColor=HexColor('#6366f1'), strokeColor=None))
    return d

# Helper to build contact text cells
def make_contact_item(icon_func, text, style):
    t = Table([[icon_func(), Paragraph(text, style)]], colWidths=[15, None])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    return t

# --- NUMBERED CANVAS (PAGINATION LAYER) ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # 1. Draw sketchy border highlight glow (Excalidraw style)
        draw_sketchy_line(self, 15, 15, 15, self._pagesize[1] - 15, HexColor('#14b8a6'), width=1)
        draw_sketchy_line(self, 15, self._pagesize[1] - 15, self._pagesize[0] - 15, self._pagesize[1] - 15, HexColor('#6366f1'), width=1)
        
        # 2. Draw page numbers at the bottom right
        self.setFont("ArchitectsDaughter", 8)
        self.setFillColor(HexColor('#64748b'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(self._pagesize[0] - 40, 25, page_text)
        
        self.restoreState()

# --- PDF BUILD ENGINE ---
def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    # Custom colors
    teal = HexColor('#14b8a6')
    indigo = HexColor('#6366f1')
    off_white = HexColor('#f8fafc')
    slate_grey = HexColor('#94a3b8')
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'NameHeader',
        parent=styles['Heading1'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=24,
        leading=28,
        textColor=teal,
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    contact_style = ParagraphStyle(
        'ContactText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9.5,
        leading=12,
        textColor=slate_grey
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=14,
        leading=17,
        textColor=teal,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    comp_title_style = ParagraphStyle(
        'CompanyTitle',
        parent=styles['Heading3'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=11,
        leading=14,
        textColor=off_white,
        spaceBefore=0,
        spaceAfter=0,
        keepWithNext=True
    )
    
    edu_title_style = ParagraphStyle(
        'EduTitleText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=10.5,
        leading=14,
        textColor=off_white,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    
    # Right-aligned for job headers
    date_style = ParagraphStyle(
        'JobDateText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=9.5,
        leading=14,
        textColor=slate_grey,
        alignment=TA_RIGHT,
        spaceBefore=0,
        spaceAfter=0,
        keepWithNext=True
    )
    
    # Left-aligned for certificates/projects columns
    date_left_style = ParagraphStyle(
        'DateLeftText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=9.5,
        leading=14,
        textColor=slate_grey,
        spaceBefore=0,
        spaceAfter=0,
        keepWithNext=True
    )
    
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9.2,
        leading=14.5,
        textColor=slate_grey,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )
    
    sub_bullet_style = ParagraphStyle(
        'SubBulletPoint',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9.2,
        leading=14.5,
        textColor=slate_grey,
        leftIndent=24,
        firstLineIndent=-8,
        spaceAfter=2
    )
    
    tag_style = ParagraphStyle(
        'TechTag',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=8.5,
        leading=11,
        textColor=teal,
        spaceBefore=4,
        spaceAfter=8
    )
    
    norm_text_style = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9.5,
        leading=15,
        textColor=slate_grey,
        spaceAfter=6
    )
    
    skills_label_style = ParagraphStyle(
        'SkillsLabel',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=9.5,
        leading=15,
        textColor=off_white
    )

    # Job Header Table builders
    def make_job_header(title_text, dates_text):
        bullet = create_sketchy_list_bullet()
        title_p = Paragraph(title_text, comp_title_style)
        date_p = Paragraph(dates_text, date_style)
        t = Table([[bullet, title_p, date_p]], colWidths=[18, 390, 124])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
        ]))
        return t

    def make_sub_job_header(title_text, dates_text):
        bullet = create_sketchy_sub_bullet()
        title_p = Paragraph(title_text, comp_title_style)
        date_p = Paragraph(dates_text, date_style)
        t = Table([[bullet, title_p, date_p]], colWidths=[18, 390, 124])
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
        ]))
        return t
    
    story = []
    
    # ------------------ HEADER SECTION ------------------
    story.append(Spacer(1, 10))
    story.append(Paragraph("K Y A W T &nbsp; M A Y &nbsp; H L A I N G &nbsp; ( P I N K Y )", title_style))
    
    email_html = '<a href="mailto:pinky.hlaing173@gmail.com"><font color="#14b8a6"><u>pinky.hlaing173@gmail.com</u></font></a>'
    portfolio_html = '<a href="https://kyawtmayhlaing173.github.io/cv_resume/"><font color="#14b8a6"><u>kyawtmayhlaing173.github.io/cv_resume/</u></font></a>'
    linkedin_html = '<a href="https://www.linkedin.com/in/kyawt-may-hlaing-4623aaab/"><font color="#14b8a6"><u>linkedin.com/in/kyawt-may-hlaing-4623aaab</u></font></a>'
    medium_html = '<a href="https://medium.com/@pinky.hlaing173"><font color="#14b8a6"><u>medium.com/@pinky.hlaing173</u></font></a>'
    
    contacts_table_data = [
        [
            make_contact_item(create_email_icon, email_html, contact_style),
            make_contact_item(create_website_icon, portfolio_html, contact_style)
        ],
        [
            make_contact_item(create_linkedin_icon, linkedin_html, contact_style),
            make_contact_item(create_medium_icon, medium_html, contact_style)
        ]
    ]
    contacts_table = Table(contacts_table_data, colWidths=[260, 272])
    contacts_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(contacts_table)
    story.append(Spacer(1, 4))
    
    # ------------------ ABOUT ------------------
    story.append(Paragraph("ABOUT", section_title_style))
    about_text = (
        "With a proven track record in developing innovative mobile applications, I excel in leveraging "
        "skills in Flutter and Agile methodologies. My expertise spans cross-platform development, "
        "complemented by strong problem-solving and collaboration abilities. Achievements include "
        "leading seamless integrations, optimizing app performance, and driving project success, "
        "showcasing a blend of technical proficiency and teamwork."
    )
    story.append(Paragraph(about_text, norm_text_style))
    
    # ------------------ EDUCATION ------------------
    story.append(Paragraph("EDUCATION", section_title_style))
    
    ieee_html = '<a href="https://ieeexplore.ieee.org/document/8920931"><font color="#14b8a6"><u>https://ieeexplore.ieee.org/document/8920931</u></font></a>'
    
    story.append(Paragraph("Master of Computer Science In High-Performance Computing ( M.C.Sc )", edu_title_style))
    story.append(Paragraph("2017 - 2019 • <i>University of Information Technology, Yangon, Myanmar</i>", date_left_style))
    story.append(Paragraph(f"Thesis Paper: \"Electricity Billing System using Ethereum and Firebase\" ({ieee_html})", norm_text_style))
    story.append(Spacer(1, 4))
    
    story.append(Paragraph("Bachelor of Computer Science In High-Performance Computing ( B.C.Sc )", edu_title_style))
    story.append(Paragraph("2012 - 2017 • <i>University of Information Technology, Yangon, Myanmar</i>", date_left_style))
    story.append(Spacer(1, 4))
    
    # ------------------ EXPERIENCE ------------------
    story.append(Paragraph("EXPERIENCE", section_title_style))
    
    # 1. AMPTALK
    amptalk_company = "<b>Senior Mobile Engineer</b> • <a href='https://www.linkedin.com/company/amptalk/'><font color='#14b8a6'><u>Amptalk Co., Ltd</u></font></a>"
    story.append(make_job_header(amptalk_company, "August 2025 - Present"))
    story.append(Paragraph("Architecting scalable audio capture and analytics applications for enterprise sales summary integrations on the Analysis Mobile team.", norm_text_style))
    story.append(Paragraph("• <b>Core Mobile Recorder:</b> Architected a robust, production-grade meeting voice recorder application in Flutter, using the record package for high-fidelity audio capture.", bullet_style))
    story.append(Paragraph("• <b>OS Audio Management:</b> Implemented platform-level audio session logic to handle background recording modes and graceful recovery during phone call interruptions.", bullet_style))
    story.append(Paragraph("• <b>Background Transfer:</b> Designed resilient upload queues that transfer chunked audio files to transcription servers in the background.", bullet_style))
    story.append(Paragraph("• <b>Flutter Codebase Standards:</b> Leading code reviews and standardizing clean architectures for the Analysis Mobile division to ensure code modularity.", bullet_style))
    story.append(Paragraph("<b>Project Link:</b> [ <a href='https://apps.apple.com/jp/app/amptalk-analysis/id6738689188'><font color='#14b8a6'><u>App Store</u></font></a> ]", bullet_style))
    story.append(Paragraph("<b>Skills:</b> Flutter, Dart, Swift, Firebase, AWS, Node.js, TypeScript, Notion, Linear", tag_style))
    story.append(Spacer(1, 4))

    # 2. OPN THAILAND
    opn_block = []
    opn_company = "<b>Senior Software Engineer</b> • <a href='https://www.linkedin.com/company/opn-co/'><font color='#14b8a6'><u>Opn Thailand Co., Ltd</u></font></a>"
    opn_block.append(make_job_header(opn_company, "April 2024 - July 2025"))
    opn_block.append(make_sub_job_header("<font color='#14b8a6'><b>Software Engineer</b></font>", "July 2022 - April 2024"))
    
    opn_block.append(Paragraph("<b>Key Projects</b>", comp_title_style))
    opn_block.append(Paragraph("• <b>TICKETIER</b>, a mobile app for ticketing system", bullet_style))
    opn_block.append(Paragraph("• Developed a comprehensive ticketing platform, focusing on the mobile application to enhance user accessibility and engagement.", sub_bullet_style))
    opn_block.append(Paragraph("• <b>Responsibilities:</b>", sub_bullet_style))
    opn_block.append(Paragraph("- Designed and implemented mobile app features that streamline the ticket purchasing process, enabling users to easily browse events, and make secure payments.", sub_bullet_style))
    opn_block.append(Paragraph("- Managed the integration of payment gateways to ensure secure and efficient transactions.", sub_bullet_style))
    opn_block.append(Paragraph("- Managed App Store submissions, addressing feedback, ensuring compliance with guidelines, and delivering timely updates.", sub_bullet_style))
    opn_block.append(Paragraph("• <b>Outcome:</b> Successfully delivered a user-friendly mobile application that increased ticket sales and improved customer satisfaction by providing a seamless booking experience.", sub_bullet_style))
    opn_block.append(Paragraph("<b>Project Link:</b> [ <a href='https://apps.apple.com/us/app/ticketier-show-event-tickets/id6476260768'><font color='#14b8a6'><u>App Store</u></font></a> ]", sub_bullet_style))
    
    opn_block.append(Paragraph("• <b>Wallet as a Service</b>", bullet_style))
    opn_block.append(Paragraph("• Responsible for developing iOS applications on the Wallet as a Service (WaaS) team, focusing on e-wallet solutions for clients.", sub_bullet_style))
    opn_block.append(Paragraph("• Collaborated with backend teams to integrate secure payment processing via Omise, ensuring a smooth transaction experience for users.", sub_bullet_style))
    opn_block.append(Paragraph("<b>Skills:</b> Flutter, SwiftUI, Swift, Firebase Authentication, Firebase Remote Config, Firebase Analytics, Jira, Confluence, Figma, Postman, Github, Git Action, Fastlane", tag_style))
    story.append(KeepTogether(opn_block))
    story.append(Spacer(1, 4))
    
    # 3. ONE ATKHYAR
    atkhyar_block = []
    atkhyar_company = "<b>Full-Stack Developer</b> • <a href='https://atkhayar.com/'><font color='#14b8a6'><u>One Atkhyar Co., Ltd</u></font></a>"
    atkhyar_block.append(make_job_header(atkhyar_company, "August 2019 - June 2022"))
    
    atkhyar_block.append(Paragraph("<b>Key Projects</b>", comp_title_style))
    atkhyar_block.append(Paragraph("• <font color='#14b8a6'><b>Shi Del</b></font>, a lifestyle app", bullet_style))
    atkhyar_block.append(Paragraph("• Developed Shi Del from the ground up, creating both backend and frontend architecture and managing deployment across platforms.", sub_bullet_style))
    atkhyar_block.append(Paragraph("• <b>Contributions:</b> Built backend services, crafted a user-friendly frontend, and handled deployments on both the App Store and Play Store.", sub_bullet_style))
    atkhyar_block.append(Paragraph("• <b>Outcome:</b> Successfully launched and scaled the app, providing users with reliable, personalized experience.", sub_bullet_style))
    atkhyar_block.append(Paragraph("<b>Project Link:</b> [ <a href='https://apps.apple.com/jp/app/shi-del/id1612929510'><font color='#14b8a6'><u>App Store</u></font></a> ]", sub_bullet_style))
    
    atkhyar_block.append(Paragraph("• <font color='#14b8a6'><b>Chat Chin</b></font>, Myanmar's no. 1 car servicing app plus emergency assistance", bullet_style))
    atkhyar_block.append(Paragraph("• Developed Chat Chin app from the ground up, creating both backend and frontend architecture and managing deployment across platform.", sub_bullet_style))
    atkhyar_block.append(Paragraph("• <b>Contributions:</b>", sub_bullet_style))
    atkhyar_block.append(Paragraph("- Implemented a search feature that allows users to find businesses by location, enhancing discoverability.", sub_bullet_style))
    atkhyar_block.append(Paragraph("- Developed a data listing feature, integrating crawled data to provide up-to-date information on car services.", sub_bullet_style))
    atkhyar_block.append(Paragraph("- Included functionality for users to add reviews, promoting community engagement and feedback.", sub_bullet_style))
    atkhyar_block.append(Paragraph("• <b>Outcome:</b> Successfully launched and scaled the app, offering users reliable car servicing and emergency assistance with a personalized experience.", sub_bullet_style))
    atkhyar_block.append(Paragraph("<b>Project Link:</b> [ <a href='https://atkhayar.com/'><font color='#14b8a6'><u>Website</u></font></a> ]", sub_bullet_style))
    atkhyar_block.append(Paragraph("<b>Skills:</b> Flutter, Ionic, Firebase Authentication, Firestore, Firebase Functions, Firebase Storage, Firebase Analytics, Jira, Confluence, Figma, Gitlab, GCP, Algolia, Typescript, Angular", tag_style))
    story.append(KeepTogether(atkhyar_block))
    story.append(Spacer(1, 4))
    
    # 4. CLOUD SOURCE MYANMAR
    cloud_company = "<b>Software Developer (Part Time)</b> • <a href='https://www.linkedin.com/company/cloudsource-myanmar/'><font color='#14b8a6'><u>Cloud Source Myanmar Co., Ltd</u></font></a>"
    story.append(make_job_header(cloud_company, "July 2018 - Sep 2019"))
    story.append(Paragraph("• Developed a web application with CRUD functionality in Ruby on Rails.", bullet_style))
    story.append(Paragraph("• Designed, developed, and debugged cross-platform mobile applications in Ionic Framework.", bullet_style))
    story.append(Paragraph("• Created prototype system design using Sketch design toolkit.", bullet_style))
    story.append(Paragraph("<b>Skills:</b> Ruby on Rails, Ionic, PHP Laravel, Javascript, Angular, Typescript", tag_style))
    story.append(Spacer(1, 4))
    
    # 5. ACROQUEST MYANMAR
    acro_company = "<b>Web Developer (Intern)</b> • <a href='https://www.linkedin.com/company/acroquest-technology/'><font color='#14b8a6'><u>Acroquest Myanmar Technology Co., Ltd</u></font></a>"
    story.append(make_job_header(acro_company, "May 2017 - Aug 2017"))
    story.append(Paragraph("• Designed, developed, and tested website using HTML5, CSS, jQuery, Spring MVC, MyBatis, and MySQL.", bullet_style))
    story.append(Paragraph("• Researched on network vendor product.", bullet_style))
    story.append(Paragraph("<b>Skills:</b> HTML, CSS, jQuery, Java Spring MVC, MyBatis, MySQL", tag_style))
    
    story.append(Spacer(1, 4))
    
    # ------------------ PERSONAL PROJECTS ------------------
    story.append(Paragraph("PERSONAL PROJECTS", section_title_style))
    
    testflight_html = '<a href="https://testflight.apple.com/join/8D2XfJEE"><font color="#14b8a6"><u>https://testflight.apple.com/join/8D2XfJEE</u></font></a>'
    playstore_html = '<a href="https://play.google.com/store/apps/details?id=com.htamanel.thePegu"><font color="#14b8a6"><u>https://play.google.com/store/apps/details?id=com.htamanel.thePegu</u></font></a>'
    notetaking_html = '<a href="https://github.com/kyawtmayhlaing173/Ionic-NoteTakingApp"><font color="#14b8a6"><u>https://github.com/kyawtmayhlaing173/Ionic-NoteTakingApp</u></font></a>'
    
    projects_data = [
        [
            Paragraph("<b>2023</b>", date_left_style),
            Paragraph(
                "<b>Daily Motivation App (SwiftUI + Firebase + Appstore)</b><br/>"
                f"Link: {testflight_html}<br/>"
                "Log your mood daily to track your progress over time, receive motivational quotes to start your day "
                "on a positive note, and view your mood history with easy-to-read charts.",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>2021</b>", date_left_style),
            Paragraph(
                "<b>News App (Flutter + Google Ads + API)</b><br/>"
                f"Link: {playstore_html}<br/>"
                "This app is developed with Flutter. I teamed up with my friend to develop this. This app is to show "
                "users the latest news.",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>2021</b>", date_left_style),
            Paragraph(
                "<b>Chrome Dino App (Flutter + Google Ads)</b><br/>"
                "This is the replicate version of the chrome dino app. I teamed up with my friend to develop this. "
                "We cloned the dino game repository online and modify to our own needs.",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>2021</b>", date_left_style),
            Paragraph(
                "<b>Note Taking App (Ionic Cordova + Firebase)</b><br/>"
                f"Link: {notetaking_html}<br/>"
                "This app is to help user takes daily notes with easy using UI.",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>2016</b>", date_left_style),
            Paragraph(
                "<b>Island Cruise Booking Website (PHP + MYSQL)</b><br/>"
                "This website provides an island cruise booking system to users. I teamed up with my friend to develop "
                "this website. Users can book tickets, edit tickets, and delete tickets using this website.",
                norm_text_style
            )
        ]
    ]
    
    projects_table = Table(projects_data, colWidths=[60, 472])
    projects_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(projects_table)
    story.append(Spacer(1, 4))
    
    # ------------------ CERTIFICATE ------------------
    story.append(Paragraph("CERTIFICATE", section_title_style))
    
    credly_html = '<a href="https://www.credly.com/badges/314a6a4e-8b66-437a-9f7d-d75a9f38d05f"><font color="#14b8a6"><u>314a6a4e-8b66-437a-9f7d-d75a9f38d05f</u></font></a>'
    
    certs_data = [
        [Paragraph("<b>2026</b>", date_left_style), Paragraph(f"AWS Certified Solutions Architect – Associate (Credly ID: {credly_html})", norm_text_style)],
        [Paragraph("<b>2020</b>", date_left_style), Paragraph("AWS Cloud Practitioner (CLF-C01)<br/><font color='#64748b'>LinuxAcademy</font>", norm_text_style)],
        [Paragraph("<b>2019</b>", date_left_style), Paragraph("Chinese Proficiency Test (HSK) Level 5", norm_text_style)],
        [Paragraph("<b>2017</b>", date_left_style), Paragraph("Fundamental Information Technology Engineer Examination<br/><font color='#64748b'>Information Technology Professional Examination Council</font>", norm_text_style)],
        [Paragraph("<b>2016</b>", date_left_style), Paragraph("Information Technology Passport Examination<br/><font color='#64748b'>Information Technology Professional Examination Council</font>", norm_text_style)]
    ]
    certs_table = Table(certs_data, colWidths=[60, 472])
    certs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(certs_table)
    story.append(Spacer(1, 4))
    
    # ------------------ TRAINING ------------------
    story.append(Paragraph("TRAINING", section_title_style))
    
    trainings_data = [
        [
            Paragraph("<b>Sep 2014 -<br/>Oct 2014</b>", date_left_style),
            Paragraph(
                "<b>Android Mobile Application</b><br/>"
                "Training Institute: KOREA INTERNATIONAL COOPERATION AGENCY (KOICA)<br/>"
                "Location: University of Information Technology, Yangon, Myanmar",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>Oct 13 2016 -<br/>Oct 21 2016</b>", date_left_style),
            Paragraph(
                "<b>Android Game with Arduino Microcontroller Basic Course</b><br/>"
                "Training Institute: KOREA INTERNATIONAL COOPERATION AGENCY (KOICA)<br/>"
                "Location: University of Information Technology, Yangon, Myanmar",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>May 30 2016 -<br/>July 15 2016</b>", date_left_style),
            Paragraph(
                "<b>IT Service Management</b><br/>"
                "Training Institute: HITACHI, Ltd.,<br/>"
                "Location: University of Information Technology, Yangon, Myanmar",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>Jan 23 2017 -<br/>Mar 03 2017</b>", date_left_style),
            Paragraph(
                "<b>Bigdata IoT/Pentaho training</b><br/>"
                "Training Institute: HITACHI, Ltd.,<br/>"
                "Location: University of Information Technology, Yangon, Myanmar",
                norm_text_style
            )
        ],
        [
            Paragraph("<b>Jan 21 2017 -<br/>Aug 12 2017</b>", date_left_style),
            Paragraph(
                "<b>Enterprise Foundation Network Associate</b><br/>"
                "Training Institute: Vision To Motion Myanmar CO., LTD<br/>"
                "Location: University of Information Technology, Yangon, Myanmar",
                norm_text_style
            )
        ]
    ]
    
    trainings_table = Table(trainings_data, colWidths=[90, 442])
    trainings_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(trainings_table)
    story.append(Spacer(1, 4))
    
    # ------------------ LANGUAGE SKILLS ------------------
    story.append(Paragraph("LANGUAGE SKILLS", section_title_style))
    
    langs_data = [
        [make_lang_item(create_myanmar_flag, "<b>Myanmar</b> (Native)", norm_text_style), make_lang_item(create_china_flag, "<b>Chinese</b> (Intermediate)", norm_text_style)],
        [make_lang_item(create_uk_flag, "<b>English</b> (Intermediate)", norm_text_style), make_lang_item(create_japan_flag, "<b>Japanese</b> (N4 Level)", norm_text_style)]
    ]
    langs_table = Table(langs_data, colWidths=[260, 272])
    langs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(langs_table)
    
    # Build the background rendering callback
    def draw_background(canvas_obj, doc_obj):
        canvas_obj.saveState()
        canvas_obj.setFillColor(HexColor('#05050b'))
        canvas_obj.rect(0, 0, doc_obj.pagesize[0], doc_obj.pagesize[1], fill=True, stroke=False)
        canvas_obj.restoreState()

    # Build the document
    doc.build(story, onFirstPage=draw_background, onLaterPages=draw_background, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    output_path = "/Users/kyawtmayhlaing/Desktop/development/ai/interactive-portfolio/Kyawt_May_Hlaing_Resume.pdf"
    print(f"Building PDF resume to {output_path}...")
    build_pdf(output_path)
    print("PDF build complete successfully!")
