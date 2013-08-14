from urllib import urlencode


def tab_for(page_id, app_id, ssl=True):
    protocol = ssl and 'https' or 'http'
    param = dict(sk="app_%s" % app_id)
    return "%s://www.facebook.com/%s?%s" % (
        protocol, page_id, urlencode(param)
    )


def url_for_share(url):
    return "https://www.facebook.com/sharer/sharer.php?" + urlencode(
        dict(u=url)
    )
