import os
import json
from google import genai

client = genai.Client(
    api_key = os.getenv("gemini key")
)

def build_icp(description: str):
    prompt = f"""
    Convert the following customer despcryption into a structured ICP.
    
    Customer descryption:
    {description}
    
    ndustries: list of strings
countries: list of strings
employees_min: integer or null
employees_max: integer or null
revenue_min: number or null
funding_min: number or null
budget_min: number or null
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return json.loads(response.text)
    
    