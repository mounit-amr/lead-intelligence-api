import os
import aiosmtplib
from email.message import EmailMessage

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")

async def send_hot_lead_email(lead, score):
    message = EmailMessage()
    
    message["From"] = SMTP_USERNAME
    message["To"] = NOTIFICATION_EMAIL
    message["Subject"] = f"Hot Lead = {lead.company}"
    
    message.set_content(
        f"""
    New high priority lead detected
    
    Lead ID: {lead.lead_id}
    Company: {lead.company}
    Industry: {lead.industry}
    Employees: {lead.employees}
    Country: {lead.country}

    Lead Score: {score}
        
    Action: Contact this lead immediately.
        
        """ 
    )
    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD
    )