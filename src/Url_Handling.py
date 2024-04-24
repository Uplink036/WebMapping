def get_name_from_URL(url):
    if not checkIfURL(url):
        return None
    return url.split("//")[-1]

def checkIfURL(url):
    if url is None:
        return False
    return url.startswith("http://") or url.startswith("https://")