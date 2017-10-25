import os
import youtube_dl
import time
import sys

DOWNLOAD_PERCENT = 0
CURRENT_WD = os.getcwd()

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

# https://youtu.be/vSFH1T3SnBY
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
        fmt = meta['formats']
        for f in fmt:
            try:
                #.split('-')[1]
                print(f['format']+" "+str(f['filesize']/(1048576)) +"Mb ")
            except:
                pass
        
        print 'description : %s' %(meta['thumbnail'])
    else:
        print("No data to show")

def create_folder(folder_name):
    folder_path = os.path.join(os.sep, CURRENT_WD, folder_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_path)
        return (True, folder_path)
    else:
        print("Folder already exixts")
        folder_name = raw_input("Enter folder name manually:- ")
        folder_path = os.path.join(os.sep, CURRENT_WD, folder_name)
        os.mkdir(folder_path)
        return (True, folder_path)


def get_video_info(url):
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(url, download=False)
            return meta
    except:
        return None
        # print_video_info(meta)
 

def get_video_formats(meta):
    fmt = meta['formats']
    for f in fmt:
        try:
            #.split('-')[1]
            # print(list(f['format'].split('-')[1]+" "+f['ext']+" "+str(f['filesize']/(1048576)) +"Mb "))
            print(f['format'].split('-')[1]+" "+f['ext']+" "+str(f['filesize']/(1048576)) +"Mb ")
        except:
            pass

def download(url):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
         ydl.download([url])


url = raw_input("Enter URL :- ")

if url:
    information = get_video_info(url)
    if information is not None:
        status, path = create_folder(information['title'])

        if status:
            os.chdir(path)
            download(url)
        else:
            print("Error in download please try again")
else:
    print("*************** No URL found ***************")


