
def make(url):
    protocol = "http://"
    return url if url[:7] == protocol else protocol + url