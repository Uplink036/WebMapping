def get_name_from_URL(url: str) -> str | None:
    if not isValidURL(url):
        return None
    return url.split("//")[-1]


def isValidURL(url: str) -> bool:
    if url is None:
        return False
    return url.startswith("http://") or url.startswith("https://")
