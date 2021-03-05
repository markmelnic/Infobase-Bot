from datetime import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

UA = UserAgent()
BASE_URL = "https://www.infobase.md/ro/"

class Explorer:
    def __init__(self, entity):
        self.entity = entity
        self.headers = {"User-Agent": UA.chrome, "referer": BASE_URL}
        self.session = HTMLSession()
        self.results = self.make_request()
        print(self.results)

    def make_request(self) -> str:
        response = self.session.get(
            BASE_URL + 'search?q=' + self.entity.replace(' ', '%20'),
            headers=self.headers
        )
        response.html.render()
        soup = BeautifulSoup(response.content, "html.parser")
        print(soup)
        return soup.find_all(_class = "MuiCardContent-root")
