import logging
import time
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class Chat:
    def __init__(self, id=None, username=None, fullname=None):
        self.chat_id = id
        self.username = username
        self.fullname = fullname
        self.status = "NOT_SET"
        logger.info(f"__init__ {username, fullname}: {id}")

        if self.chat_id != None and self.username != None:
            self.set_chat_id()
    
    def get_profile(self, profile_id):
        # profile_id = 6
        # chat_id = 786206902
        
        url = f"http://web:3000/profiles/{profile_id}"
        profile = requests.get(url)

        print(profile.json())

        if profile is not None:
            logger.info(f"get_profile: username check for {self.username}")
            # profile = Profile.objects.get(telegram_username=self.username)
        else:
            logger.info(f"get_profile: username {self.username} doesn't exist")

        return profile.json()

    def update_profile(self, profile_id, chat_id):
        # profile_id = 6
        # chat_id = 786206902

        data = {'telegram_chat_id': f'{chat_id}'}
        url = f"http://web:3000/profiles/{profile_id}?"
        profile = requests.put(url, json=data)

        print(profile.json())
        logger.info(f"update_profile: {self.username} {self.chat_id}")

        return profile.json()

    def set_chat_id(self):
        profile = self.get_profile(6)

        if profile:
            logger.info(f"set_chat_id: chat_id {self.chat_id} found")
            if self.chat_id is not profile['telegram_chat_id']:
                self.update_profile(6, self.chat_id)
                logger.info(f"set_chat_id: chat_id {self.chat_id} updated")
        else:
            logger.info(f"set_chat_id: username {self.username} doesn't exist")
            return 'Proflie not found'

    def save(self):
        logger.info(f"save {self.username, self.fullname}: {self.chat_id}")
        logger.info(f"save --- {str(time.ctime(time.time()))}")

        self.set_chat_id()
