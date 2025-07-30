import feedparser
from bs4 import BeautifulSoup
import requests

unwanted_phrases=[
    "Want smarter insights in your inbox? Sign up for our weekly newsletters to get only what matters to enterprise AI, data, and security leaders. Subscribe Now",
    "If you want to impress your boss, VB Daily has you covered. We give you the inside scoop on what companies are doing with generative AI, from regulatory shifts to practical deployments, so you can share insights for maximum ROI.",
    "Read our Privacy Policy",
    "Thanks for subscribing. Check out more VB newsletters here.",
    "An error occured."
]

def clean_content(content):
    for phrase in unwanted_phrases:
        if phrase in content:
            content = content.replace(phrase, "")
    return content.strip()



def get_news():
    feed = feedparser.parse("https://venturebeat.com/category/ai/feed/")
    top_links = []
    for article in feed.entries[:7]:
        try:
            url = article.link
            html_content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).text
            soup = BeautifulSoup(html_content, 'html.parser')
            textBlock = soup.find('div', {'class': 'article-content'})
            content = clean_content(
                "\n".join(p.text.strip() for p in textBlock.find_all('p'))) if textBlock else "No content found."

        except Exception as e:
            print(f"Failed to retrieve content from {url}: {str(e)}")
            content = "Failed to retrieve content."

        top_links.append({
            "title": article.title,
            "content": content,
            "url":url
        })

    return top_links




