import urllib.parse
import wechat_conf
import hashlib
import wxutl
import time
from locode import xml
from locode import http

def validation(e):
    queries = e['LOCODE_HTTP_QUERIES'] = urllib.parse.parse_qs(e['QUERY_STRING'])
    keys = ['signature', 'timestamp', 'nonce']
    if len(keys) != sum([x in keys for x in queries]):
        return False
    string_array = queries['timestamp'] + queries['nonce'] + [wechat_conf.token]
    string_array.sort()
    signature = hashlib.sha1((''.join(string_array)).encode('utf-8')).hexdigest()
    if signature != queries['signature'][0]:
        return False
    return True

def decrypt_xml(e):
    http.set_header(e)
    http.set_content(e, '')
    http.set_status(e, '200 ')
    queries = e['LOCODE_HTTP_QUERIES']
    raw_data = e['wsgi.input'].read(int(e['CONTENT_LENGTH']))
    nonce = queries.get('nonce')[0]
    msg_signature = queries.get('msg_signature')[0]
    timestamp = queries.get('timestamp')[0]
    xml_data = xml.parse_xml(raw_data)
    calc_signature = wxutl.get_signature(wechat_conf.token, xml_data['Encrypt'], timestamp, nonce)
    if msg_signature != calc_signature:
        return False 
    xml_data, appid = wxutl.decrypt(xml_data['Encrypt'])
    if wechat_conf.appid != appid:
        return False
    e['LOCODE_WECHAT_XML'] = xml.parse_xml(xml_data)
    return True

def encrypt_xml(e):
    content = e.get('LOCODE_WECHAT_RESPONSE')
    content = wxutl.encrypt(content, wechat_conf.appid)
    timestamp = str(int(time.time()))
    nonce = e.get('LOCODE_HTTP_QUERIES').get('nonce')[0]
    content = xml.simple_xml().add_tag('Encrypt', content) \
                              .add_tag('MsgSignature', wxutl.get_signature(content, timestamp, nonce, wechat_conf.token)) \
                              .add_tag('Nonce', nonce) \
                              .add_tag('TimeStamp', timestamp, False) \
                              .text
    http.set_content(e, content)
