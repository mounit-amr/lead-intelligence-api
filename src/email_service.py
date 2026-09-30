import os
import resend


RESEND_API_KEY = os.getenv("RESEND_API_KEY")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")

resend.api_key = RESEND_API_KEY


async def send_hot_lead_email(lead, score):
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [NOTIFICATION_EMAIL],
        "subject": f"Hot Lead: {lead.company}",
        "html": f"""
        <h2>New High-Priority Lead</h2>

        <p><strong>Lead ID:</strong> {lead.lead_id}</p>
        <p><strong>Company:</strong> {lead.company}</p>
        <p><strong>Industry:</strong> {lead.industry}</p>
        <p><strong>Employees:</strong> {lead.employees}</p>
        <p><strong>Country:</strong> {lead.country}</p>

        <p><strong>Lead Score:</strong> {score}</p>

        <p><strong>Action:</strong> Contact this lead immediately.</p>
        """
    }

    return await resend.Emails.send_async(params)
# import os
# import aiosmtplib
# from email.message import EmailMessage

# SMTP_HOST = "smtp.gmail.com"
# SMTP_PORT = 587

# SMTP_USERNAME = os.getenv("SMTP_USERNAME")
# SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
# NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL")

# async def send_hot_lead_email(lead, score):
#     message = EmailMessage()
    
#     message["From"] = SMTP_USERNAME
#     message["To"] = NOTIFICATION_EMAIL
#     message["Subject"] = f"Hot Lead = {lead.company}"
    
#     message.set_content(
#         f"""
#     New high priority lead detected
    
#     Lead ID: {lead.lead_id}
#     Company: {lead.company}
#     Industry: {lead.industry}
#     Employees: {lead.employees}
#     Country: {lead.country}

#     Lead Score: {score}
        
#     Action: Contact this lead immediately.
        
#         """ 
#     )
#     await aiosmtplib.send(
#         message,
#         hostname=SMTP_HOST,
#         port=SMTP_PORT,
#         start_tls=True,
#         username=SMTP_USERNAME,
#         password=SMTP_PASSWORD
#     )