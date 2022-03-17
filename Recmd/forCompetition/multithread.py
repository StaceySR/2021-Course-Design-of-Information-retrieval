import threading
import time
import random

from spider import GetInfo
from spider.Connection import common_crawler
from spider.GetInfo import getInfo

type_id = {}


def pumpToDat(linkLists, titleLists, sponsorLists, levelLists, typeName, wholeType):
    # 首先知道每个Lists中包含有多少page的信息
    # 然后对于每个page中的信息一条一条写入
    # 设置两个循环
    global seen
    global id
    global f
    global urlLast
    global type_id
    start_id = id + 1
    print("typeName:", typeName, "startId:", start_id)
    for page in range(len(linkLists)):
        for i in range(len(linkLists[page]['linkList'])):
            id += 1
            string = str(id).zfill(4) + "::" + titleLists[page][i] + '::' + wholeType + '\t' + typeName + '\t' + sponsorLists[page][i] + "\t" + \
                     levelLists[page][i] + "\t" + linkLists[page]["typeList"][i] + "\t"
            if u'万' in linkLists[page]["viewList"][i]:
                linkLists[page]["viewList"][i] = linkLists[page]["viewList"][i].replace(u'万', '0000')
                string = string + linkLists[page]["viewList"][i] + '\t'
            else:
                string = string + linkLists[page]["viewList"][i] + '\t'
            if u'免' not in str(linkLists[page]["feeList"][i]):
                string = string + '\t' + '收费' + '\n'
            else:
                string = string + linkLists[page]["feeList"][i] + '\n'
            # if linkList[i] not in seen and string!=None:
            f.write(string)
    end_id = id
    type_id[typeName] = {"start_id": start_id, "end_id": end_id}
    print("typeName:", typeName, "endId:", end_id)


def crawl(url, typeName, wholeType):
    print(url)
    page = 0
    linkLists = {}
    titleLists = {}
    sponsorLists = {}
    levelLists = {}
    applicationTimeLists = {}
    competitionTimeLists = {}
    statusLists = {}
    while True:
        print(typeName, page)
        soup = common_crawler(url, page)
        linkList, titleList, sponsorList, levelList, applicationTimeList, competitionTimeList, statusList = getInfo(soup)
        if len(linkList) == 0:
            break
        titleLists[page] = titleList
        sponsorLists[page] = sponsorList
        levelLists[page] = levelList
        applicationTimeLists[page] = applicationTimeList
        competitionTimeLists[page] = competitionTimeList
        statusLists[page] = statusList
        viewList, typeList, feeList, priceList = GetInfo.getMore(linkList)
        linkContent = {"linkList": linkList, "viewList": viewList, "typeList": typeList, "feeList": feeList}
        linkLists[page] = linkContent
        page += 1
    # pumpToDat(linkLists, titleLists, sponsorLists, levelLists, typeName, wholeType)
    return linkLists, titleLists, sponsorLists, levelLists


g_num = 0


class myThread(threading.Thread):
    def __init__(self, urlLast, typeName, wholeType):
        threading.Thread.__init__(self)
        self.urlLast = urlLast
        self.typeName = typeName
        self.wholeType = wholeType

    def run(self):
        # global allInfo
        global g_num
        linkLists, titleLists, sponsorLists, levelLists = crawl(self.urlLast, self.typeName, self.wholeType)
        print(linkLists)
        pumpToDat(linkLists, titleLists, sponsorLists, levelLists, self.typeName, self.wholeType)
        print("in work1 g_num is : %d" % g_num)
        g_num += 1


def randomNum(a, b):
    return random.randint(a, b)


def write(string):
    global f_userInfo
    f_userInfo.write(string)


userIds = []


