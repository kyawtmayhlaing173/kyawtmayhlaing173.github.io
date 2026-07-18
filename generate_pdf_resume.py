import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

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
        
        # 1. Fill background with HexColor('#05050b')
        self.setFillColor(HexColor('#05050b'))
        self.rect(0, 0, self._pagesize[0], self._pagesize[1], fill=True, stroke=False)
        
        # 2. Draw subtle border highlight glow
        self.setStrokeColor(HexColor('#14b8a6'))
        self.setLineWidth(1)
        # Left accent border glow
        self.line(15, 15, 15, self._pagesize[1] - 15)
        self.setStrokeColor(HexColor('#6366f1'))
        # Top accent border glow
        self.line(15, self._pagesize[1] - 15, self._pagesize[0] - 15, self._pagesize[1] - 15)
        
        # 3. Draw page numbers at the bottom right
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor('#64748b'))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(self._pagesize[0] - 40, 30, page_text)
        
        # 4. Draw footer branding text
        self.drawString(40, 30, "Kyawt May Hlaing — Portfolio Resume (kyawtmayhlaing173.github.io)")
        
        self.restoreState()

def build_pdf(filename):
    # Setup document: margins of 0.5 in (36pt) for a dense, professional tech resume layout
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
    dark_grey = HexColor('#475569')
    
    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        'NameHeader',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=30,
        textColor=teal,
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'RoleHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=indigo,
        spaceAfter=8
    )
    
    contact_style = ParagraphStyle(
        'ContactText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=slate_grey,
        spaceAfter=15
    )
    
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=14,
        textColor=teal,
        spaceBefore=12,
        spaceAfter=4,
        keepWithNext=True
    )
    
    comp_title_style = ParagraphStyle(
        'CompanyTitle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=off_white,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    
    role_title_style = ParagraphStyle(
        'RoleTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=11,
        textColor=indigo,
        spaceAfter=4,
        keepWithNext=True
    )
    
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=slate_grey,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=2
    )
    
    tag_style = ParagraphStyle(
        'TechTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=teal
    )
    
    norm_text_style = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=slate_grey,
        spaceAfter=4
    )
    
    story = []
    
    # ------------------ HEADER SECTION ------------------
    story.append(Paragraph("KYAWT MAY HLAING", title_style))
    story.append(Paragraph("SENIOR MOBILE ENGINEER", subtitle_style))
    
    contacts = [
        "<b>Email:</b> pinky.hlaing173@gmail.com",
        "<b>LinkedIn:</b> linkedin.com/in/kyawt-may-hlaing-4623aaab",
        "<b>GitHub:</b> github.com/kyawtmayhlaing173",
        "<b>Location:</b> Tokyo, Japan",
        "<b>Portfolio:</b> kyawtmayhlaing173.github.io"
    ]
    contact_p = Paragraph(" | ".join(contacts), contact_style)
    story.append(contact_p)
    
    # ------------------ PROFILE SUMMARY ------------------
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_title_style))
    summary_text = (
        "Result-driven, details-oriented Senior Mobile Engineer with over <b>7 years</b> of experience in designing, "
        "developing, and optimizing high-performance iOS and Android applications. Expert in <b>SwiftUI, Flutter, and Swift</b>, "
        "with a proven track record of orchestrating payment system migrations, building CI/CD deployment automation Pipelines, "
        "and managing real-time chat infrastructures. Certified <b>AWS Solutions Architect</b> with deep full-stack proficiency "
        "in NodeJS, TypeScript, Firebase, and scalable cloud systems."
    )
    story.append(Paragraph(summary_text, norm_text_style))
    story.append(Spacer(1, 4))
    
    # ------------------ WORK EXPERIENCE ------------------
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_title_style))
    
    # 1. AMPTALK
    amptalk_title = (
        "<font color='#f8fafc'><b>Amptalk</b></font> &nbsp;|&nbsp; "
        "<font color='#14b8a6'><b>Senior Mobile Engineer</b></font> &nbsp;|&nbsp; "
        "<font color='#64748b'>Tokyo, Japan (Aug 2025 - Present)</font>"
    )
    story.append(Paragraph(amptalk_title, comp_title_style))
    story.append(Paragraph("• Spearheaded the development of VoIP communication software integration in iOS using Swift and Flutter.", bullet_style))
    story.append(Paragraph("• Scaled client-side audio streaming pipelines, integrating audio session guidelines for smooth call handoffs.", bullet_style))
    story.append(Paragraph("• Deployed cloud backend integration modules utilizing Node.js, Typescript, and AWS.", bullet_style))
    story.append(Paragraph("<b>Technologies:</b> Flutter, Dart, Swift, Firebase, AWS, Node.js, TypeScript", tag_style))
    story.append(Spacer(1, 6))
    
    # 2. OPN THAILAND
    opn_title = (
        "<font color='#f8fafc'><b>Opn Thailand</b> (formerly Omise)</font> &nbsp;|&nbsp; "
        "<font color='#64748b'>Bangkok, Thailand (Jul 2022 - Jul 2025)</font>"
    )
    story.append(Paragraph(opn_title, comp_title_style))
    
    # Promoted Role
    story.append(Paragraph("Senior Mobile Engineer &nbsp;<font color='#64748b' size='8'>(Promoted Jul 2024 - Jul 2025)</font>", role_title_style))
    story.append(Paragraph("• Architected payment SDK systems handling multi-million dollar transactions for enterprise clients in Southeast Asia.", bullet_style))
    story.append(Paragraph("• Led migrations of legacy UI platforms to SwiftUI, resolving core layout threads and reducing render times by 20%.", bullet_style))
    story.append(Paragraph("• Configured DevOps pipelines via Fastlane and GitHub Actions, cutting delivery cycles to TestFlight and Play Store by 40%.", bullet_style))
    story.append(Paragraph("• Supervised mobile engineering standards, conducting reviews, writing modular frameworks, and onboarding new staff.", bullet_style))
    
    # Junior Role
    story.append(Paragraph("Software Engineer &nbsp;<font color='#64748b' size='8'>(Jul 2022 - Jun 2024)</font>", role_title_style))
    story.append(Paragraph("• Integrated secure card tokenization modules matching PCI-DSS compliance specifications across regional APIs.", bullet_style))
    story.append(Paragraph("• Programmed core components for native iOS payment SDKs, maintaining robust offline safety nets.", bullet_style))
    story.append(Paragraph("• Deployed and maintained Firebase push notification suites and Firestore real-time client databases.", bullet_style))
    story.append(Paragraph("<b>Technologies:</b> SwiftUI, Swift, Firebase, Firestore, REST APIs, Fastlane, CI/CD, Git", tag_style))
    story.append(Spacer(1, 6))
    
    # 3. ONE ATKHYAR
    oneatkhyar_title = (
        "<font color='#f8fafc'><b>One Atkhyar</b></font> &nbsp;|&nbsp; "
        "<font color='#14b8a6'><b>Mobile Engineer</b></font> &nbsp;|&nbsp; "
        "<font color='#64748b'>Yangon, Myanmar (Mar 2019 - Jun 2022)</font>"
    )
    story.append(Paragraph(oneatkhyar_title, comp_title_style))
    story.append(Paragraph("• Built the flagship lifestyle/e-commerce app 'Shi Del' from scratch, scaling client adoption to over 100k active users.", bullet_style))
    story.append(Paragraph("• Designed highly responsive UI flows using Flutter and Dart, incorporating state management (Bloc) and clean architecture.", bullet_style))
    story.append(Paragraph("• Configured Algolia search nodes and real-time Firestore database triggers to manage heavy product catalog indices.", bullet_style))
    story.append(Paragraph("• Programmed backend microservice layers using Node.js, TypeScript, and Firebase Cloud Functions.", bullet_style))
    story.append(Paragraph("<b>Technologies:</b> Flutter, Dart, Firebase, Firestore, Algolia, TypeScript, NodeJS, Clean Architecture, Confluence", tag_style))
    story.append(Spacer(1, 8))
    
    # Force Page Break to prevent overflow and keep layout clean
    story.append(PageBreak())
    
    # 4. CLOUDSOURCE MYANMAR
    cloudsource_title = (
        "<font color='#f8fafc'><b>Cloudsource Myanmar</b></font> &nbsp;|&nbsp; "
        "<font color='#14b8a6'><b>Full Stack Developer</b></font> &nbsp;|&nbsp; "
        "<font color='#64748b'>Yangon, Myanmar (Jul 2018 - Sep 2019)</font>"
    )
    story.append(Paragraph(cloudsource_title, comp_title_style))
    story.append(Paragraph("• Programmed responsive client web portals and administrative dashboards using Laravel and Ruby on Rails.", bullet_style))
    story.append(Paragraph("• Configured complex SQL schemas, transactional index optimizations, and API integrations in PostgreSQL databases.", bullet_style))
    story.append(Paragraph("• Maintained server hosting deployments, integrating secure SSL handshakes and cron monitoring automation.", bullet_style))
    story.append(Paragraph("<b>Technologies:</b> Ruby on Rails, Laravel, PostgreSQL, PHP, Ruby, SQL, Apache", tag_style))
    story.append(Spacer(1, 6))
    
    # 5. ACROQUEST MYANMAR
    acroquest_title = (
        "<font color='#f8fafc'><b>Acroquest Myanmar Technology</b></font> &nbsp;|&nbsp; "
        "<font color='#14b8a6'><b>Software Engineer Intern</b></font> &nbsp;|&nbsp; "
        "<font color='#64748b'>Yangon, Myanmar (May 2017 - Aug 2017)</font>"
    )
    story.append(Paragraph(acroquest_title, comp_title_style))
    story.append(Paragraph("• Implemented proof-of-concept decentralized utility billing applications detailing smart contract automations.", bullet_style))
    story.append(Paragraph("• Programmed Solidity smart contract validation scripts on private Ethereum testnet networks.", bullet_style))
    story.append(Paragraph("<b>Technologies:</b> Solidity, Smart Contracts, Ethereum, JavaScript, HTML/CSS", tag_style))
    story.append(Spacer(1, 10))
    
    # ------------------ TECHNICAL SKILLS ------------------
    story.append(Paragraph("TECHNICAL SKILLS", section_title_style))
    
    skills_data = [
        [Paragraph("<b>Mobile & Core:</b>", comp_title_style), 
         Paragraph("SwiftUI, Flutter, Swift, Dart, Ionic, Android SDK", norm_text_style)],
        [Paragraph("<b>Backend & Web:</b>", comp_title_style), 
         Paragraph("Node.js, TypeScript, Ruby on Rails, Laravel, PHP, REST APIs, PostgreSQL, SQL", norm_text_style)],
        [Paragraph("<b>Cloud & Infra:</b>", comp_title_style), 
         Paragraph("AWS (S3, EC2, Lambda), Firebase, Cloud Firestore, Firebase Cloud Functions", norm_text_style)],
        [Paragraph("<b>DevOps & Tools:</b>", comp_title_style), 
         Paragraph("Fastlane, CI/CD pipelines, Docker, Git, GitHub Actions, Linear, Notion, Confluence", norm_text_style)]
    ]
    
    skills_table = Table(skills_data, colWidths=[120, 410])
    skills_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 10))
    
    # ------------------ CERTIFICATIONS ------------------
    story.append(Paragraph("CREDENTIALS & CERTIFICATIONS", section_title_style))
    
    certs_data = [
        [Paragraph("<b>2026:</b>", comp_title_style), Paragraph("AWS Certified Solutions Architect – Associate (Credly: 314a6a4e-8b66-437a-9f7d-d75a9f38d05f)", norm_text_style)],
        [Paragraph("<b>2025:</b>", comp_title_style), Paragraph("AWS Certified Cloud Practitioner", norm_text_style)]
    ]
    certs_table = Table(certs_data, colWidths=[60, 470])
    certs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(certs_table)
    story.append(Spacer(1, 10))
    
    # ------------------ PUBLICATIONS ------------------
    story.append(Paragraph("PUBLICATIONS & RESEARCH", section_title_style))
    pub_text = (
        "<b>IEEE Xplore Publication: Blockchain Utility Billing (2019)</b><br/>"
        "Co-authored decentralized utilities systems research detailing automated consumer settlement triggers "
        "via Ethereum smart contracts and cloud integrations. Indexed in IEEE Xplore: <i>https://ieeexplore.ieee.org/document/8920931</i>"
    )
    story.append(Paragraph(pub_text, norm_text_style))
    story.append(Spacer(1, 10))
    
    # ------------------ EDUCATION ------------------
    story.append(Paragraph("EDUCATION", section_title_style))
    edu_text = (
        "<b>Bachelor of Computer Science (B.C.Sc.)</b> &nbsp;|&nbsp; "
        "University of Computer Studies, Yangon, Myanmar (2013 - 2018)"
    )
    story.append(Paragraph(edu_text, norm_text_style))
    story.append(Spacer(1, 10))
    
    # ------------------ LANGUAGES ------------------
    story.append(Paragraph("LANGUAGE PROFICIENCIES", section_title_style))
    langs = [
        "<b>Myanmar:</b> Native Proficiency",
        "<b>English:</b> Intermediate",
        "<b>Chinese:</b> HSK Level 5",
        "<b>Japanese:</b> N4 Level"
    ]
    story.append(Paragraph(" &nbsp;•&nbsp; ".join(langs), norm_text_style))
    
    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == "__main__":
    output_path = "/Users/kyawtmayhlaing/Desktop/development/ai/interactive-portfolio/Kyawt_May_Hlaing_Resume.pdf"
    print(f"Building PDF resume to {output_path}...")
    build_pdf(output_path)
    print("PDF build complete successfully!")
