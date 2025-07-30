# 🤖 AI Tech News Poster with Human-in-the-Loop Approval

This project automatically fetches the latest tech/AI news using Tavily, summarizes the content with an LLM (e.g., OpenAI), and allows a human to approve the post before it is published to LinkedIn via the LinkedIn API.

---

## 🚀 Features

- 🔍 **Tavily Search API** to fetch trending tech/AI news
- 🧠 **LLM Summarization** using OpenAI (or other compatible models)
- 🖼️ **Post preview and approval** via FastAPI web interface
- 🧑‍⚖️ **Human-in-the-loop** to ensure quality and prevent auto-posting
- 🔗 **LinkedIn posting** using LinkedIn API after manual approval

---

## 📦 Requirements

- Python 3.10+
- A [Tavily API Key](https://app.tavily.com/)
- An [OpenAI API Key](https://platform.openai.com/)
- A [LinkedIn Developer App](https://www.linkedin.com/developers/apps)

---

## Server

```uvicorn news_poster:app --reload```

Visit http://localhost:8000/fetch to fetch and queue the latest news.

Then go to http://localhost:8000/review to:

View generated LinkedIn posts

Approve or reject each post manually

Once approved, the post is automatically published to LinkedIn.
