import random

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from wikipya import Wikipya
from bs4 import BeautifulSoup

import httpx


def wikipedia_search(request):
    template = loader.get_template('wikipedia/index.html')

    with open(str(template.origin)) as file:
        return HttpResponse(file.read())


async def get_wiki_page(request, page_name):
    wiki = Wikipya("ru").get_instance()

    async with httpx.AsyncClient() as client:
        try:
            page_name = page_name.split('#')[0]
            res = await client.get(f"https://ru.wikipedia.org/wiki/{page_name}")
        except Exception:
            s = await wiki.search(page_name.split("#")[0], 1)

            page_name = s[0].title
            print(s[0].title)
            res = await client.get(f"https://ru.wikipedia.org/wiki/{page_name}")

    soup_orig = BeautifulSoup(res.text)
    soup = soup_orig.find_all("div", class_="mw-parser-output")[0]

    # image_url = image.source if image is not None else None
    try:
        image = soup_orig.find_all("table", class_="infobox")[0] \
                         .find_all("a", class_="image")[0].img
    except Exception:
        image = None

    for tag in [
        *soup.find_all("table", class_="infobox"),
        *soup.find_all("span", class_="mw-editsection"),
        *soup.find_all("table", class_="noprint"),
        *soup.find_all("div", class_="navbox"),
        *soup.find_all("div", class_="thumb"),
        *soup.find_all("table", class_="metadata")
    ]:
        try:
            tag.replace_with("")
        except:
            pass

    for p in soup.findAll("p"):
        if p.text.replace("\n", "") == "":
            p.replace_with("")

    # reccomendations = []

    # for link in random.choices(list(filter(lambda x: x.get("title"),
    #         soup.select("a[href]:not(.reference, .columns)"))), k=5):
    #     print(link.get("title"))
    #     card_page = await wiki.page(link.get("title"))

    #     try:
    #         card_image = await card_page.image(100)
    #         card_image = image.source
    #     except:
    #         card_image = None

    #     reccomendations.append({
    #         "title": link.get("title") or link.text,
    #         "url": link["href"],
    #         "description": card_page.parsed[:100],
    #         "image": card_image
    #     })

    # print(reccomendations)

    if image:
        image_url = image["srcset"].split()[-2]
    else:
        image_url = ""

    try:
        page_name = soup_orig.find_all("h1")[0].text
    except:
        pass

    p = soup.find_all("p")[0]
    description = str(p)

    p.replace_with("")

    text = str(soup)

    return render(request, "wikipedia/page.html", context={
        "text": text,
        "title": page_name,
        "description": description,
        "image": image_url,
        # "links": reccomendations
    })
