import urllib.request,time
from django.shortcuts import render
import Main.yt_download_new_superspeed_api as yt_api
from django.http import HttpResponse, Http404
import os
from django.conf import settings

def index(request):
    global URL
    return render(request,'index.html',locals())
def fbl():
    import sys,time
    exc_type, exc_obj, exc_tb = sys.exc_info()
    error_inf='error type:  '+str(exc_type)+'\nerror obj:" '+str(exc_obj)+' "\nerror in line:" '+str(exc_tb.tb_lineno)+' "'
    return error_inf

def gitList(request):
    if request.method == 'POST':
        print('IP from '+ str(request.META['REMOTE_ADDR']))
        URL = request.POST['url']
        print(URL)
        try:
            if request.POST['url'] == '':
                return render(request,'index.html',locals())
            user = yt_api.Downloader(request.META['REMOTE_ADDR']) #建立user物件
            user.analyze(request.POST['url'])#分析單個url
            print(request.POST['choices-single-defaul'])
            while not user.analyze_finish:
                print('analyzing URL which requested from '+str(request.META['REMOTE_ADDR']))
                time.sleep(1)
            user.download_single(format_='mp4',res=str(request.POST['choices-single-defaul']))
            while not user.download_finish:
                print('downloading video which requested from '+ str(request.META['REMOTE_ADDR']))
                time.sleep(1)
            print(user.path)
            ipaddr = request.META['REMOTE_ADDR'].split('.')
            _dir= str(ipaddr[0]+"_"+ipaddr[1]+"_"+ipaddr[2]+"_"+ipaddr[3])
            print("已經存入 "+_dir)
            # user.download_single(format_='mp4',res=str(request.POST['choices-single-defaul']))
            file_path = str(settings.MEDIA_ROOT[0])+'\\'+ user.path.replace('/','\\')
            print(file_path)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response #下載
            raise Http404
            # return render(request,'list.html',locals())
        except :
            print(fbl())
            user.clear()
            return render(request,'index.html',locals())

def Error(request,path):
    ipaddr = request.META['REMOTE_ADDR'].spilt('.')
    _dir= str(ipaddr[0]+"_"+ipaddr[1]+"_"+ipaddr[2]+"_"+ipaddr[3])
    file_path = os.path.join(settings.MEDIA_ROOT, _dir)
    print(file_path)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    raise Http404

def loading (request):
    return render(request,'loading.html',locals())

            
        
        
            
