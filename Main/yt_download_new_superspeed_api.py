from pytube import YouTube
from threading import Thread
from bs4 import BeautifulSoup as bs4
import time,os,sys,re
import shutil,requests,psutil
import multiprocessing as mp




class Downloader():

    def __core__(self,yt,multi=False,method=None,select=None,higher=None,alb=True,ip='192.168.0.1',keywords=[]):
        global video,video_fname,video_progress,file_title,audio,audio_fname,audio_progress,file_title2,audio_progress,video_progress
        def fbl():
            import sys,time
            exc_type, exc_obj, exc_tb = sys.exc_info()
            error_inf='error type:  '+str(exc_type)+'\nerror obj:" '+str(exc_obj)+' "\nerror in line:" '+str(exc_tb.tb_lineno)+' "'
            return error_inf
        def progress(stream, chunk, bytes_remaining):
            if stream.type=="audio":
                global audio_progress
                contentSize = audio.filesize
                size = contentSize - bytes_remaining
                audio_progress = round(float(size/contentSize*100),3)
                if audio_progress>=99:
                    audio_progress=89.9
            else:
                global video_progress
                contentSize = video.filesize
                size = contentSize - bytes_remaining
                video_progress = round(float(size/contentSize*100),3)
                if video_progress>=99:
                    video_progress=98.9
        def get_album_art(url):
            global album_request
            album_request=''
            while 1:
                try:
                    album_request = requests.get(url,timeout=10)
                    break
                except:
                    pass
        def get_video_info(url):
            global video_info
            video_info=''
            while 1:
                while 1:
                    try:
                        req=requests.get(url,headers={},timeout=10)
                        break
                    except:
                        pass
                if len(req.content)<1000000:
                    soup=bs4(req.content,'html.parser')
                    try:
                        providor=soup.find(class_='yt-uix-sessionlink spf-link').text
                    except:
                        try:
                            providor=soup.find(class_='yt-uix-sessionlink spf-link ').text
                        except:
                           providor=''
                    try:
                        date_=soup.find(itemprop="datePublished").get('content').split('-')
                        date=date_[0]
                        date_full=date_[0]+date_[1]+date_[2]
                    except:
                        date_full=''
                        date=''
                    try:
                        genre=soup.find(itemprop="genre").get('content').split('-')[0]
                    except:
                        genre=''
                    if date!='':
                        video_info=(providor,date,genre,date_full)
                        break
        def video_downlaoder():
            global video,video_fname,video_progress,file_title,ip
            while 1:
                try:
                    video_fname=video.download('./file/'+self.ip+'/video_tmp')
                    file_title='.'.join(video_fname.replace('/','\\').split('\\')[-1].split('.')[:-1])
                    break
                except:
                    time.sleep(1)
            video_progress=99
        def audio_downloader():
            global audio,audio_fname,audio_progress,file_title2,ip
            while 1:
                try:
                    audio_fname=audio.download('./file/'+self.ip+'/audio_tmp')
                    file_title2='.'.join(audio_fname.replace('/','\\').split('\\')[-1].split('.')[:-1])
                    break
                except:
                    time.sleep(1)
            audio_progress=99
        
        video_progress=0
        audio_progress=0
        cut=0
        yt.register_on_progress_callback(progress)
        copyright_='https://www.youtube.com/watch?v='+yt.video_id
        streams=yt.streams.otf()
        album_thread=Thread(target=get_album_art,args=(yt.thumbnail_url,))
        album_thread.start()
        video_info_thread=Thread(target=get_video_info,args=(copyright_,))
        video_info_thread.start()
        title=yt.title
        res=['4320p','2160p','1440p','1080p','720p','480p','360p','240p','144p']
        res_adv=['4320p','2160p','1440p','1080p','720p','480p','360p','240p','144p']
        fps=[60,30]
        abrs=["160kbps","128kbps"]
        for a in res.copy():
            if len(streams.filter(res=a))==0:
                res.remove(a)
        
        if method=='1':
            if not multi:
                selected=select
            else:
                selected=res_adv.index(select)
                selectedh=''
                selectedl=''
                while not res_adv[selected] in res and selected>=0:
                    selected-=1
                if selected>=0:
                    selectedh=res_adv[selected]
                selected=res_adv.index(select)
                while not res_adv[selected] in res and selected<len(res_adv):
                    selected+=1
                if selected<len(res_adv):
                    selectedl=res_adv[selected]
                selected = selectedh if higher and selectedh!='' or not higher and selectedl=='' else selectedl
            for a in fps:
                videos=streams.filter(type="video",res=selected,fps=a)
                #print(videos)
                if len(videos)>0:
                    break
            backup_v=''
            video=''
            for a in videos:
                if a.audio_codec==None:
                    if a.video_codec.count('vp9')==0:
                        if backup_v=='':
                            backup_v=a
                    else:
                        video=a
                        break
            if video=='':
                video=backup_v
            #print(video)
            backup_a=''
            audio=''
            for a in abrs:
                if len(streams.filter(type="audio",abr=a))>0:
                    audios=streams.filter(type="audio",abr=a)
                    for b in audios:
                        if b.audio_codec.count('opus')==0:
                            if backup_a=='':
                                final_abr=a
                                backup_a=b
                        else:
                            audio=b
                            final_abr=a
                            break
                if backup_a!='' or audio!='':
                    break
            if audio == '':
                audio = backup_a
            #print(audio)
            video_download=Thread(target=video_downlaoder)
            video_download.start()
            audio_download=Thread(target=audio_downloader)
            audio_download.start()
            t=0
            if not multi:
                p0=-1
                p1=-1
                while video_progress!=99 or audio_progress!=99:
                    if (p0!=video_progress or p1!=audio_progress) and t>=1:
                        p0=video_progress
                        p1=audio_progress
                        t=0
                    time.sleep(0.2)
                    t+=0.2
            else:
                p0=-1
                p1=-1
                while video_progress!=99 or audio_progress!=99:
                    if (p0!=video_progress or p1!=audio_progress) and t>=3:
                        p0=video_progress
                        p1=audio_progress
                        t=0
                    time.sleep(0.2)
                    t+=0.2


            time.sleep(0.1)
            while album_thread.is_alive() or video_info_thread.is_alive():
                time.sleep(0.1)
            time.sleep(0.1)

            #while try for anti unknow bug..
            while 1:
                try:
                    album_path='./file/'+self.ip+'/audio_tmp/'+file_title+'.jpg'
                    break
                except:
                    time.sleep(0.1)
            #
            
            f=open(album_path,'wb')
            f.write(album_request.content)
            f.close()
            file_title+='.mp4'
            cmd ='ffmpeg -y -i "'+video_fname+'" -i "'+album_path+'" -i "'+audio_fname+'" -q:a 2 -abr 1 -b:a '+final_abr.replace('bps','')+' -c copy '+(' -ss '+start_time+(' -to '+end_time if end_time!='-1' else '') if cut else '')+' -map 0 -map 1:0 -map 2 -metadata artist="'+video_info[0]+'" -metadata date="'+video_info[1]+'" -metadata genre="'+video_info[2]+'" -metadata comment="'+copyright_+'\tFull recorded date = '+video_info[3]+'" -disposition:v:1 attached_pic -preset ultrafast -strict experimental "'+'.\\file\\'+ip+'\\'+file_title+'" -threads 2'#-threads 2
            final=file_title
            cmd+=' -hide_banner -loglevel panic'
            os.system(cmd)
            #print(cmd)

            try:
                os.remove(video_fname)
            except:
                pass
            try:
                os.remove(audio_fname)
            except:
                pass
            try:
                os.remove(album_path)
            except:
                pass


        
        elif method=='2':
            backup_a=''
            audio=''
            for a in abrs:
                if len(streams.filter(type="audio",abr=a))>0:
                    audios=streams.filter(type="audio",abr=a)
                    for b in audios:
                        if b.audio_codec.count('opus')==0:
                            if backup_a=='':
                                final_abr=a
                                backup_a=b
                        else:
                            audio=b
                            final_abr=a
                            break
                if backup_a!='' or audio!='':
                    break
            if audio == '':
                audio = backup_a
            audio_download=Thread(target=audio_downloader)
            audio_download.start()


            
            t=0
            if not multi:
                p1=-1
                while audio_progress!=99:
                    if p1!=audio_progress and t>=1:
                        p1=audio_progress
                        t=0
                    time.sleep(0.2)
                    t+=0.2
            else:
                p1=-1
                while audio_progress!=99:
                    if p1!=audio_progress and t>=1.5:
                        p1=audio_progress
                        t=0
                    time.sleep(0.2)
                    t+=0.2



            
            time.sleep(0.1)
            while album_thread.is_alive() or video_info_thread.is_alive():
                time.sleep(0.1)
            time.sleep(0.1)

            #while try for anti unknow bug..
            while 1:
                try:
                    album_path='./file/'+self.ip+'/audio_tmp/'+file_title2+'.jpg'
                    break
                except:
                    time.sleep(0.1)
            #
            
            f=open(album_path,'wb')
            f.write(album_request.content)
            f.close()
            file_title2+='.mp3'
            alb_=alb
            if multi:
                rev=False
                for a in keywords:
                    if a in title.lower():
                        alb_=not alb_
                        break
            cmd ='ffmpeg -y -i "'+audio_fname+'"'+(' -i "'+album_path+'"' if alb_ else '')+' -q:a '+('3' if final_abr=="160kbps" else '4')+' -abr 1 -b:a '+final_abr.replace('bps','')+(' -ss '+start_time+(' -to '+end_time if end_time!='-1' else '') if cut else '')+(' -map 0 -map 1:0' if alb_ else '')+' -metadata:s:v title="Album cover" -metadata artist="'+video_info[0]+'" -metadata date="'+video_info[1]+'" -metadata genre="'+video_info[2]+'" -metadata "Full recorded date"='+video_info[3]+' -metadata composer="'+copyright_+'" -disposition:v:1 attached_pic -preset ultrafast "'+'.\\file\\'+ip+'\\'+file_title2+'" -threads 2'#-threads 1
            final=file_title2
            cmd+=' -hide_banner -loglevel panic'
            print(cmd)
            os.system(cmd)
            #try:
            #    os.remove(audio_fname)
            #except:
            #    pass
            #try:
            #    os.remove(album_path)
            #except:
            #    pass
        if not multi:
            self.path='./file/'+ip+'/'+final
        video_progress=100
        audio_progress=100

    def __analyze_single__(self,url):
        verified=False
        while 1:
            try:
                for a in range(3):
                    yt = YouTube(url)
                    if yt.title!='YouTube':
                        self.yt=yt
                        break
                if yt.title=='YouTube':
                    if not verified:
                        try:
                            title_req=requests.get('https://www.youtube.com/watch?v='+yt.video_id)
                            soup=bs4(title_req.content,'html.parser')
                            if soup.find(id='eow-title').get('title')=='YouTube':
                                self.yt=yt
                                break
                            else:
                                verified=True
                        except:
                            pass
                else:
                    break
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                if "<class 'urllib.error.URLError'>" in str(exc_type) or "<class 'KeyError'>" in str(exc_type) or 'Software caused connection abort' in str(exc_obj) or 'Temporary failure in name resolution' in str(exc_obj) or 'Remote end closed connection without response' in str(exc_obj) or 'IncompleteRead' in str(exc_obj) or "[WinError 10051] 通訊端操作嘗試連線到一個無法連線的網路。" in str(exc_obj):
                    time.sleep(2)
                else:
                    raise Exception("URL Error")
        streams=self.yt.streams.otf()
        res=['4320p','2160p','1440p','1080p','720p','480p','360p','240p','144p']
        for a in res.copy():
            if len(streams.filter(res=a))==0:
                res.remove(a)
        self.avaliable_res=res
        self.title=yt.title
        self.thumbnail_url=yt.thumbnail_url
        self.analyze_finish=True
    def __download_single__(self,method,select=None,cut=False,start_time='0',end_time='-1',alb=True):
        self.downloading={'mehtod':'single','format':('mp4' if method=='1' else 'mp3')}
        t=Thread(target=self.__core__,args=(self.yt,False,method,select,None,alb,self.ip))
        t.start()
        t.join()
        self.download_finish=True
    def __download_list__(self,method,select=None,higher=True,alb=True,keywords=[],downloader_num=1,urls=[]):
        download_tasks=[0 for a in range(downloader_num)]
        self.__downloading_title=[0 for a in range(downloader_num)]
        monitor_thread=Thread(target=self.__multi_downloader_progress_manager__,args=(len(urls),))
        monitor_thread.start()
        live=1
        count=0
        while live:
            for a in range(len(download_tasks)):
                if download_tasks[a]==0 or not download_tasks[a].is_alive():
                    if download_tasks[a]!=0:
                        self.__succ.append(self.__downloading_title[a])
                        self.file_path.append('.\\file\\'+self.ip+'\\'+self.__downloading_title[a]+'.'+('mp4' if method=='1' else 'mp3'))
                        download_tasks[a]=0
                        self.__downloading_title[a]=0
                    while 1:
                        if len(self.__analyze_list)>0:
                            if self.__analyze_list[0]!='end':
                                download_tasks[a]=mp.Process(target=self.__core__,args=(self.__analyze_list[0],True,method,select,higher,alb,self.ip,keywords))
                                download_tasks[a].start()
                                self.__downloading_title[a]=self.__analyze_list[0].title
                                self.__analyze_list.pop(0)
                                break
                            else:
                                live=0
                                break
                        else:
                            time.sleep(0.02)
                            break
                    if not live:
                        break
            time.sleep(0.5)
        fin=0
        while not fin:
            fin=1
            for a in range(len(download_tasks)):
                if download_tasks[a]!=0:
                    if not download_tasks[a].is_alive():
                        self.__succ.append(self.__downloading_title[a])
                        self.file_path.append('.\\file\\'+self.ip+'\\'+self.__downloading_title[a]+'.'+('mp4' if method=='1' else 'mp3'))
                        download_tasks[a]=0
                        self.__downloading_title[a]=0
                    else:
                        fin=0
            time.sleep(1)
        for a in range(len(self.__downloading_title)):
            if self.__downloading_title[a]!=0:
                self.__succ.append(self.__downloading_title[a])
                self.file_path.append('.\\file\\'+self.ip+'\\'+self.__downloading_title[a]+'.'+('mp4' if method=='1' else 'mp3'))
                self.__downloading_title[a]=0
        monitor_thread.join()
        self.download_finish=True
    def __multi_downloader_progress_manager__(self,url_len):
        succ_n=0
        fail_n=0
        self.downloading=[]
        downloading_title_=self.__downloading_title.copy()
        t=0
        os.system('cls')
        while 1:
            if (succ_n!=len(self.__succ) or fail_n!=len(self.__fail) or downloading_title_!=self.__downloading_title.copy()) and t>=2:
                succ_n=len(self.__succ)
                fail_n=len(self.__fail)
                downloading_title_=self.__downloading_title.copy()
                downloading_=[]
                left=url_len-succ_n-fail_n
                os.system('cls')
                for a in downloading_title_:
                    if a!=0:
                        downloading_.append(a)
                self.downloading=downloading_.copy()
                self.fail=self.__fail.copy()
                self.succ=self.__succ.copy()
                t=0
                if left==0:
                    break
            time.sleep(0.5)
            t+=0.5
    def __analyze_manager__(self,urls_):
        urls=urls_.copy()
        self.__analyze_list=[]
        analyze_tasks=[0 for a in range(3)]
        while len(urls)>0:
            while len(urls)>0 and len(self.__analyze_list)<15:
                for a in range(len(analyze_tasks)):
                    if analyze_tasks[a]==0 or not analyze_tasks[a].is_alive():
                        time.sleep(0.0001)
                        analyze_tasks[a]=Thread(target=self.__analyze__,args=(urls[0],))
                        analyze_tasks[a].start()
                        urls.pop(0)
                        break
            while len(urls)>0 and len(self.__analyze_list)>=10:
                #print('i"m done')
                time.sleep(0.5)
        fin=0
        while not fin:
            fin=1
            for a in analyze_tasks:
                if a!=0 and a.is_alive():
                    fin=0
            time.sleep(0.5)
        self.__analyze_list.append('end')
    def __analyze__(self,url):
        verified=False #verified title is not "YouTube"
        while 1:
            try:
                for a in range(3):
                    yt = YouTube(url)
                    if yt.title!='YouTube':
                        if yt.title in self.__title_anti_error:
                            self.__fail.append(url+'  (title repeat)')
                        else:
                            self.__analyze_list.append(yt)
                            self.__title_anti_error.append(yt.title)
                        break
                if yt.title=='YouTube':
                    if not verified:
                        try:
                            title_req=requests.get('https://www.youtube.com/watch?v='+yt.video_id)
                            soup=bs4(title_req.content,'html.parser')
                            if soup.find(id='eow-title').get('title')=='YouTube':
                                self.__analyze_list.append(yt)
                                self.__title_anti_error.append(yt.title)
                                break
                            else:
                                verified=True#keep retrying to get real title
                        except:
                            pass
                else:
                    break
            except:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                if "<class 'urllib.error.URLError'>" in str(exc_type) or "<class 'KeyError'>" in str(exc_type) or 'Software caused connection abort' in str(exc_obj) or 'Temporary failure in name resolution' in str(exc_obj) or 'Remote end closed connection without response' in str(exc_obj) or 'IncompleteRead' in str(exc_obj) or "[WinError 10051] 通訊端操作嘗試連線到一個無法連線的網路。" in str(exc_obj):
                    time.sleep(2)
                else:
                    f=open('error.txt','a+')
                    f.write(str(exc_type)+'\n\n'+str(exc_obj)+'\n\n\n')
                    f.close()
                    self.__fail.append(url)
                    break
    def __init__(self,ip='192.168.0.1'):
        self.download_finish=False
        self.audio_progress=0
        self.video_progress=0
        self.analyze_status=0
        self.list_finished=0
        self.finished_url=0
        self.downloading=None
        self.ip=ip.replace('.','_')
        try:
            os.makedirs('file/'+self.ip)
        except:
            pass
    def analyze(self,url):
        self.analyze_finish=False
        Thread(target=self.__analyze_single__,args=(url,)).start()
    def download_single(self,format_,res=None,cut=False,start_time='0',end_time='-1',alb=True):
        self.download_finish=False
        if format_=='mp4':
            method='1'
        elif format_=='mp3':
            method='2'
        Thread(target=self.__download_single__,args=(method,res,cut,start_time,end_time,alb)).start()
        time.sleep(0.1)

        
    def download_list(self,format_,res=None,higher=True,alb=True,keywords=[],downloader_num=1,yt_list=[]):
        self.download_finish=False
        if format_=='mp4':
            method='1'
        elif format_=='mp3':
            method='2'
        self.__analyze_list=[]
        self.__fail=[]
        self.__title_anti_error=[]
        self.__succ=[]
        self.fail=[]
        self.succ=[]
        self.downloading=[]
        self.file_path=[]
        yt_list_=yt_list.copy()
        id_list=[]
        for a in range(len(yt_list_)):
            url=yt_list_[a].split('&')[0]
            try:
                try:
                    id_=re.match('(.*)watch(.*)v=(.*)',url).group(3).split('&')[0]
                except:
                    id_=re.match('(.*)youtu.be/(.*)',url).group(2).split('&')[0]
                if id_list.count(id_)==0:
                    id_list.append(id_)
                else:
                    yt_list.remove(yt_list_[a])
            except:
                pass
        del yt_list_,id_list
        analyze_manager_thread=Thread(target=self.__analyze_manager__,args=(yt_list,))
        analyze_manager_thread.start()
        Thread(target=self.__download_list__,args=(method,res,higher,alb,keywords,downloader_num,yt_list)).start()

    def get_progress(self):
        if self.downloading:
            if self.downloading['mehtod']=='single':
                self.video_progress=video_progress
                self.audio_progress=audio_progress
                return ({'audio_progress':self.audio_progress,'video_progress':self.video_progress} if self.downloading['format']=='mp4' else {'audio_progress':self.audio_progress})
    def move2server(self,server_root_path):
        try:
            os.makedirs(os.path.join(server_root_path,'file/'+self.ip))
        except:
            pass
        self.server_root_path=os.path.join(server_root_path,'file/'+self.ip).replace('\\','/')
        p=os.path.join(server_root_path,self.path).replace('\\','/')
        shutil.move(self.path,p)
        return p
    def clear(self):
        try:
            shutil.rmtree(self.ip)
        except:
            pass
        try:
            shutil.rmtree(self.server_root_path)
        except:
            pass
