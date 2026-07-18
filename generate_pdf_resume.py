import os
import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon, String
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --- REGISTER HANDWRITTEN FONT FAMILY ---
# Maps ArchitectsDaughter to all styles to prevent ReportLab from crashing when encountering bold/italic tags
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
    
    # Draw two slightly offset overlapping lines with wobbly midpoints
    for offset in [(-0.6, 0.4), (0.6, -0.4)]:
        dx = x2 - x1
        dy = y2 - y1
        
        # Calculate intermediate points with random offset
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

def draw_sketchy_circle(canvas_obj, x, y, r, fillColor, strokeColor, width=1.2):
    canvas_obj.saveState()
    canvas_obj.setFillColor(fillColor)
    canvas_obj.setStrokeColor(strokeColor)
    canvas_obj.setLineWidth(width)
    
    # Fill solid inner node slightly smaller
    canvas_obj.circle(x, y, r - 0.5, fill=True, stroke=False)
    
    # Draw wobbly double stroke ellipses
    for offset in [0.4, -0.4]:
        rx = r + random.uniform(-0.5, 0.5)
        ry = r + random.uniform(-0.5, 0.5)
        canvas_obj.ellipse(x - rx + offset, y - ry + offset, x + rx + offset, y + ry + offset, fill=False, stroke=True)
        
    canvas_obj.restoreState()

# --- CUSTOM DYNAMIC TIMELINE FLOWABLE ---
class TimelineLine(Flowable):
    def __init__(self, width=20, is_start=False, is_end=False):
        super(TimelineLine, self).__init__()
        self.width = width
        self.is_start = is_start
        self.is_end = is_end

    def wrap(self, availWidth, availHeight):
        # Return height of 0 so ReportLab's table engine sizes the row height based on text contents
        return self.width, 0

    def draw(self):
        # Center coordinates
        x_center = self.width / 2.0
        
        y_start = 0 if not self.is_end else self.height - 10
        y_end = self.height if not self.is_start else self.height - 10
        
        # 1. Draw sketchy vertical line
        draw_sketchy_line(self.canv, x_center, y_start, x_center, y_end, HexColor('#6366f1'), width=1.2)
        
        # 2. Draw sketchy circle node
        draw_sketchy_circle(self.canv, x_center, self.height - 10, 4.5, HexColor('#14b8a6'), HexColor('#05050b'), width=1.2)

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

def create_location_icon():
    d = Drawing(12, 12)
    d.add(Circle(6, 7.5, 3.2, fillColor=None, strokeColor=HexColor('#14b8a6'), strokeWidth=0.8))
    d.add(Circle(6, 7.5, 1, fillColor=HexColor('#14b8a6'), strokeColor=None))
    d.add(Polygon([3, 5.5, 6, 0.5, 9, 5.5], fillColor=HexColor('#14b8a6'), strokeColor=None))
    return d

def create_website_icon():
    d = Drawing(12, 12)
    d.add(Circle(6, 6, 5.5, fillColor=None, strokeColor=HexColor('#14b8a6'), strokeWidth=0.8))
    d.add(Line(0.5, 6, 11.5, 6, strokeColor=HexColor('#14b8a6'), strokeWidth=0.6))
    d.add(Circle(6, 6, 2.2, fillColor=None, strokeColor=HexColor('#14b8a6'), strokeWidth=0.6))
    return d

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
        
        # 3. Draw footer branding text
        self.drawString(40, 25, "Kyawt May Hlaing — Portfolio Resume (kyawtmayhlaing173.github.io)")
        
        self.restoreState()

