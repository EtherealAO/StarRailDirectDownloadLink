# -*- coding: utf-8 -*-

import collections
import json
import requests
import threading
import traceback


def get_online_json(url, max_retry_times=5):
    print('try to get online json')
    print('url:"{}"\nmax retry times:{}'.format(url, max_retry_times))
    retry_times = 1
    while (retry_times < max_retry_times + 1):
        try:
            print('try times:{}'.format(retry_times))
            stringContent = str(requests.get(url).content, 'utf-8')
            if stringContent != None and stringContent != '':
                online_json = json.loads(stringContent)
                retry_times = max_retry_times + 2
        except:
            retry_times = retry_times + 1
    print('get online json successful\n')
    return online_json


def merge_starrail_json(local_json, online_json):
    print('try to merge starrail json')
    local_json['pre_download_game'] = online_json['data']['pre_download_game']
    latest = online_json['data']['game']['latest']
    if local_json['latest'] != latest:
        deprecated_packages = local_json['deprecated_packages']
        deprecated_packages.append(local_json['latest'])
        local_json['latest'] = latest
    print('merge starrail json successful\n')
    return local_json


def get_starrail_json():
    print('try to get starrail json\n')
    starrail_url = 'https://api-launcher-static.mihoyo.com/hkrpg_cn/mdk/launcher/api/resource?channel_id=1&key=6KcVuOkbcqjJomjZ&launcher_id=33&sub_channel_id=1'
    online_json = get_online_json(starrail_url)
    local_path = 'README.md'
    with open(local_path, 'a+') as local_file:
        print('try to read local file')
        local_file.seek(0)
        try:
            local_json = json.loads(local_file.read().strip().strip('```'), object_pairs_hook=collections.OrderedDict)
        except:
            local_json = {'pre_download_game': '', 'latest': '', 'deprecated_packages': []}
        starrail_json = merge_starrail_json(local_json, online_json)
        local_file.seek(0)
        local_file.truncate()
        json_str = json.dumps(starrail_json, ensure_ascii=False, indent=4, separators=(',', ':'))
        print('try to write local file')
        local_file.write('```\n{}\n```'.format(json_str))
        print('get starrail json successful')


if __name__ == '__main__':
    try:
        t = threading.Thread(target=get_starrail_json)
        t.daemon = True
        t.start()
        t.join(timeout=300)
    except:
        print(traceback.format_exc())
