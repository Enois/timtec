from urlparse import parse_qs
from yurl import URL

def get_youtube_id(url):
    '''
    Parses Youtube urls for video ids.

    Supports the following formats:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    '''
    url = URL(url)
    if url.host == 'youtu.be':
        return url.path[1:]
    elif 'youtube.com' in url.host:
        if url.path.startswith('/watch'):
            return parse_qs(url.query)['v'][0]
        if url.path.startswith('/embed/') or url.path.startswith('/v/'):
            return url.path.split('/')[2]
    else:
        return None
