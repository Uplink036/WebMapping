def get_name_from_URL(url: str) -> str | None:
    if not is_valid(url):
        return None
    return url.split("//")[-1]


def is_valid(url: str) -> bool:
    if url is None:
        return False
    return url.startswith("http://") or url.startswith("https://")
