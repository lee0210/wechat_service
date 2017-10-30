import base64
import string
import random
import hashlib
import time
import struct
from Crypto.Cipher import AES
import socket
import importlib
import xml.sax
import wechat_conf

block_size = 32
aes_key = base64.b64decode(wechat_conf.aes_key + '=')

def encrypt(data, appid):
    sample = string.digits + string.ascii_letters
    rand_str = ''.join(random.sample(sample, 16))
    data = data.encode('utf-8')
    data = bytes(rand_str, 'utf-8') + struct.pack('I', socket.htonl(len(data))) + data + bytes(appid, 'utf-8')
    data_length = len(data)
    pad_length = block_size - (data_length % block_size)
    pad = bytes(chr(pad_length), 'utf-8')
    data = data + pad * pad_length
    ase_cryptor = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
    cipher = ase_cryptor.encrypt(data)
    return base64.b64encode(cipher).decode('ascii')

def decrypt(data):
    ase_cryptor = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
    plain_text = ase_cryptor.decrypt(base64.b64decode(data))
    pad_length = plain_text[-1]
    content = plain_text[16:-pad_length]
    xml_len = socket.ntohl(struct.unpack('I', content[:4])[0])
    return content[4:4+xml_len].decode('utf-8'), content[4+xml_len:].decode('utf-8')

def get_signature(*arg):
    signature_param = list(arg)
    signature_param.sort()
    return hashlib.sha1(''.join(signature_param).encode('utf-8')).hexdigest()

def get_access_token():
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(wechat_conf.token_socket)
    client_socket.send(b'G')
    client_socket.settimeout(5)
    data_length, = struct.unpack('>i', client_socket.recv(4))
    if data_length > 0:
        result, = struct.unpack('>{0}s'.format(data_length), client_socket.recv(data_length))
        return str(result, 'utf-8')
    return None


if __name__ == '__main__':
    data = 'wXxMmGPJNqjRvrHzoS2Sz2hNM6qosaxGzqN7wkMhKd1MKPFuNR0sXeYJbl/Hqn7CzAfEN8a/PuQMNI+HXX8dtCW+f/ZmOxBbikDuAgnj3x82RnbVMlz6hsrnyVCvpLd1fVgi0+k3ebb7rN9GNDHB411xBp6b1MCgi99T8Z1NyU+qSyNHL6nYm832A3JJHmCPznwa7cHIRtpQMvSXIzTrpFPbmV2MoZsOhd2xHksPGaw7NIYQWOA3qWw9VfcRjduBWR8H9+05bKzkIY3ULzmJfKAimXAkGBwpEu6dAGxtFGyULq4DYcqAssgc6qzeTEK8gHQ6rBXNxavKv1+YbNuYBg=='
    data = encrypt(data, wechat_conf.appid)
    print(data)
    print(decrypt(data))
    print(get_access_token())