# --- PDF BUILD ENGINE ---
def build_pdf(filename):
    # Setup document: margins of 40pt for a clean, professional tech resume layout
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
    
    # Custom Paragraph Styles (Using ArchitectsDaughter)
    title_style = ParagraphStyle(
        'NameHeader',
        parent=styles['Heading1'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=28,
        leading=32,
        textColor=teal,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'RoleHeader',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=13,
        leading=15,
        textColor=indigo,
        spaceAfter=8
    )
    
    contact_style = ParagraphStyle(
        'ContactText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9,
        leading=12,
        textColor=slate_grey
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=13,
        leading=15,
        textColor=teal,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    date_style = ParagraphStyle(
        'DateColText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=9,
        leading=13,
        textColor=slate_grey,
        alignment=TA_RIGHT
    )
    
    exp_detail_style = ParagraphStyle(
        'ExpDetailText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9.2,
        leading=14.5,
        textColor=slate_grey,
        spaceAfter=12
    )
    
    norm_text_style = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter',
        fontSize=9.5,
        leading=15,
        textColor=slate_grey,
        spaceAfter=4
    )
    
    skills_label_style = ParagraphStyle(
        'SkillsLabel',
        parent=styles['Normal'],
        fontName='ArchitectsDaughter-Bold',
        fontSize=9.5,
        leading=15,
        textColor=off_white
    )
    
    story = []
    
    # ------------------ HEADER SECTION ------------------
    story.append(Paragraph("KYAWT MAY HLAING", title_style))
    story.append(Paragraph("SENIOR MOBILE ENGINEER", subtitle_style))
    
    # Contact Information Grid (featuring Clickable Links styled in Teal)
    email_html = '<a href="mailto:pinky.hlaing173@gmail.com"><font color="#14b8a6"><u>pinky.hlaing173@gmail.com</u></font></a>'
    linkedin_html = '<a href="https://linkedin.com/in/kyawt-may-hlaing-4623aaab"><font color="#14b8a6"><u>linkedin.com/in/kyawt-may-hlaing-4623aaab</u></font></a>'
    github_html = '<a href="https://github.com/kyawtmayhlaing173"><font color="#14b8a6"><u>github.com/kyawtmayhlaing173</u></font></a>'
    portfolio_html = '<a href="https://kyawtmayhlaing173.github.io"><font color="#14b8a6"><u>kyawtmayhlaing173.github.io</u></font></a>'
    
    contacts_table_data = [
        [
            make_contact_item(create_email_icon, email_html, contact_style),
            make_contact_item(create_linkedin_icon, linkedin_html, contact_style),
            make_contact_item(create_github_icon, github_html, contact_style)
        ],
        [
            make_contact_item(create_location_icon, "Tokyo, Japan", contact_style),
            make_contact_item(create_website_icon, portfolio_html, contact_style),
            Paragraph("", contact_style)
        ]
    ]
    contacts_table = Table(contacts_table_data, colWidths=[180, 220, 132])
    contacts_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(contacts_table)
    story.append(Spacer(1, 4))
    
    # ------------------ PROFILE SUMMARY ------------------
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_title_style))
    summary_text = (
        "Result-driven, details-oriented Senior Mobile Engineer with over <b>7 years</b> of experience in designing, "
        "developing, and optimizing high-performance iOS and Android applications. Expert in <b>SwiftUI, Flutter, and Swift</b>, "
        "with a proven track record of orchestrating payment system migrations, building CI/CD deployment automation pipelines, "
        "and managing real-time chat infrastructures. Certified <b>AWS Solutions Architect</b> with deep full-stack proficiency "
        "in NodeJS, TypeScript, Firebase, and scalable cloud systems."
    )
    story.append(Paragraph(summary_text, norm_text_style))
    story.append(Spacer(1, 4))
    
    # ------------------ WORK EXPERIENCE (TIMELINE TABLES) ------------------
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_title_style))
    
    # 1. AMPTALK (is_start=True to begin the vertical line connector)
    exp1_data = [[
        Paragraph("<b>Aug 2025 -<br/>Present</b><br/><font color='#64748b'>Tokyo, Japan</font>", date_style),
        TimelineLine(width=20, is_start=True),
        Paragraph(
            "<b><font size='11.5' color='#f8fafc'>Amptalk</font></b> &nbsp;|&nbsp; <font color='#14b8a6'><b>Senior Mobile Engineer</b></font><br/>"
            "• Spearheaded the development of VoIP communication software integration in iOS using Swift and Flutter.<br/>"
            "• Scaled client-side audio streaming pipelines, integrating audio session guidelines for smooth call handoffs.<br/>"
            "• Deployed cloud backend integration modules utilizing Node.js, Typescript, and AWS.<br/>"
            "<b>Technologies:</b> Flutter, Dart, Swift, Firebase, AWS, Node.js, TypeScript",
            exp_detail_style
        )
    ]]
    exp1_table = Table(exp1_data, colWidths=[90, 20, 422])
    exp1_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    exp1_table.spaceBefore = 0
    exp1_table.spaceAfter = 0
    story.append(exp1_table)
    
    # 2. OPN THAILAND (SR)
    exp2_data = [[
        Paragraph("<b>Jul 2024 -<br/>Jul 2025</b><br/><font color='#64748b'>Bangkok, Thailand</font>", date_style),
        TimelineLine(width=20),
        Paragraph(
            "<b><font size='11.5' color='#f8fafc'>Opn Thailand</font></b> &nbsp;<font color='#94a3b8' size='9'>(formerly Omise)</font> &nbsp;|&nbsp; <font color='#14b8a6'><b>Senior Mobile Engineer</b></font><br/>"
            "• Architected payment SDK systems handling multi-million dollar transactions for enterprise clients in Southeast Asia.<br/>"
            "• Led migrations of legacy UI platforms to SwiftUI, resolving core layout threads and reducing render times by 20%.<br/>"
            "• Configured DevOps pipelines via Fastlane and GitHub Actions, cutting delivery cycles to TestFlight and Play Store by 40%.<br/>"
            "• Supervised mobile engineering standards, conducting reviews, writing modular frameworks, and onboarding new staff.",
            exp_detail_style
        )
    ]]
    exp2_table = Table(exp2_data, colWidths=[90, 20, 422])
    exp2_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    exp2_table.spaceBefore = 0
    exp2_table.spaceAfter = 0
    story.append(exp2_table)

    # 3. OPN THAILAND (SE)
    exp3_data = [[
        Paragraph("<b>Jul 2022 -<br/>Jun 2024</b><br/><font color='#64748b'>Bangkok, Thailand</font>", date_style),
        TimelineLine(width=20),
        Paragraph(
            "<b><font size='11.5' color='#f8fafc'>Opn Thailand</font></b> &nbsp;|&nbsp; <font color='#14b8a6'><b>Software Engineer</b></font><br/>"
            "• Integrated secure card tokenization modules matching PCI-DSS compliance specifications across regional APIs.<br/>"
            "• Programmed core components for native iOS payment SDKs, maintaining robust offline safety nets.<br/>"
            "• Deployed and maintained Firebase push notification suites and Firestore real-time client databases.<br/>"
            "<b>Technologies:</b> SwiftUI, Swift, Firebase, Firestore, REST APIs, Fastlane, CI/CD, Git",
            exp_detail_style
        )
    ]]
    exp3_table = Table(exp3_data, colWidths=[90, 20, 422])
    exp3_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    exp3_table.spaceBefore = 0
    exp3_table.spaceAfter = 0
    story.append(exp3_table)

    # 4. ONE ATKHYAR
    exp4_data = [[
        Paragraph("<b>Mar 2019 -<br/>Jun 2022</b><br/><font color='#64748b'>Yangon, Myanmar</font>", date_style),
        TimelineLine(width=20),
        Paragraph(
            "<b><font size='11.5' color='#f8fafc'>One Atkhyar</font></b> &nbsp;|&nbsp; <font color='#14b8a6'><b>Mobile Engineer</b></font><br/>"
            "• Built the flagship lifestyle/e-commerce app 'Shi Del' from scratch, scaling client adoption to over 100k active users.<br/>"
            "• Designed highly responsive UI flows using Flutter and Dart, incorporating state management (Bloc) and clean architecture.<br/>"
            "• Configured Algolia search nodes and real-time Firestore database triggers to manage heavy product catalog indices.<br/>"
            "• Programmed backend microservice layers using Node.js, TypeScript, and Firebase Cloud Functions.<br/>"
            "<b>Technologies:</b> Flutter, Dart, Firebase, Firestore, Algolia, TypeScript, NodeJS, Clean Architecture, Confluence",
            exp_detail_style
        )
    ]]
    exp4_table = Table(exp4_data, colWidths=[90, 20, 422])
    exp4_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    exp4_table.spaceBefore = 0
    exp4_table.spaceAfter = 0
    story.append(exp4_table)

    # 5. CLOUDSOURCE MYANMAR
    exp5_data = [[
        Paragraph("<b>Jul 2018 -<br/>Sep 2019</b><br/><font color='#64748b'>Yangon, Myanmar</font>", date_style),
        TimelineLine(width=20),
        Paragraph(
            "<b><font size='11.5' color='#f8fafc'>Cloudsource Myanmar</font></b> &nbsp;|&nbsp; <font color='#14b8a6'><b>Full Stack Developer</b></font><br/>"
            "• Programmed responsive client web portals and administrative dashboards using Laravel and Ruby on Rails.<br/>"
            "• Configured complex SQL schemas, transactional index optimizations, and API integrations in PostgreSQL databases.<br/>"
            "• Maintained server hosting deployments, integrating secure SSL handshakes and cron monitoring automation.<br/>"
            "<b>Technologies:</b> Ruby on Rails, Laravel, PostgreSQL, PHP, Ruby, SQL, Apache",
            exp_detail_style
        )
    ]]
    exp5_table = Table(exp5_data, colWidths=[90, 20, 422])
    exp5_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    exp5_table.spaceBefore = 0
    exp5_table.spaceAfter = 0
    story.append(exp5_table)

    # 6. ACROQUEST MYANMAR (is_end=True to terminate the vertical line connector)
    exp6_data = [[
        Paragraph("<b>May 2017 -<br/>Aug 2017</b><br/><font color='#64748b'>Yangon, Myanmar</font>", date_style),
        TimelineLine(width=20, is_end=True),
        Paragraph(
            "<b><font size='11.5' color='#f8fafc'>Acroquest Myanmar Technology</font></b> &nbsp;|&nbsp; <font color='#14b8a6'><b>Software Engineer Intern</b></font><br/>"
            "• Implemented proof-of-concept decentralized utility billing applications detailing smart contract automations.<br/>"
            "• Programmed Solidity smart contract validation scripts on private Ethereum testnet networks.<br/>"
            "<b>Technologies:</b> Solidity, Smart Contracts, Ethereum, JavaScript, HTML/CSS",
            exp_detail_style
        )
    ]]
    exp6_table = Table(exp6_data, colWidths=[90, 20, 422])
    exp6_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    exp6_table.spaceBefore = 0
    exp6_table.spaceAfter = 0
    story.append(exp6_table)
    story.append(Spacer(1, 4))
    
    # ------------------ TECHNICAL SKILLS ------------------
    story.append(Paragraph("TECHNICAL SKILLS", section_title_style))
    
    skills_data = [
        [Paragraph("<b>Mobile & Core:</b>", skills_label_style), 
         Paragraph("SwiftUI, Flutter, Swift, Dart, Ionic, Android SDK", norm_text_style)],
        [Paragraph("<b>Backend & Web:</b>", skills_label_style), 
         Paragraph("Node.js, TypeScript, Ruby on Rails, Laravel, PHP, REST APIs, PostgreSQL, SQL", norm_text_style)],
        [Paragraph("<b>Cloud & Infra:</b>", skills_label_style), 
         Paragraph("AWS (S3, EC2, Lambda), Firebase, Cloud Firestore, Firebase Cloud Functions", norm_text_style)],
        [Paragraph("<b>DevOps & Tools:</b>", skills_label_style), 
         Paragraph("Fastlane, CI/CD pipelines, Docker, Git, GitHub Actions, Linear, Notion, Confluence", norm_text_style)]
    ]
    
    skills_table = Table(skills_data, colWidths=[120, 412])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 4))
    
    # ------------------ CERTIFICATIONS ------------------
    story.append(Paragraph("CREDENTIALS & CERTIFICATIONS", section_title_style))
    
    credly_html = '<a href="https://www.credly.com/badges/314a6a4e-8b66-437a-9f7d-d75a9f38d05f"><font color="#14b8a6"><u>314a6a4e-8b66-437a-9f7d-d75a9f38d05f</u></font></a>'
    
    certs_data = [
        [Paragraph("<b>2026:</b>", skills_label_style), Paragraph(f"AWS Certified Solutions Architect – Associate (Credly ID: {credly_html})", norm_text_style)],
        [Paragraph("<b>2025:</b>", skills_label_style), Paragraph("AWS Certified Cloud Practitioner", norm_text_style)]
    ]
    certs_table = Table(certs_data, colWidths=[60, 472])
    certs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(certs_table)
    story.append(Spacer(1, 4))
    
    # ------------------ PUBLICATIONS ------------------
    story.append(Paragraph("PUBLICATIONS & RESEARCH", section_title_style))
    
    ieee_html = '<a href="https://ieeexplore.ieee.org/document/8920931"><font color="#14b8a6"><u>https://ieeexplore.ieee.org/document/8920931</u></font></a>'
    
    pub_text = (
        "<b>IEEE Xplore Publication: Blockchain Utility Billing (2019)</b><br/>"
        "Co-authored decentralized utilities systems research detailing automated consumer settlement triggers "
        f"via Ethereum smart contracts and cloud integrations. Indexed in IEEE Xplore: {ieee_html}"
    )
    story.append(Paragraph(pub_text, norm_text_style))
    story.append(Spacer(1, 4))
    
    # ------------------ EDUCATION ------------------
    story.append(Paragraph("EDUCATION", section_title_style))
    edu_text = (
        "<b>Bachelor of Computer Science (B.C.Sc.)</b> &nbsp;|&nbsp; "
        "University of Computer Studies, Yangon, Myanmar (2013 - 2018)"
    )
    story.append(Paragraph(edu_text, norm_text_style))
    story.append(Spacer(1, 4))
    
    # ------------------ LANGUAGES ------------------
    story.append(Paragraph("LANGUAGE PROFICIENCIES", section_title_style))
    langs = [
        "<b>Myanmar:</b> Native Proficiency",
        "<b>English:</b> Intermediate",
        "<b>Chinese:</b> HSK Level 5",
        "<b>Japanese:</b> N4 Level"
    ]
    story.append(Paragraph(" &nbsp;•&nbsp; ".join(langs), norm_text_style))
    
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
