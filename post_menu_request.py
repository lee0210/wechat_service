import sys
import wxutl
import urllib.parse
import http.client

url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}'

print(sys.argv)

f = open(sys.argv[1], 'r')
data = f.read()
f.close()
print(data)

access_token = wxutl.get_access_token()

data = urllib.parse.urlencode({'body': data}, encoding = 'utf-8')
print(data)


hc = http.client.HTTPConnection('')

response = urllib.request.request(url.format(access_token), data, header, method = 'POST').read()
#print(response)
