from Groq_summarisation import get_news_summary
import pywhatkit as kit
from datetime import datetime, timedelta,date
import os
from dotenv import load_dotenv

load_dotenv()

#get the phone number
phone = os.getenv("PHONE")

#get the message to be sent
def get_msg():
    print("Getting latest news summary...")
    news_summary = get_news_summary()

    msg=f"*AI DAILY DIGEST - {datetime.now().strftime('%d-%m-%Y')}:*\n\n"
    for idx,news in enumerate(news_summary, start=1):
        msg += (
            f"*{idx}. {news.get('title').strip()}*\n"
            f"_{news.get('summary').strip()}_\n"
            f"🔗 Read more: {news.get('url')} \n\n"
        )
    return msg.strip()

def send_msg_whatsapp(phn,msg):
    # now = datetime.now()
    # send_time = now +timedelta(minutes=1)
    # hour = send_time.hour
    # minute = send_time.minute

    # print(f"Sending message to {phn} at {hour}:{minute}")

    #send the message using pywhatkit
    kit.sendwhatmsg_instantly(phn,msg,wait_time=20,tab_close=True,close_time=3)

message = get_msg()
send_msg_whatsapp(phone,message)