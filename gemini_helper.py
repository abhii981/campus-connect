import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_complaint(complaint_text: str) -> dict:
    prompt = f"""
You are an AI system used in a university complaint management platform.

From the complaint below, extract:
1. Category (Hostel, Classroom, Library, Academics, Infrastructure, Other)
2. Area / Location (if mentioned, else "Unknown")
3. Urgency (low, medium, high)

Return ONLY valid JSON in this format:
{{
  "category": "...",
  "area": "...",
  "urgency": "..."
}}

Complaint:
\"\"\"{complaint_text}\"\"\"
"""

    response = model.generate_content(prompt)

    try:
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
        return json.loads(text)
    except Exception:
        return {
            "category": "Other",
            "area": "Unknown",
            "urgency": "medium"
        }

def analyze_feedback_summary(feedback_text: str) -> str:
    prompt = f"""
You are an AI assistant helping a university administration.

Analyze the following student feedback and provide:
1. Overall sentiment summary
2. Major positive points
3. Major issues raised
4. Actionable suggestions

Return a concise but informative paragraph.

Feedback:
\"\"\"{feedback_text}\"\"\"
"""

    response = model.generate_content(prompt)
    return response.text.strip()
