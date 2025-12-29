import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from google.genai.types import Part, Blob
from google.adk.tools import ToolContext

async def gen_offer_letter(
    tool_context: ToolContext,
    candidate_name: str,
    job_role: str,
    salary: str
) -> dict:
    """
    Generates an official offer letter PDF and saves it as an artifact.
    """
    tmp_path = f"/tmp/offer_{uuid.uuid4().hex[:6]}.pdf"
    doc = SimpleDocTemplate(tmp_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = [
        Paragraph(f"OFFER LETTER", styles['Title']),
        Spacer(1, 12),
        Paragraph(f"Candidate: {candidate_name}", styles['Normal']),
        Paragraph(f"Role: {job_role}", styles['Normal']),
        Paragraph(f"Annual Salary: {salary}", styles['Normal']),
        Spacer(1, 12),
        Paragraph("Congratulations! We are pleased to offer you this position.", styles['Normal'])
    ]
    
    doc.build(story)

    # Convert to bytes for artifact storage
    with open(tmp_path, "rb") as f:
        pdf_bytes = f.read()

    artifact_filename = f"Offer_{candidate_name.replace(' ', '_')}.pdf"

    # Save to system artifacts
    await tool_context.save_artifact(
        filename=artifact_filename,
        artifact=Part(inline_data=Blob(mime_type="application/pdf", data=pdf_bytes))
    )

    return {
        "status": "PDF Generated",
        "artifact_name": artifact_filename  # This key is vital for the agent
    }