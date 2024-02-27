import requests

class SubtitleDownload:
    def __init__(self, bvid: str, page, cookie: str):
        self.bvid = bvid
        self.page = page
        self.pagelist_api = "https://api.bilibili.com/x/player/pagelist"
        self.subtitle_api = "https://api.bilibili.com/x/player/v2"
        self.headers = {
            'authority': 'api.bilibili.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://www.bilibili.com',
            'referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'cookie': cookie,
        }
        
    def _get_player_list(self):
        response = requests.get(self.pagelist_api, params = {'bvid': self.bvid}, headers = self.headers)
        cid_list = [x['cid'] for x in response.json()['data']]
        return cid_list
    
    def _get_subtitle_list(self, cid: str):
        params = (
            ('bvid', self.bvid),
            ('cid', cid),
        )
        response = requests.get(self.subtitle_api, params = params, headers = self.headers)
        # print(response.json())
        subtitles = response.json()['data']['subtitle']['subtitles']
        if subtitles:
            n = 1
            print("当前字幕列表：")
            for x in subtitles:
                print(str(n) + '.' + x['lan_doc'])
                n = n+1
            m = int(input("请输入下载的字幕序号："))
            return ['https:' + subtitles[m-1]['subtitle_url']]
        else:
            print("获取字幕列表失败，当前没有可下载的字幕，或检查cookie是否正确")
            return None
        return []
    
    def _get_subtitle(self, cid: str):
        subtitles = self._get_subtitle_list(cid)
        if subtitles:
            return self._request_subtitle(subtitles[0])
    
    def _request_subtitle(self, url: str):
        response = requests.get(url)
        if response.status_code == 200:
            body = response.json()['body']
            return body

    def _get_pagelist(self):
        response = requests.get(self.pagelist_api, params = {'bvid': self.bvid}, headers = self.headers)
        pagelist = len(response.json()['data'])
        print(f"当前视频共有分集：{pagelist}")
        page = int(input("请选择集数：")) - 1
        return page

    def download_subtitle(self):
        # self.__init__()
        self.page = self._get_pagelist()
        subtitle_list = self._get_subtitle(self._get_player_list()[self.page])
        if subtitle_list:
            text_list = [x['content'] for x in subtitle_list]
            text = ' '.join(text_list)
            print("字幕获取成功\n")
            return text
        else:
            text = "该视频没有可供下载的字幕"
            return text
    
class SubtitleDownloadError(Exception):
    pass