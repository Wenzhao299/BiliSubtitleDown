from subtitle_down import SubtitleDownload
import json

if __name__ == '__main__':
    with open('settings.json') as f:
        cookie = json.load(f)['cookie']

    bvid = input("请输入视频bv号：")
    p_num = 0
    pagelist = SubtitleDownload(bvid, p_num, cookie)._get_pagelist()
    print(f"当前视频共有分集：{pagelist}")
    p_num = int(input("请选择集数：")) - 1
    
    subtitle = SubtitleDownload(bvid, p_num, cookie).download_subtitle()
    print("字幕获取成功\n")
    print(subtitle)