### Actively soliciting contributors!

Have ideas for how YTScraper can be improved? Feel free to open an issue or a pull request!

# YTScraper
*YTScraper* is a simple Python tool (based on pytube) aimed to create text, audio and video datasets from youtube.

## Ambition
The ambition of this project is to make an interactive tool for collecting audio training data for finetuning multimodal LLM or audio transcription or translation.

## TODO 
- Save video owner information so that we can ask for their permission to use data
- Add an audio filtering module to remove background noise   
- Add module to generate audio embeddings 
- And much more 

## Quickstart

### Installation

YTScraper is currently developed for AI/ML engineers and requires an installation of Python 3.6 or greater, as well as wheel and setup tools.
To install run the following command:

```bash
$ git clone https://github.com/FawadAbbas12/YTScraper
$ cd YTScraper
```
```bash
$ pip install .
```
or 

```bash
$ python setup.py install
```


### Using YTScraper in a Python script

To download a subs and audio using the library in a script, you'll need to import the Subtitle_downloader class from the library which will scan for reuired subtitles in video and download them. From there, you can further download audio for videos which have the desired subs and then split then on bases of sub time stamp.

```python
 # download subs
 >>> class SOURCE_TYPE:
      PLAYLIST='playlist'
      VIDEO_LIST='videos'
      VIDEO='video'

 >>> from YTScraper import Subtitle_downloader
 >>> Subtitle_downloader( 
    source, # can be a video/playlist url or a file with multiple video links  
    source_type:SOURCE_TYPE, # show correct source type from  SOURCE_TYPE cass
    language_filter=['en', 'ur'], # language tag for sub
    download_auto_generated=False # download youtube auto sus for given language tag 
    ).download()

    # This will save the subtutltles uner subtitles/{language}/ directory
  ######
``# OR
  data_list = [
      'https://www.youtube.com/watch?v=zQtLIp1TXQE&list=PLb2aaNHUy_gGjz5E2R9ufU_14gITmpTpm'
      # 'https://www.youtube.com/playlist?list=PLS19FEYA85DgxHWVvKUUG8gxGVfCXiLnB'
      # 'https://www.youtube.com/watch?v=rRFA2OF9ZO4&list=UULFy2QNyhhTND6hx80pHNB1zg',
      # 'https://www.youtube.com/watch?v=71oHy1VAY0Q&list=UULFVv5Z0rUq122Yiq9mRNTpJQ',
      # 'https://www.youtube.com/watch?v=8umnbZ0LwbQ&list=UULFV48hMI--HOi-fGZ7019RVg',
      # 'https://www.youtube.com/watch?v=aDeimNINv7A&list=UULF44l9XMwecN5nSgIF2Dvivg',
      # 'https://www.youtube.com/watch?v=np7QxKOF9Bc&list=UULPrUvSaacXAvxu5pbQDdfgLA',
      # 'https://www.youtube.com/watch?v=oBMSjdbA9-o&list=UULFyG1lWu497KzOKeIwdDvwxA',
      # 'https://www.youtube.com/watch?v=sZ-QfeiCwKM&list=UULPXKfR4_mJlcpveUxD0Jqz7g',
      # 'https://www.youtube.com/watch?v=ZdrcXaW_AmQ&list=UULFFSxPOD_6miBXa71Vx1UDBg',
      # 'https://www.youtube.com/watch?v=gwgfdGow9K0&list=PL3FMLcIo9R3Cj0EUWuQjj8msx-QAOZ7lT',
      # 'https://www.youtube.com/watch?v=A98pFNA0Xu8&list=UULF00CEaGLWf6X6-F6XuuHe2A',
      # 'https://www.youtube.com/watch?v=3_6btSfFdHo&list=PLS19FEYA85DhZtdMPi0eyAngXPbYQIMji',
  ]
  downloader = Subtitle_downloader(data_list,SOURCE_TYPE.PLAYLIST)
  downloader.download()
  downloader.show_download_summary()
```

```python
 # Download audio for subs
 >>> from YTScraper import Audio_Downloader 
 >>> Audio_Downloader(
      srt_source, # Source folder where srt files have been downloaded
      download_formats=[ # youtube audio bitrate
        '48kbps',
        '128kbps',
        '50kbps',
        '70kbps',
        '160kbps']
    ).download()

    # this will save audios under ./audio/{id}/{audio_format} direcoty 
    # whereas id is youtube video id and audio_format is birate of audio
```


```python
 # split audio files according to subs time stamp
 >>> from YTScraper import SplitAudio
     SplitAudio(
      data_files_root:str, # root directory for srt files 
      audio_root:str, # root folder whihc contains all audio files as id/bitrate/*.audio.*
      out_folder:str, # diretory to save splittted audio files 
      audio_file_exts:list =[
        'mp4',
        'mp3', 
        'wav',
        'webm'
        ],
      numthread:int=8
      ).process()
```

