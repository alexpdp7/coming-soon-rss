import httpx
import bs4


def get_comingsoon_links():
    r = httpx.get("https://www.comingsoon.net/")
    s = bs4.BeautifulSoup(r.text)
    return [(a.attrs["href"], a.attrs["title"]) for a in s.find_all("a", title=True)]
