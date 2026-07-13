def remove_duplicates(news):

    seen = set()
    unique = []

    for article in news:

        url = article["url"]

        if url not in seen:

            unique.append(article)

            seen.add(url)

    return unique


def validate(article):

    required = [
        "title",
        "url",
        "content"
    ]

    return all(article.get(field) for field in required)