def generator(type_id):
    # 制造用户数据
    # 用户ID :: 竞赛ID :: 用户对于竞赛的评分
    # 既然是制造数据，那么就造的真一点
    # 1、每个用户至少7条记录；
    # 2、每个用户参加的竞赛中，至少有4条是同一类别的竞赛；
    # 3、对于同一类别的竞赛，评分在【3， 5】区间内
    # 4、对于不同类别的竞赛，评分在【0，3】区间内

    # type_id = {"数学建模": {"start_id": 100, "end_id": 988}, ....}
    keys = type_id.keys()
    for i in range(100000):
        # 生成100000个用户
        id = str(randomNum(0, 1000000))
        if id not in userIds:
            userIds.append(id)
            string = id.zfill(7)
            # 1、为该用户随机抽取一个竞赛类别curType：【0，len(type_id)】区间中取随机数
            curType = randomNum(0, len(type_id))
            # 2、为该用户确定总共有几条有效竞赛记录rightComNum:[4, 10]区间中取随机数
            rightComNum = randomNum(4, 10)
            # 3、为该用户确定总共有几条无效竞赛记录errorComNum：[0, 3]区间中取随机数
            errorComNum = randomNum(0, 3)
            compIds = []
            errorCompIds = []
            count1 = 0
            count2 = 0
            while count1 <= rightComNum:
                compId = randomNum(type_id[keys[curType]]['start_id'], type_id[keys[curType]['end_id']])
                if compId not in compIds:
                    curString = string + "::" + str(compId).zfill(4) + "::" + str(randomNum(3, 5))
                    write(curString + '\n')
                    count1 += 1

            while count2 < errorComNum:
                key = randomNum(0, len(keys))
                compId = randomNum(type_id[key]['start_id'], type_id[key]['end_id'])
                if compId not in errorCompIds and compId not in compIds:
                    curString = string + "::" + str(compId).zfill(4) + "::" + str(randomNum(0, 3))
                    write(curString + '\n')
                    count2 = errorComNum


if __name__ == '__main__':
    id = 0
    f = open("data/compdata.dat", 'a', encoding='utf-8')
    urlLastList = {"工科": {"数学建模": '/vs/mcm/', "程序设计": '/vs/acm/', "机器人": '/vs/robot/', "工程机械": '/vs/machine/',
                          "土木建筑": '/vs/building/',
                          "大数据": '/vs/big_data/', "交通车辆": '/vs/traffic/', "航空航天": '/vs/airplane/',
                          "船舶海洋": '/vs/ship_sea/',
                          "环境能源": '/vs/energy/', "计算机&信息技术": '/vs/computer/', "材料高分子": '/vs/material/',
                          "电子&自动化": '/vs/electronic/'},
                   '文体': {'工业&创意设计': '/vs/industry_design/', '外语': '/vs/english/', '演讲主持&辩论': '/vs/speech/',
                          '模特': '/vs/model/',
                          '歌舞书画&摄影': '/vs/song_and_dance/', '体育': '/vs/sports/', '科技文化艺术节': '/vs/technology/',
                          'UI设计': '/vs/ui_design/',
                          '服装设计': '/vs/fashion_design/', '电子竞技': '/vs/electronic_games/'},
                   '理科': {'数学': '/vs/match/', '物理': '/vs/physics/', '化学化工': '/vs/chemistry/', '健康生命&医学': '/vs/health/',
                          '力学': '/vs/mechanics/'},
                   '综合': {'职业技能': '/vs/occupation/', '挑战杯': '/vs/tiaozhanbei/', '环保公益': '/vs/environment/',
                          '社会综合': '/vs/society/',
                          '商科': '/vs/commerce/', '创业': '/vs/chuangye/', '商业': '/vs/business/',
                          '创青春': '/vs/chuangqingchun/'}}
    threadList = []
    for wholeType in urlLastList:
        for type in urlLastList[wholeType]:
            url = "https://www.saikr.com" + urlLastList[wholeType][type]
            t = myThread(urlLast=url, typeName=type, wholeType=wholeType)
            threadList.append(t)
    for thread in threadList:
        thread.start()
        time.sleep(1)

    # 爬取完竞赛信息之后开始制造用户数据，利用全局变量中记录的id值
    print(type_id)
    # 把这个type_id记录下来
    f_typeId = open('typeId.dat', 'a', encoding='utf-8')
    str_type_id = str(type_id)
    f_typeId.write(str_type_id)
    # --开始制造用户数据
    f_userInfo = open('user.dat', 'a', encoding='utf-8')
    generator(type_id)


