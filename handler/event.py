from locode import router

def route(e):
    router.next_node(e, e['LOCODE_WECHAT_XML'].get('MsgType'))

def subscribe(e):
    pass
