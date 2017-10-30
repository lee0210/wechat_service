#!/usr/bin/python
import socket
import os
import sys
import urllib2
import json
from wechat_conf import token_socket
from wechat_conf import appid
from wechat_conf import appsecret
import datetime
import struct

url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'

def request_token():
    response = urllib2.urlopen(url.format(appid, appsecret)).read()
    try:
        r = json.loads(response)
        expires = datetime.datetime.now() + datetime.timedelta(seconds=r['expires_in'])
        return r['access_token'].encode('utf-8'), expires
    except ValueError as err:
        return None, None

def get_token():
    try:
        client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_socket.connect(token_socket)
        client_socket.send('G')
        client_socket.settimeout(5)
        data_length, = struct.unpack('>i', client_socket.recv(4))
        if data_length > 0:
            result, = struct.unpack('>{0}s'.format(data_length), client_socket.recv(data_length))
            return result
        return None
    except Exception as e:
        return None

if __name__ == '__main__':

    if os.path.exists(token_socket): 
        os.unlink(token_socket)
    
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(token_socket)
    server_socket.listen(10)
    
    terminal = False
    
    expired = datetime.datetime.now()
    token = ''
    
    while not terminal:
        client_socket, addr = server_socket.accept()
        option, = struct.unpack('>c', client_socket.recv(1))
        if option == 'G':
            if expired < datetime.datetime.now():
                token, expired = request_token()
            data_length = len(token)
            response = struct.pack('>i{0}s'.format(data_length), data_length, token)
            client_socket.send(response) 
        client_socket.close()
        
    
    
    
    
