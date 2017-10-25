import os
import youtube_dl
import time
import sys

DOWNLOAD_PERCENT = 0

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'downloading':
        global DOWNLOAD_PERCENT
        sys.stdout.write("\r%d%%" % DOWNLOAD_PERCENT)
        DOWNLOAD_PERCENT +=1
        sys.stdout.flush()
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
    
def print_video_info(meta):
    if meta:
        print 'upload date : %s' %(meta['upload_date'])
        print 'uploader    : %s' %(meta['uploader'])
        print 'views       : %d' %(meta['view_count'])
        print 'likes       : %d' %(meta['like_count'])
        print 'dislikes    : %d' %(meta['dislike_count'])
        print 'id          : %s' %(meta['id'])
        print 'format      : %s' %(meta['format'])
        print 'duration    : %s' %(meta['duration'])
        print 'title       : %s' %(meta['title'])
        print 'description : %s' %(meta['description'])
    else:
        print("No data to show")

ydl_opts = {
    'format': '22',
    # 'postprocessors': [{
    #     'key': 'FFmpegExtractAudio',
    #     'preferredcodec': 'mp3',
    #     'preferredquality': '192',
    # }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}

url = raw_input("Enter URL :- ")

if url:
    
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     meta = ydl.extract_info(url, download=False) 
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

else:
    print("*************** No URL found ***************")

