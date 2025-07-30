from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import os
from tavily import TavilyClient
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LINKEDIN_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN")

llm = ChatOpenAI(model_name="gpt-4", temperature=0.5)
tavily = TavilyClient(api_key=TAVILY_API_KEY)

pending_posts = []

def fetch_ai_news():
    result = tavily.search(query="latest in generative AI, LLMs", search_depth="advanced", include_answers=True)
    return result['results'][:3]

def generate_post(title, content, url):
    prompt = f"""Create a professional LinkedIn post for this tech news:
Title: {title}
Content: {content}

Format:
🚀 Title
🔍 Summary
🔗 Read more: {url}
#AI #LLM #TechNews"""
    return llm.predict(prompt)

def post_to_linkedin(message):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {LINKEDIN_TOKEN}",
        "X-Restli-Protocol-Version": "2.0.0",
        "Content-Type": "application/json"
    }
    payload = {
        "author": f"urn:li:person:{LINKEDIN_PERSON_URN}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": message
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 201

@app.get("/review", response_class=HTMLResponse)
def review_posts():
    html = "<h1>Pending LinkedIn Posts for Approval</h1>"
    for i, post in enumerate(pending_posts):
        html += f"<form method='post' action='/approve'>"
        html += f"<textarea rows='10' cols='100' name='content'>{post}</textarea><br>"
        html += f"<input type='hidden' name='index' value='{i}'>"
        html += f"<button type='submit' name='action' value='approve'>Approve</button>"
        html += f"<button type='submit' name='action' value='reject'>Reject</button>"
        html += "</form><hr>"
    return html or "<p>No posts pending approval.</p>"

@app.post("/approve")
def approve_post(index: int = Form(...), action: str = Form(...), content: str = Form(...)):
    if action == "approve":
        success = post_to_linkedin(content)
        if success:
            print(f"✅ Posted to LinkedIn: {content[:60]}...")
    del pending_posts[index]
    return RedirectResponse("/review", status_code=303)

@app.get("/fetch")
def fetch_and_prepare():
    articles = fetch_ai_news()
    for art in articles:
        post = generate_post(art['title'], art['content'], art['url'])
        pending_posts.append(post)
    return {"status": "Fetched and queued posts for approval."}

@app.get("/")
def root():
    return RedirectResponse("/review")
