import time
import datetime
from locode import dba
from locode import router
from locode import xml

def route(e):
    content = e['LOCODE_WECHAT_XML'].get('Content')
    command = content.split(': ')
    if len(command) == 2:
        router.next_node(e, command[0])   
    if content == 'yzm':
        router.next_node(e, 'captcha')   
    else:
        router.next_node(e, 'default')

def register(e):
    pass

def captcha(e):
    dba.table('user_auth')\
        .insert({
            'id': e.get('LOCODE_WECHAT_XML').get('FromUserName'),
            'password': '00000000',
            'expire_time': 


def default(e):
    xml_data = e['LOCODE_WECHAT_XML']
    content = xml.simple_xml()\
        .add_tag('ToUserName', xml_data['FromUserName']) \
        .add_tag('FromUserName', xml_data['ToUserName']) \
        .add_tag('Content', xml_data['Content']) \
        .add_tag('CreateTime', str(int(time.time())+1), False) \
        .add_tag('MsgType', 'text') \
        .text
    e['LOCODE_WECHAT_RESPONSE'] = content

