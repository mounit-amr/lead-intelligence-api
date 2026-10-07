import os
from fastapi import FastAPI, UploadFile, File,Header, HTTPException
from fastapi.responses import FileResponse
from src.schemas import Lead, ICP
from src.scoring import score_lead
from src.email_service import send_hot_lead_email
from typing import List
import pandas as pd


app = FastAPI(
    title="Lead Intelligence API",
    description="AI-powered B2B lead qualification and scoring API",
    version="0.1.0"
)

API_KEY = os.getenv("API_KEY")

DEFAULT_ICP = ICP(
    industries=["Software", "SaaS", "IT", "CyberSecurity"],
    countries=["India"],
    employees_min=50,
    revenue_min=1_000_000,
    funding_min=500_000,
    budget_min=500_000
)

def verify_api_key(x_api_key: str | None):
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API key is not configured"
        )
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

@app.get("/health")
def health():
    return {
        "Status:" "healthy"
    }
    
# @app.post("/test-lead")
# def testload(lead : Lead):
#     return{
#         "message": "Lead received",
#         "lead": lead
#     }

@app.post("/score")
async def score_lead_endpoint(
    lead: Lead,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    result = score_lead(lead, DEFAULT_ICP)

    if result["priority"] == "high":
        try:
            await send_hot_lead_email(
                lead,
                result["score"]
            )
        except Exception as e:
            print(f"Email notificaton failed: {e}")

    return {
        "lead_id": lead.lead_id,
        **result
    }

@app.post("/qualify")
def qualify_lead(
    lead: Lead,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    result = score_lead(lead, DEFAULT_ICP)

    if result["score"] >= 75:
        action = "Contact immediately"

    elif result["score"] >= 50:
        action = "Follow up soon"

    else:
        action = "Add to nurture campaign"

    return {
        "lead_id": lead.lead_id,
        "qualification": result["classification"],
        "score": result["score"],
        "probability": result["probability"],
        "reasons": result["reasons"],
        "recommended_action": action
    }
    
@app.post("/score/batch")
def score_batch(
    leads: list[Lead],
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    results = []

    for lead in leads:
        result = score_lead(lead, DEFAULT_ICP)

        results.append({
            "lead_id": lead.lead_id,
            **result
        })

    return {
        "total_leads": len(results),
        "results": results
    }
    
@app.post("/score/csv")
async def score_csv(
    file: UploadFile = File(...),
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV file"
        )

    try:
        df = pd.read_csv(file.file)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not read the CSV file"
        )

    required_columns = [
        "lead_id",
        "company",
        "industry",
        "employees",
        "country",
        "revenue",
        "funding"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Missing required columns",
                "missing_columns": missing_columns
            }
        )

    results = []

    for _, row in df.iterrows():

        try:
            lead = Lead(
                lead_id=str(row["lead_id"]),
                company=str(row["company"]),
                industry=str(row["industry"]),
                employees=int(row["employees"]),
                country=str(row["country"]),
                revenue=float(row["revenue"]),
                funding=float(row["funding"])
            )

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid lead data: {str(e)}"
            )

        result = score_lead(lead, DEFAULT_ICP)

        results.append({
            "lead_id": lead.lead_id,
            **result
        })

    return {
        "total_leads": len(results),
        "results": results
    }

@app.post("/webhook")
async def lead_webhook(
    lead: Lead,
    x_api_key: str | None = Header(default=None)
):
    verify_api_key(x_api_key)

    result = score_lead(lead, DEFAULT_ICP)

    if result["priority"] == "high":
        try:
            await send_hot_lead_email(
                lead,
                result["score"]
            )
        except Exception as e:
            print(f"Email notification failed: {e}")

    return {
        "message": "Lead received successfully",
        "lead_id": lead.lead_id,
        **result
    }

@app.get("/demo")
def demo():
    return FileResponse("static/demo.html")

@app.post("/demo/score")
def demo_score(lead: Lead):
    result = score_lead(lead, DEFAULT_ICP)
    
    if result["score"] >= 75:
        action = "Contact this lead immediately"
        
    elif result["score"] >= 50:
        action = "Follow up soon"
    
    else:
        action = "Add to nurture campaign"
        
    return {
        **result, 
        "recommended_action" : action
    }
    
@app.post("/score/custom")
def customscor(
    lead: Lead,
    icp: ICP,
    x_api_key: str | None = Header(default=None) 
               ):
    
    verify_api_key(x_api_key)
    result = score_lead(lead,icp)
    
    return{
        "lead_id": lead.lead_id,
        **result
    }