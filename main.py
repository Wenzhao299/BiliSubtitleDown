from subtitle_down import SubtitleDownload
import json

if __name__ == '__main__':
    with open('settings.json') as f:
        cookie = json.load(f)['cookie']

    bvid = input("请输入视频bv号：")
    subtitle = SubtitleDownload(bvid, 0, cookie).download_subtitle()
    print(subtitle)