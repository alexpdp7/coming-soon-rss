import dataclasses
import datetime
from http import server

import httpx
import bs4


def get_comingsoon_links():
    r = httpx.get("https://www.comingsoon.net/")
    s = bs4.BeautifulSoup(r.text)
    return [(a.attrs["href"], a.attrs["title"]) for a in s.find_all("a", title=True)]


@dataclasses.dataclass
class ComingSoonArticle:
    href: str
    title: str
    first_seen: datetime.datetime


class ComingSoon:
    def __init__(self):
        self.href_to_articles = dict()

    def refresh(self):
        links = get_comingsoon_links()
        for href, title in links:
            if href in self.href_to_articles:
                continue
            self.href_to_articles[href] = ComingSoonArticle(
                href, title, datetime.datetime.now()
            )

    def get_newest(self):
        return sorted(
            self.href_to_articles.values(), key=lambda a: a.first_seen, reverse=True
        )


COMING_SOON = ComingSoon()


class Handler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(server.HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        COMING_SOON.refresh()
        self.wfile.write(repr(COMING_SOON.get_newest()).encode("utf8"))


def main():
    server.HTTPServer(("", 8000), Handler).serve_forever()
