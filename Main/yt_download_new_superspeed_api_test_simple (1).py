import yt_download_new_superspeed_api as yt_api
import time

#__name__ == '__main__'很重要，本api有使用multiprocessing，不使用會出錯
if __name__ == '__main__':
    user=yt_api.Downloader('192.168.0.1')

    user.analyze('https://www.youtube.com/watch?v=cTlshvPrIZo')#分析單個url
    while not user.analyze_finish:
        print('nfin')
        time.sleep(1)
    print('fin')
    print()
    print(user.title)#影片title
    print(user.thumbnail_url)#影片專輯封面
    print()
    format_=input('\n\n1.mp4\n2.mp3\n\nplease select:')
    if format_=='1':#下載mp4
        print()
        print(user.avaliable_res)
        resolution=input('請從之以上可用畫質中選擇一個:')
        print()


        
        #start_time、end_time可不輸入即不剪輯
        user.download_single(format_='mp4',res=resolution)



        while not user.download_finish:
            p=user.get_progress()
            print(p)
            time.sleep(1)
        print(p)
        print()
        print(user.path)
        path=input('\n\nmove to path: ')
        file_path=user.move2server(path)
        print('\n\nfinal file path:',file_path)
        input('\n\nfinish.\n輸入以清除使用者資料:')
        user.clear()
    elif format_=='2':#下載mp3
        print()
        print('1.with album art(專輯封面)')
        print('2.no album art(專輯封面)')
        if input('please select:') == '1':
            alb=True
        else:
            alb=False
        print()



        #start_time、end_time可不輸入即不剪輯
        user.download_single(format_='mp3')



        while not user.download_finish:
            p=user.get_progress()
            print(p)
            time.sleep(1)
        print(p)
        path=input('\n\nmove to path: ')
        file_path=user.move2server(path)
        print('\n\nfinal file path:',file_path)
        input('\n\nfinish.\n輸入以清除使用者資料:')
        user.clear()
