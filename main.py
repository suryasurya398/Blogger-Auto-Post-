import requests, json, os, random
from datetime import datetime

BLOGGER_API_KEY = os.environ["BLOGGER_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
BLOG_ID = os.environ["BLOG_ID"]

topics = [
    "Best ways to earn money online in 2025",
    "Latest technology trends in India 2025",
    "Health and fitness tips for busy people",
    "Personal finance and savings strategies",
    "Motivation for students preparing for exams",
    "AI tools every Indian must know in 2025",
    "Top startup ideas in India 2025",
    "Digital marketing trends in 2025",
    "Yoga and meditation benefits",
    "Cyber security awareness for beginners"
]

def generate_article(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    prompt = f"Write a 1500+ word SEO-friendly Hindi blog article on: {topic}. Include intro, subheadings, FAQs, and conclusion. Human tone."
    data = {"contents":[{"parts":[{"text": prompt}]}]}
    res = requests.post(url, headers=headers, data=json.dumps(data)).json()
    return res["candidates"][0]["content"]["parts"][0]["text"]

def post_to_blogger(title, content, topic):
    # Free stock image (auto insert based on topic keyword)
    top_img = f"<img src='https://source.unsplash.com/1200x600/?{topic.replace(' ', '')}' alt='{topic}'/>"
    bottom_img = f"<img src='https://source.unsplash.com/1200x600/?{topic.replace(' ', '')},india' alt='{topic}'/>"

    final_content = f"{top_img}<br>{content}<br>{bottom_img}"

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?key={BLOGGER_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {"kind": "blogger#post", "title": title, "content": final_content}
    return requests.post(url, headers=headers, data=json.dumps(data)).json()

if __name__ == "__main__":
    topic = random.choice(topics)
    print(f"Generating article on: {topic}")
    article = generate_article(topic)
    result = post_to_blogger(topic, article, topic)
    print("✅ Posted:", result.get("url", "Check Blogger"))
