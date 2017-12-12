from locode import router
from locode import http

def route(e):
    if 'echostr' in e['LOCODE_HTTP_QUERIES']:
        router.next_node(e, 'init')
    else:
        router.next_node(e, 'event')

def init(e):
    http.set_header(e)
    http.set_status(e, '200 ')
    http.set_content(e, e['LOCODE_HTTP_QUERIES']['echostr'][0])
