# -*- coding: utf-8 -*-
import sys
import json
import requests
if __name__ == "__main__":
    with open('README.md','a+') as readme:
        readme.seek(0)
        sys.stdout = readme
        JsonFile=json.loads(readme.read().strip().strip('```'))
        stringContent=str(requests.get(f'https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/resource?key=eYd89JmJ&launcher_id=18').content,'utf-8')
        latest=json.loads(stringContent)['data']['game']['latest']
        deprecated_packages=JsonFile['deprecated_packages']
        if JsonFile['latest']!=latest:
            deprecated_packages.append(JsonFile['latest'])
            JsonFile['latest']=latest
            readme.seek(0)
            readme.truncate()
            print('```\n'+json.dumps(JsonFile,ensure_ascii=False,indent=4,separators=(',',':'))+'\n```')
