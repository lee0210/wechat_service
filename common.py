from datetime import datetime
from datetime import timedelta

GMT_format = "%a, %d %b %Y %H:%M:%S GMT"

def default_header():
    header = {}
    header['content-type'] = 'text/html'
    dt = datetime.now() + timedelta(days=1)
    header['Expires'] = dt.strftime(GMT_format)
    return header
 
def default_json_header():
    header = {}
    header['content-type'] = 'application/json'
    return header

def default_text_header():
    header = {}
    header['content-type'] = 'text/plain'
    return header
 
