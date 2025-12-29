import requests
import logging
import base64
from google.adk.tools import ToolContext

logger = logging.getLogger(__name__)

async def trigger_webhook(
    tool_context: ToolContext,
    email: str, 
    subject: str, 
    message: str = "", 
    artifact_name: str = None  # The Agent MUST fill this with the returned value from the PDF tool
):
    """
    Sends an email via n8n. 
    If artifact_name is provided, it retrieves the file from storage and attaches it.
    """
    N8N_URL = "https://shashivendra.app.n8n.cloud/webhook/send-email"
    
    encoded_content = None
    
    if artifact_name:
        try:
            # Note: Ensure you are using the correct method for your ADK version.
            # Usually it is load_artifact or get_artifact.
            artifact = await tool_context.load_artifact(artifact_name)
            
            # Extract bytes from the Blob
            file_bytes = artifact.inline_data.data
            encoded_content = base64.b64encode(file_bytes).decode('utf-8')
            logger.info(f"Artifact {artifact_name} loaded and encoded.")
        except Exception as e:
            logger.error(f"Failed to load artifact: {e}")

            # We continue so the email at least sends, but you could return an error here.

    payload = {
        "email": email,
        "subject": subject,
        "message": message,
        "has_attachment": bool(encoded_content),
        "attachment_data": {
            "filename": artifact_name,
            "data": encoded_content,
            "mimetype": "application/pdf",
            "encoding": "base64"
        } if encoded_content else None
    }
    
    try:
        r = requests.post(N8N_URL, json=payload, timeout=30)
        r.raise_for_status()
        return {"status": "success", "message": "Payload delivered to n8n"}
    except Exception as e:
        return {"status": "error", "details": str(e)}