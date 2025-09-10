import os
import requests
import json
from datetime import datetime

# Blogger + Gemini API Keys
BLOGGER_API_KEY = os.environ.get("BLOGGER_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def log(msg):
    """Simple logger with time"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def generate_post():
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"

    prompt = """
    Write a 1000+ word SEO-friendly blog post in Hindi on a trending technology topic.
    Include: intro, basics, methods, benefits, uses, FAQs, and conclusion.
    Tone: Human-like and engaging.
    """

    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    if response.status_code != 200:
        log(f"❌ Error from Gemini API: {response.text}")
        return None, None

    result = response.json()
    try:
        article = result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        log(f"❌ Error parsing Gemini response: {e}")
        return None, None

    title = "आज की टेक्नोलॉजी अपडेट्स"
    return title, article

def post_to_blogger(title, content):
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/?key={BLOGGER_API_KEY}"
    data = {
        "kind": "blogger#post",
        "blog": {"id": BLOGGER_BLOG_ID},
        "title": title,
        "content": content
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        log(f"✅ Post published successfully: {title}")
    else:
        log(f"❌ Failed to publish post: {response.text}")

if __name__ == "__main__":
    log("🚀 Starting Auto Blogger Bot...")
    title, article = generate_post()
    if article:
        post_to_blogger(title, article)
    else:
        log("⚠️ No article generated. Skipping post.")
