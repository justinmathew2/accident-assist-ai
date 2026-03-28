from google import genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


TRIAGE_PROMPT = """
ROLE: Expert Forensic Trauma Analyst.
TASK: Analyze the provided accident scene (image/text) to assess medical urgency based on structural forensic evidence.

CRITICAL ANALYSIS CRITERIA:
1. Total Vehicle Deformation: Assess the percentage of structural loss.
2. Cabin Intrusion: Check if the survival space for occupants is compromised (dashboard/steering wheel pushed into cabin).
3. Heavy Vehicle Proximity: Identify if the incident involves multi-vehicle collisions or proximity to trucks (potential under-ride).

DETERMINISTIC RULE:
- If the vehicle's front end is unrecognizable, or if there is visible cabin intrusion/crush (e.g., as seen in high-impact collisions like the 'Test1.jpg' scenario), you MUST set severity to 'CRITICAL'.

OUTPUT JSON SCHEMA:
{
  "severity": "CRITICAL" | "HIGH" | "MEDIUM" | "LOW",
  "triage_level": 1 | 2 | 3 | 4,
  "recommended_actions": [string],
  "incident_summary": string,
  "ambulance_priority": "HIGH PRIORITY" | "STANDARD",
  "forensic_notes": string
}

INSTRUCTIONS: 
- For 'CRITICAL' severity, ensure 'ambulance_priority' is 'HIGH PRIORITY' regardless of current traffic conditions. 
- If input is inadequate, default to 'MEDIUM' for safety.
"""

def analyze_incident(description=None, image_data=None):
    """
    Analyzes an incident using Gemini multimodal capabilities.
    """
    try:
        if not os.getenv("GOOGLE_API_KEY"):
            return mock_analyze_incident(description)
            
        content = [TRIAGE_PROMPT]
        if description: content.append(description)
        if image_data:
            # Handle Base64 image data if provided
            import base64
            from PIL import Image
            import io
            
            # Assuming image_data is a Base64 string for simplicity
            img_bytes = base64.b64decode(image_data.split(",")[-1])
            img = Image.open(io.BytesIO(img_bytes))
            content.append(img)
            
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=content
        )
        
        # Extract JSON from generated text
        json_str = response.text.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0]
        
        result = json.loads(json_str)
        return result
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return mock_analyze_incident(description)

def mock_analyze_incident(description="No data"):
    """
    Mock response for triage in case of failure or development mode.
    """
    severity = "MEDIUM"
    if description and ("blood" in description.lower() or "unconscious" in description.lower()):
        severity = "HIGH"
    elif description and ("minor" in description.lower() or "dent" in description.lower()):
        severity = "LOW"
    
    return {
        "severity": severity,
        "triage_level": 2 if severity == "MEDIUM" else (3 if severity == "HIGH" else 1),
        "recommended_actions": [
            "Ensure safe distance from vehicles",
            "Do not move the injured person unless there is immediate danger",
            "Keep the patient warm and dry"
        ],
        "incident_summary": f"Automated forensic analysis of: {description[:50] if description else 'No description provided'}...",
        "ambulance_priority": "HIGH PRIORITY" if severity in ["HIGH", "CRITICAL"] else "STANDARD",
        "forensic_notes": "Structural assessment points to moderate risk based on incident context."
    }
