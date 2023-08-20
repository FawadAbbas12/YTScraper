import os
from tqdm import tqdm
from pytube import YouTube
import time

def make_dir(path):
    os.makedirs(path,exist_ok=True)

class Audio_Downloader:
    def __init__(self, srt_source,download_formats=['48kbps','128kbps','50kbps','70kbps','160kbps']):
        self.srt_source = os.listdir(srt_source)
        self.download_formats = download_formats
        self._essential_paths = ['./audio','./cache/audio/urls/','./cache/audio/streams/']
        for path in self._essential_paths:
            make_dir(path)
        self.hit_count = 0

    @checkpoint(key=Template('url:{2}.cache'), work_dir='./cache/audio/urls/', refresh=False)
    def _get_audio(self, url, cache):
        streams= None
        isvalid= False
        try:
            streams = YouTube(url).streams.filter(only_audio=True)
            isvalid= True
        except Exception as e:print(e)
        finally: return streams, isvalid

    @checkpoint(key=Template('url:{3}.cache'), work_dir='./cache/audio/streams/', refresh=False)
    def _download_stream(self,save_dir,stream, cache):
        downloaded = False
        try:
            os.makedirs(save_dir,exist_ok=True)
            stream.download(save_dir)
            downloaded = True
        except Exception as e:print(e)
        finally:return downloaded

    def download(self):
        tqdm_list = tqdm(self.srt_source)
        for idx, file in enumerate(tqdm_list):
            tqdm_list.set_description(f'Processing: {idx}: {file}')
            id = file.replace(".str","")
            if not file.split('.')[-1] in ['str','str'] \
            or id.split('_')[-1] in ['a.en'] \
            or os.path.exists(f'audio/{id}') \
            :continue
            link = f'https://youtube.com/{id}'
            audio_sources,is_valid = self._get_audio(link,id)
            if not is_valid:continue
            for audio_source in audio_sources:
                audio_format = audio_source.abr
                if not audio_format in self.download_formats:continue
                save_dir = f'audio/{id}/{audio_format}'
                if os.path.exists(save_dir):continue
                self.hit_count+= 1
                tqdm_list.set_description(f'Processing: {idx},{self.hit_count}: {file}')
                self._download_stream(save_dir,audio_source, f'{id}_{audio_format}')
                if (self.hit_count %(30*len(self.download_formats)))==0 and self.hit_count != 0:
                    print('sleeping for a minute')
                    time.sleep(60)
                # return
