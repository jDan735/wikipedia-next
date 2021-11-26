from django.http.response import JsonResponse

from wikipya import Wikipya


async def wikipedia_search(request, q):
    wiki = Wikipya("ru").get_instance()
    s = await wiki.search(q, 10)

    results = []

    for result in s:
        # page, image, url = await wiki.get_all(q)
        image = ""
        opensearch = await wiki.opensearch(result.title, 1)

        results.append(dict(
            title=result.title,
            image=image,
            description=result.snippet,
            url=opensearch.results[0].link.split("/")[-1]))

    return JsonResponse({"results": results})
