import urllib.request
import urllib.parse
import wxutl

data = '''
{
    "button":[
        {
           "type" : "click",
           "name" : "验证码",
           "key" : "LOCODE_KEY_YZM"
        }
    ]
}'''

access_token = wxutl.get_access_token()
url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={0}'.format(access_token)

data = urllib.parse.urlencode({'body': data})
data = data.encode('utf-8')

req = urllib.request.Request(url, data, method = 'POST')
with urllib.request.urlopen(req) as response:
   the_page = response.read()
print(the_page)
