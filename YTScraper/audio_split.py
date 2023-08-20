from threading import Thread
import shutil
from uuid import uuid3
import os
class copyFiles(Thread):
    def __init__(self, source, dest):
        super().__init__()
        self.source = source
        self.dest = dest

    def zip_folder(self):
        zip_file = str(uuid3())+'.zip'
        shutil.make_archive(zip_file, 'zip', self.source)

    def copy(self, zip_file, dest):
        shutil.copy(
            zip_file,
            dest
        )

    def clean_up(self, zip_file):
        shutil.rmtree(self.source)
        os.remove(zip_file)
    def process(self):
        zip_file = self.zip_folder()
        self.copy(zip_file, self.dest)
        self.clean_up(zip_file)

    def run(self):
        self.isRunning = True
        self.process()
        self.isRunning = False


class Split_Audio:
    def __init__(self,
                 data_files_root:str,
                 audio_root:str,
                 out_folder:str,
                 audio_file_exts:list =['mp4','mp3', 'wav','webm'],
                 numthread:int=8
                 ):
        self.data_files = tqdm(glob(f'{data_files_root}/*.data'))
        self.audio_root = audio_root
        self.out_folder = out_folder
        make_dir(self.out_folder)
        make_dir(os.path.join(self.out_folder,'tsv_data'))
        make_dir('./cache/split/')
        self.numthread = numthread
        self.audio_file_exts =audio_file_exts
        with open('done.txt','r')as f:
            self.doneFiles = [line.strip() for line in f.readlines()]

    def get_audio_files(self, file_name):
        audio_folder = os.path.join(self.audio_root, file_name)
        audio_files = []
        if os.path.exists(audio_folder):
            # for dir_name in os.listdir(audio_folder):
            for dir_name in ['48kbps']:
                dir_path = os.path.join(audio_folder, dir_name)
                if not os.path.isdir(dir_path):continue
                files = [f for f in os.listdir(dir_path) if f.split('.')[-1] in self.audio_file_exts]
                for file_name in files:
                    audio_file = {
                        'bitrate': dir_name,
                        'segment': AudioSegment.from_file(os.path.join(dir_path, file_name))
                    }
                    audio_files.append(audio_file)
        return audio_files

    def save_audio(self, name, bitrate, idx, segment, text):
        output_file = os.path.join(self.out_folder,f"{name}/{idx}_{bitrate}.mp3")
        segment.export(output_file, format="mp3")
        with open(os.path.join(self.out_folder,f"tsv_data/{name}.tsv"),'a+') as f:
            f.write(f"{idx}\t{bitrate}\t{output_file}\t{text}\n")

    def process_audio(self, file_name):
        _file_name = os.path.basename(file_name).replace('.data','')
        if _file_name in self.doneFiles:
            print(f'skiping {_file_name}')
            return
        self.doneFiles.append(_file_name)
        self.data_files.set_description(f'processing : {_file_name}')
        with open('done.txt','a+')as f:
            f.write(f'{_file_name}\n')
        make_dir(os.path.join(self.out_folder,f"{_file_name}/"))
        audios = self.get_audio_files(_file_name)
        with open(file_name,'r',encoding='utf-8')as f:
            spoken_lines = f.readlines()

        total =len(spoken_lines)
        for idx, line in enumerate(spoken_lines[:-1]):
            self.data_files.set_description(f'processing : {_file_name} {idx}/{total}')
            line = line.split(',')
            if not len(line)>=3:
                continue
            start = line[0]
            end=line[1]
            text = ', '.join(line[2:])
            start_time = self.get_millisec(start)
            end_time = self.get_millisec(end)
            for audio in audios:
                segment = audio['segment'][start_time:end_time]
                self.save_audio(_file_name,audio['bitrate'], idx, segment, text.strip())
            # time.sleep(60)

    def get_millisec(self, time_str):
        """Get milli seconds from time."""
        h, m, s = time_str.split(':')
        return (int(h) * 3600 + int(m) * 60 + int(s))*1000

    def process(self):
        for idx,data_file in enumerate(self.data_files):
            if os.path.basename(data_file).split('_')[-1] == 'a.en.data':continue
            self.process_audio(data_file)



    @checkpoint(key=Template('url:{3}.cache'), work_dir='./cache/split/', refresh=False)
    def create_thread(self, data_file, executor, cache):
        self.futures.append(executor.submit(self.process_audio, data_file))

    def process_mp(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.numthread) as executor:
            self.futures = []
            for data_file in self.data_files:
                if os.path.basename(data_file).split('_')[-1] == 'a.en.data':continue
                self.create_thread(data_file,executor, os.path.basename(data_file))
            for future in concurrent.futures.as_completed(self.futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error processing file: {str(e)}")

    def merge(self):
        pass

