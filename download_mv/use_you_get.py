import sys

from you_get import common as you_get
url = "https://www.bilibili.com/video/BV1nMQSYGEH1/?share_source=copy_web&vd_source=b2e9e1dfdf1c9b8f1da0d25877e5926f"
# url = input("请输入视频链接：")

sys.argv = ['you-get', url, '--cookies', 'cookies.txt']
playlist = input("是否下载视频列表？(y/n): ")
if playlist.lower() == 'y':
    sys.argv.append('--playlist')
you_get.main()
