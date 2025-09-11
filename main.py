import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import google.generativeai as genai

# ---- Load from GitHub Secrets (Environment Vars) ----
BLOGGER_SECRET_EMAIL = os.getenv("BLOGGER_SECRET_EMAIL")
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

def generate_article():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = """
    Write a 1000+ word SEO-friendly blog post in Hindi on a trending topic for Indian readers.
    Include: intro, basics, methods, benefits, FAQs, and conclusion.
    Tone: human-like, engaging, and unique.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Gemini error:", str(e))
        return None
def clean_text(s):
    return "".join(ch for ch in s if 32 <= ord(ch) <= 126)  # sirf normal ASCII rakho
def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = GMAIL_USER
    msg["To"] = BLOGGER_SECRET_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, BLOGGER_SECRET_EMAIL, msg.as_string())

if __name__ == "__main__":
    print("🚀 Auto Blogger Bot started...")
    article = generate_article()
    if article:
        today = datetime.datetime.now().strftime("%d %B %Y")
        subject = f"Auto Post - {today}"
        send_email(subject, article)
        print("✅ Post sent successfully!")
    else:
        print("⚠️ No article generated. Skipping...")
