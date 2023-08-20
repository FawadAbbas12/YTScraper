from pytube import Playlist, YouTube
from ediblepickle import checkpoint
import sqlite3
from string import Template
from tqdm import tqdm
import os
class SOURCE_TYPE:
    PLAYLIST='playlist'
    VIDEO_LIST='videos'
    VIDEO='video'

class Subtitle_downloader():
    def __init__(self, 
    source, 
    source_type:SOURCE_TYPE, 
    language_filter=['en', 'ur'], 
    download_auto_generated=False
    ) -> None:
        # self.con = sqlite3.connect(cache_db_file)
        os.makedirs('./cache/urls/', exist_ok=True)
        os.makedirs('./cache/subtitles/', exist_ok=True)
        os.makedirs('.subtitles/', exist_ok=True)
        self.language_filter = language_filter
        if download_auto_generated:
            self.language_filter = [f'a.{language}' for language in language_filter]
        for language in self.language_filter:
            os.makedirs(f'.subtitles/{language}/', exist_ok=True)
        self.source_type = source_type
        if self.source_type == SOURCE_TYPE.VIDEO:
            self.data_source = source
        else:
            with open(source, 'r') as f:self.data_source = f.readlines()
            self.data_source = tqdm(self.data_source)
    
    @checkpoint(key=Template('file_name:{2}_caption_code:{3}.cache'), work_dir='./cache/subtitles/', refresh=False)
    def _get_caption(self, video, file_name, caption_code):
        return video.captions.get_by_language_code(caption_code).xml_captions
    
    def _save_caption(self, video, caption_code):
        file_name = f'{video.watch_url}_{caption_code}.xml'.replace('https://youtube.com/','')
        with open(f'subtitles/{caption_code}/{file_name}','w')as f:
            f.write(self._get_caption(video, file_name, caption_code))
    
    @checkpoint(key=Template('url:{2}.cache'), work_dir='./cache/urls/', refresh=False)
    def _get_video(self, url, cache):
        return YouTube(url)
    
    def _process_video(self, url:str):
        cache_path = url.strip().replace('https://www.youtube.com/watch?v=','')
        # print(cache_path)
        video = self._get_video(url.strip(), cache_path)
        keys = video.captions.keys()
        for caption_code in self.language_filter:
            if caption_code in keys:
                self._save_caption(video, caption_code)
    
    def _process_playlist(self, playlist:Playlist):
        for url in playlist.video_urls:
            self.data_source.set_description(f'Processing {url.replace("https://youtube.com/","")}')
            try:self._process_video(url)
            except:pass

    def _validate_source_type(self, target):
        assert self.source_type == target ,f"Unable to download data as {target} source is set as {self.source_type}"
    
    def _download_playlists(self):
        self._validate_source_type(SOURCE_TYPE.PLAYLIST)
        for url in self.data_source:
            self._process_playlist(Playlist(url))

    def _download_video_list(self):
        self._validate_source_type(SOURCE_TYPE.VIDEO_LIST)
        for url in self.data_source:
            self.data_source.set_description(f'Processing: {url.replace("https://youtube.com/","")}')
            try:self._process_video(url)
            except:pass    
    
    def _download_video(self):
        self._validate_source_type(SOURCE_TYPE.VIDEO)
        self._process_video(self.data_source)
        
    def download(self):
        df = {
            SOURCE_TYPE.PLAYLIST:self._download_playlists,
            SOURCE_TYPE.VIDEO_LIST:self._download_video_list,
            SOURCE_TYPE.VIDEO:self._download_video_list
        }
        df[self.source_type]()