from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from bs4 import BeautifulSoup
import time
import requests

USER_URL = "https://archiveofourown.org/users/{user_name}/profile"
HEADERS = {
    "User-Agent": "Mozilla/6.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
    "refere": "https://example.com",
    "cookie": """your cookie value ( you can get that from your web page) """,
}


@dataclass
class User:
    user_name: str
    url: str = field(init=False)
    user_id: int = field(init=False)
    joined: datetime = field(init=False)

    def __post_init__(self):
        self.url = USER_URL.format(user_name=self.user_name)
        self._scrape_user_data()

    def _scrape_user_data(self):
        req = requests.get(self.url, headers=HEADERS)
        while req.status_code == 429:
            self.log.info("+")
            time.sleep(10)
            req = requests.get(self.url, headers=HEADERS)
        soup = BeautifulSoup(req.text, "lxml")
        soup.find("dl", class_="meta").find_all("dd", class_="")
        joined, user_id = [item.text for item in soup.find("dl", class_="meta").find_all("dd", class_="")]
        self.joined = datetime.strptime(joined, "%Y-%m-%d")
        self.user_id = int(user_id)