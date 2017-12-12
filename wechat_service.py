# coding=UTF-8

import logging
import traceback
import config
from locode import router
from locode import http
from locode import exception

#admin = ['oPCK0wmjUd-PtqR03DcBixQO3kQE', 'oPCK0wnFPfPWpwjltz7_1xfaf1ok']
#logging.basicConfig(level=logging.INFO)
#
#def main_entry(e, r):
#    valid_signature, queries = check_signature(e, r)
#    if not valid_signature:
#        header = common.default_text_header()
#        status, content = '200 ', 'invalid request'
#        r(status, header.items())
#        return content
# 
#    if 'echostr' in queries:
#        header = common.default_text_header()
#        status, content = '200 ', queries['echostr']
#        r(status, header.items())
#        return content
#    
#    status, header, content = process(e, r, queries)
#    r(status, list(header.items()))
#    return content
#
#def process(e, r, queries):
#    header = common.default_text_header()
#
#    raw_data = e['wsgi.input'].read(int(e['CONTENT_LENGTH']))
#
#    nonce = queries['nonce'][0]
#    msg_signature = queries['msg_signature'][0]
#    timestamp = queries['timestamp'][0]
#    xml_data = xml.parse_xml(raw_data)
#
#    calc_signature = wxutl.get_signature(wechat_conf.token, xml_data['Encrypt'], timestamp, nonce)
#    assert msg_signature == calc_signature, 'Error: Invalid Message Signature %s, %s' %(msg_signature, calc_signature)
#    
#    xml_data, appid = wxutl.decrypt(xml_data['Encrypt'])
#    assert wechat_conf.appid == appid, 'Error: Invalid App ID'
#
#    xml_data = xml.parse_xml(xml_data)
#    
#    message_type = xml_data['MsgType']
#    if message_type == 'event':
#        if xml_data['Event'] == 'subscribe':
#            content = xml.simple_xml().add_tag('ToUserName', xml_data['FromUserName']) \
#                                      .add_tag('FromUserName', xml_data['ToUserName']) \
#                                      .add_tag('Content', '谢谢订阅') \
#                                      .add_tag('CreateTime', str(int(time.time())+1), False) \
#                                      .add_tag('MsgType', 'text') \
#                                      .text
#            content = wxutl.encrypt(content, wechat_conf.appid)
#    logging.debug(xml_data['FromUserName'])
#    if message_type == 'text':
#        content = xml_data['Content']
#        if content == 'yzm' and xml_data['FromUserName'] in admin:
#            rt = dba.sql().table('login_secret').read({'id':xml_data['FromUserName']})
#            content = rt[0]['secret']
#        content = xml.simple_xml().add_tag('ToUserName', xml_data['FromUserName']) \
#                                  .add_tag('FromUserName', xml_data['ToUserName']) \
#                                  .add_tag('Content', content) \
#                                  .add_tag('CreateTime', str(int(time.time())+1), False) \
#                                  .add_tag('MsgType', 'text') \
#                                  .text
#        logging.debug(content)
#        content = wxutl.encrypt(content, wechat_conf.appid)
#        logging.debug(content)
#
#    timestamp = str(int(time.time()))
#    content = xml.simple_xml().add_tag('Encrypt', content) \
#                              .add_tag('MsgSignature', wxutl.get_signature(content, timestamp, nonce, wechat_conf.token)) \
#                              .add_tag('Nonce', nonce) \
#                              .add_tag('TimeStamp', timestamp, False) \
#                              .text
#
#    return '200 ', header, content


def application(e, r):
    try:
        router.handle(e)
    except Exception as err:
        logging.error(err)
        traceback.print_exc()
        exception.handle(e)
    r(http.get_status(e), list(http.get_header(e).items()))
    print(http.get_content(e))
    return [http.get_content(e).encode(config.encoding)]

