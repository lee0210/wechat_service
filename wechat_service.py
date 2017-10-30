# coding=UTF-8

import common
import urllib.parse
import hashlib
import wechat_conf
import os
import logging
import time
import cgi
import time
import wxutl
from locode import xml
from locode import dba
from flup.server.scgi import WSGIServer

admin = ['oPCK0wmjUd-PtqR03DcBixQO3kQE', 'oPCK0wnFPfPWpwjltz7_1xfaf1ok']
logging.basicConfig(level=logging.INFO)

def main_entry(e, r):
    valid_signature, queries = check_signature(e, r)
    if not valid_signature:
        header = common.default_text_header()
        status, content = '200 ', 'invalid request'
        r(status, header.items())
        return content
 
    if 'echostr' in queries:
        header = common.default_text_header()
        status, content = '200 ', queries['echostr']
        r(status, header.items())
        return content
    
    status, header, content = process(e, r, queries)
    r(status, list(header.items()))
    return content

def process(e, r, queries):
    header = common.default_text_header()

    raw_data = e['wsgi.input'].read(int(e['CONTENT_LENGTH']))

    nonce = queries['nonce'][0]
    msg_signature = queries['msg_signature'][0]
    timestamp = queries['timestamp'][0]
    xml_data = xml.parse_xml(raw_data)

    calc_signature = wxutl.get_signature(wechat_conf.token, xml_data['Encrypt'], timestamp, nonce)
    assert msg_signature == calc_signature, 'Error: Invalid Message Signature %s, %s' %(msg_signature, calc_signature)
    
    xml_data, appid = wxutl.decrypt(xml_data['Encrypt'])
    assert wechat_conf.appid == appid, 'Error: Invalid App ID'

    xml_data = xml.parse_xml(xml_data)
    
    message_type = xml_data['MsgType']
    if message_type == 'event':
        if xml_data['Event'] == 'subscribe':
            content = xml.simple_xml().add_tag('ToUserName', xml_data['FromUserName']) \
                                      .add_tag('FromUserName', xml_data['ToUserName']) \
                                      .add_tag('Content', '谢谢订阅') \
                                      .add_tag('CreateTime', str(int(time.time())+1), False) \
                                      .add_tag('MsgType', 'text') \
                                      .text
            content = wxutl.encrypt(content, wechat_conf.appid)
    logging.debug(xml_data['FromUserName'])
    if message_type == 'text':
        content = xml_data['Content']
        if content == 'yzm' and xml_data['FromUserName'] in admin:
            rt = dba.sql().table('captcha').read({'id':'main'})
            content = rt[0]['code']
        content = xml.simple_xml().add_tag('ToUserName', xml_data['FromUserName']) \
                                  .add_tag('FromUserName', xml_data['ToUserName']) \
                                  .add_tag('Content', content) \
                                  .add_tag('CreateTime', str(int(time.time())+1), False) \
                                  .add_tag('MsgType', 'text') \
                                  .text
        logging.debug(content)
        content = wxutl.encrypt(content, wechat_conf.appid)
        logging.debug(content)

    timestamp = str(int(time.time()))
    content = xml.simple_xml().add_tag('Encrypt', content) \
                              .add_tag('MsgSignature', wxutl.get_signature(content, timestamp, nonce, wechat_conf.token)) \
                              .add_tag('Nonce', nonce) \
                              .add_tag('TimeStamp', timestamp, False) \
                              .text

    return '200 ', header, content

def check_signature(e, r):
    queries = urllib.parse.parse_qs(e['QUERY_STRING'])
    keys = ['signature', 'timestamp', 'nonce']
    if len(keys) != sum([x in keys for x in queries]):
        return False, None
    string_array = queries['timestamp'] + queries['nonce'] + [wechat_conf.token]
    string_array.sort()
    signature = hashlib.sha1((''.join(string_array)).encode('utf-8')).hexdigest()
    if signature != queries['signature'][0]:
        return False, None
    return True, queries

if __name__ == '__main__':
    if os.path.exists(wechat_conf.wechat_socket):
        os.remove(wechat_conf.wechat_socket)
    WSGIServer(main_entry, bindAddress=wechat_conf.wechat_socket, loggingLevel=logging.INFO).run()
