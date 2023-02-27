# -*- coding: utf-8 -*-

import collections
import json
import requests
import traceback

if __name__ == '__main__':
    try:
        genshin_url = 'https://sdk-static.mihoyo.com/hk4e_cn/mdk/launcher/api/resource?key=eYd89JmJ&launcher_id=18'
        with open('README.md', 'a+') as readme:
            readme.seek(0)
            max_retry_times = 5
            retry_times = 0
            print('try to get genshin json from {}'.format(genshin_url))
            while (retry_times < max_retry_times):
                try:
                    stringContent = str(requests.get(genshin_url).content, 'utf-8')
                    if stringContent != None and stringContent != '':
                        retry_times = 10
                except:
                    retry_times = retry_times + 1
                    print('retry times:{}')
            print('get genshin json successful')
            try:
                json_content = json.loads(readme.read().strip().strip('```'), object_pairs_hook=collections.OrderedDict)
            except:
                json_content = {}
            if json_content == {}:
                json_content = {'pre_download_game': '', 'latest': '', 'deprecated_packages': []}
            changed = False
            pre_download_game = None
            pre_download_game = json.loads(stringContent)['data']['pre_download_game']
            if json_content['pre_download_game'] != pre_download_game:
                json_content['pre_download_game'] = pre_download_game
                changed = True
            latest = json.loads(stringContent)['data']['game']['latest']
            if json_content['latest'] != latest:
                deprecated_packages = json_content['deprecated_packages']
                deprecated_packages.append(json_content['latest'])
                json_content['latest'] = latest
                changed = True
            if changed:
                readme.seek(0)
                readme.truncate()
                json_str = json.dumps(json_content, ensure_ascii=False, indent=4, separators=(',', ':'))
                readme.write('```\n{}\n```'.format(json_str))
    except:
        print(traceback.format_exc())
