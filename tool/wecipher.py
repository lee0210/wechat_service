#!/usr/bin/env python
#-*- encoding:utf-8 -*-

from Crypto.Cipher import AES
import sys
import wechat_conf
reload(sys)
sys.setdefaultencoding('utf-8')

block_size = 32
population = [chr(x) for x in range(0,255)]

def pack(data):
    n = block_size - len(data) % block_size
    if n is 0:
        n = block_size
    return data + n * chr(n)

def unpack(data):
    n = ord(data[-1])
    if n < 1 or n > 32:
        return data
    return data[:-n]

def random_str(length):
    return ''.join(random.sample(population, length))    
        





