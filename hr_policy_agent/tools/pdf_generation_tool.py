import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor
from google.genai.types import Part, Blob
from google.adk.tools import ToolContext

async def gen_offer_letter(
    tool_context: ToolContext,
    candidate_name: str,
    job_role: str,
    salary: str
) -> dict:
    """
    Generates a professional, visually appealing offer letter PDF
    and saves it as an artifact.
    """
    tmp_path = f"/tmp/offer_{uuid.uuid4().hex[:6]}.pdf"
    doc = SimpleDocTemplate(tmp_path, pagesize=letter,
                            leftMargin=50, rightMargin=50, topMargin=40, bottomMargin=40)

    styles = getSampleStyleSheet()

    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        textColor=HexColor("#1A237E"),
        fontSize=22,
        leading=28,
        spaceAfter=20
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor("#0D47A1"),
        spaceBefore=18,
        spaceAfter=8
    )

    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=6
    )

    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        alignment=TA_CENTER,
        textColor=HexColor("#555555")
    )

    today = datetime.now().strftime("%B %d, %Y")

    story = []

    # --- HEADER / TITLE ---
    story.append(Paragraph("OFFICIAL OFFER LETTER", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#1A237E")))
    story.append(Spacer(1, 18))

    # --- DATE ---
    story.append(Paragraph(f"Date: {today}", normal_text))
    story.append(Spacer(1, 12))

    # --- SECTION 1: Candidate Details ---
    story.append(Paragraph("Candidate Information", section_header))
    story.append(Paragraph(f"<b>Name:</b> {candidate_name}", normal_text))
    story.append(Paragraph(f"<b>Position:</b> {job_role}", normal_text))
    story.append(Paragraph(f"<b>Annual Salary:</b> {salary}", normal_text))
    story.append(Spacer(1, 12))

    # Separator line
    story.append(HRFlowable(width="100%", thickness=0.7, color=HexColor("#B0BEC5")))
    story.append(Spacer(1, 18))

    # --- SECTION 2: Offer Content ---
    story.append(Paragraph("Offer Summary", section_header))

    story.append(Paragraph(
        """
        Congratulations! We are delighted to extend this formal offer of employment.
        Your skills, experience, and passion make you an excellent fit for this role.
        We look forward to seeing the impact you will create as part of our team.
        """,
        normal_text
    ))

    story.append(Spacer(1, 14))

    story.append(Paragraph(
        """
        Please review the terms and confirm your acceptance at the earliest
        convenience. We are excited to welcome you aboard and begin this
        professional journey together.
        """,
        normal_text
    ))

    story.append(Spacer(1, 30))

    # --- SIGNATURE ---
    story.append(Paragraph("<b>HR Department</b>", normal_text))
    story.append(Paragraph("Company Name Pvt. Ltd.", normal_text))

    story.append(Spacer(1, 40))

    # --- FOOTER ---
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#CCCCCC")))
    story.append(Paragraph("This is a computer-generated document. No signature required.", footer_style))

    # Build PDF
    doc.build(story)

    # Convert to bytes for artifact storage
    with open(tmp_path, "rb") as f:
        pdf_bytes = f.read()

    artifact_filename = f"Offer_{candidate_name.replace(' ', '_')}.pdf"

    await tool_context.save_artifact(
        filename=artifact_filename,
        artifact=Part(
            inline_data=Blob(mime_type="application/pdf", data=pdf_bytes)
        )
    )

    return {
        "status": "PDF Generated",
        "artifact_name": artifact_filename
    }
