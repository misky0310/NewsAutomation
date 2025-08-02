from groq import Groq
import os
import time
from dotenv import load_dotenv
load_dotenv()
from VB_News import get_news

def get_news_summary():
    groq_key = os.getenv("GROQ_KEY")

    client = Groq(
        api_key=groq_key,
    )
    news_summary = []
    aggregated_news = get_news()

    print("Fetching news summaries...")

    for news in aggregated_news:
        if news.get("content") == "Failed to retrieve content.":
            continue

        prompts = [
            {
                "role": "system",
                "content": '''You are an expert summariser , given the title and content of news article , summarise it in a way so as to retain
                            all the necessary information and put across to the user the main idea of the article. Briefly explain the article
                            and bring out the main discussion points and general news idea.Provide ONLY the summarised news.Return the summarised news only , 
                            NOTHING LESS , NOTHING MORE. Strictly follow the guidelines provided in the prompt.
                '''
            },
            {
                "role": "user",
                "content": f'''
                        Title :- {news.get("title")}\n
                        Content :- {news.get("content")}
                '''
            }
        ]
        print("Summarizing news...")
        chat_completion = client.chat.completions.create(
            messages=prompts,
            model="llama-3.1-8b-instant"
        )

        news_summary.append({
            "title": news.get("title"),
            "summary": chat_completion.choices[0].message.content,
            "url": news.get("url")
        })

        time.sleep(5)
    print("News summaries fetched successfully.")
    return news_summary
