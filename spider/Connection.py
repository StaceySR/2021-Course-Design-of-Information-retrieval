import requests
from bs4 import BeautifulSoup as bs
import time


'''
爬取竞赛网站信息个性化分析参赛价值
'''


# 将通过url爬取网站的源代码封装成common_crawler()函数
def common_crawler(url, page):
    header = {
        'authority': "www.saikr.com",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.183 Safari/537.36",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
                  "application/signed-exchange;v=b3;q=0.9",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "navigate",
        'sec-fetch-user': "?1",
        'sec-fetch-dest': "document",
        'referer': "https://www.saikr.com/vs/mcm/0/0?page=5",
        'accept-language': "zh-CN,zh;q=0.9",
        'cookie': "_msg_lasttime=; MEIQIA_TRACK_ID=1dtTTk2xjtJkdPDcVXp0hHKMnqn; "
                  "hdmisaslm=f277abd14c4a12448a6f164e1cf4dfb4; Hm_lvt_f0ef5de4e57d9f0a06baad7f2e18ebb3=1605142647,"
                  "1605152740; sk_session=2b40a8c147c9ce42ef5431f72c90da112442eeec; "
                  "MEIQIA_VISIT_ID=1kAvvD7HKxZcOsDTdzI7ODUXOSc; Hm_lpvt_f0ef5de4e57d9f0a06baad7f2e18ebb3=1605156501",
        'postman-token': "cbaf4433-1ba4-2b79-2f0f-d2216180cc39"
    }
    querystring = {"page": page}

    # ----------Requests模块的异常值处理---------

    while True:  # 一直循环，直到访问站点成功
        try:
            # 以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            if page == -1:
                # 这个是用来爬取主页上的筛选框信息
                response = requests.request("GET", url, headers=header, stream=True)
            else:
                response = requests.request("GET", url, headers=header, params=querystring)
            break
        except requests.exceptions.ConnectionError:  # 网络连接异常
            print('ConnectionError -- please wait 3 seconds')
            time.sleep(3)
        except requests.exceptions.ChunkedEncodingError:
            # 下载文件的时候大多数都是Chunked编码
            print('ChunkedEncodingError -- please wait 3 seconds')
            time.sleep(3)
        except:
            print('Unfortunitely -- An Unknow Error Happened, Please wait 3 seconds')
            time.sleep(3)
            time.sleep(3)
    # ------------------------------------end-------------------

    html_data = response.text.encode(response.encoding)
    # 使用BeautifulCoup库进行HTML代码的解析。
    # 第一个参数为需要提取数据的html，第二个参数是指定解析器
    soup = bs(html_data, 'html.parser')
    return soup
