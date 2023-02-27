# -*- coding: utf-8 -*-

import collections
import json
import requests
import sys
import traceback

if __name__ == "__main__":
    try:
        genshin_url = 'https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/resource?key=eYd89JmJ&launcher_id=18'
        with open('README.md', 'a+') as readme:
            readme.seek(0)
            sys.stdout = readme
            max_retry_times = 5
            retry_times = 0
            print('try to get genshin json from {}'.format(genshin_url))
            while (retry_times < max_retry_times):
                try:
                    stringContent = str(requests.get(genshin_url).content, 'utf-8')
                    if stringContent != None and stringContent != '':
                        retry_times = 5
                except:
                    retry_times = retry_times + 1
                    print('retry times:{}')
            print('get genshin json successful')
            jsonFile = json.loads(readme.read().strip().strip('```'), object_pairs_hook=collections.OrderedDict)
            changed = False
            pre_download_game = None
            try:
                pre_download_game = json.loads(stringContent)['data']['pre_download_game']
            except:
                pre_download_game = ""
            if jsonFile['pre_download_game'] != pre_download_game:
                jsonFile['pre_download_game'] = pre_download_game
                changed = True
            latest = json.loads(stringContent)['data']['game']['latest']
            if jsonFile['latest'] != latest:
                deprecated_packages = jsonFile['deprecated_packages']
                deprecated_packages.append(jsonFile['latest'])
                jsonFile['latest'] = latest
                changed = True
            if changed:
                readme.seek(0)
                readme.truncate()
                print('```\n' + json.dumps(jsonFile, ensure_ascii=False, indent=4, separators=(',', ':')) + '\n```')
    except:
        print(traceback.format_exc())
