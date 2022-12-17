from accounts.models import Profile
import requests

TOKEN = "5531357466:AAGLMJlhTQiqnBc471bK4_eM08cVz2uvm5Y"

chat_id = "786206902"
text = "TrazumiTestBot speaks: Hi Gbolahan! Try /help"


def send_message(chat_id=chat_id, text=text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    urlUpdate = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    r = requests.get(url)
    rUpdate = requests.get(urlUpdate)

    print(r.json())
    print()
    print(rUpdate.json())
    print()

    return r.json

def update_profile():
    profile_id = 6
    chat_id = 786206902
    data = {'telegram_chat_id': f'{chat_id}'}
    url = f"http://localhost:3000/profiles/{profile_id}?"
    req = requests.put(url, json=data)

    print(req.json())
    print()

    return req.json

def handle():
    profile = Profile.objects.filter(
        telegram_username='Gbolz').values().first()

    print(profile)
    return profile
