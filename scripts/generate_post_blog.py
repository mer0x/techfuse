import openai
import datetime
import os
import git

# Setează cheia API OpenAI (NU o lăsa hardcoded, folosește variabile de mediu!)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurare Hugo
REPO_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
POSTS_DIR = os.path.join(REPO_PATH, "content/posts")

# Generare articol folosind GPT-4 Turbo (noua sintaxă OpenAI)
def generate_article():
    prompt = """
    Write a **detailed, technical tutorial** for an IT topic.
    The tutorial must:
    - Be **at least 600 words long**.
    - Contain **real-world tested code examples**.
    - Have a **structured format**: Introduction, Prerequisites, Implementation, Troubleshooting, Conclusion.
    - Be in **Markdown format** for Hugo.
    - Include a **title and relevant tags**.

    Topic: "How to Set Up Docker Networking for Scalable Applications"
    """

    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Noua inițializare OpenAI API

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a technical writer specializing in IT topics."},
                  {"role": "user", "content": prompt}],
        max_tokens=4000,
    )

    return response.choices[0].message.content

# Salvăm articolul generat în Hugo
def save_article(content):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    title = "How to Set Up Docker Networking"
    slug = title.lower().replace(" ", "-")

    post_path = os.path.join(POSTS_DIR, f"{date_str}-{slug}.md")

    frontmatter = f"""---
title: "{title}"
date: {date_str}
tags: ["Docker", "Networking", "DevOps"]
categories: ["DevOps"]
draft: false
---

"""

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + content)

    return post_path

# Execută generarea și salvarea articolului
if __name__ == "__main__":
    article_content = generate_article()
    post_file = save_article(article_content)
    print(f"✅ New post generated and saved: {post_file}")
