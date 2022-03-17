import re
from spider.Connection import common_crawler


def getInfo(soup):
    """
    :param response:
    :return:  Inorder：Tuple (linkList,titleList,sponsorList,levelList,applicationTimeList,competitionTimeList,statusList,flag)
        flag 为True说明该页信息有效

        getInfo BY PAGE
        比赛信息链接
        比赛名字
        主办方
        竞赛级别
        报名时间
        比赛时间
        比赛报名状态
    """

    """构建美味汤"""
    soups_li = soup.findAll(name="li", attrs={"class": "item clearfix"})  # 装着每个比赛的soup

    """提取内容的正则表达式"""
    pattern = r'</span>(.*?)</p>'

    """初始化存放信息的List"""
    linkList = []  # 比赛信息链接
    titleList = []  # 比赛名字
    sponsorList = []  # 主办方
    levelList = []  # 竞赛级别
    applicationTimeList = []  # 报名时间
    competitionTimeList = []  # 比赛时间
    statusList = []  # 比赛报名状态

    """循环体"""
    for i in range(len(soups_li)):
        # 竞赛url链接
        link = soups_li[i].findAll(name="a", attrs={"class": "link"})[0]['href']
        # 竞赛标题
        title = soups_li[i].findAll(name="a", attrs={"class": "link"})[0]['title']
        # 报名状态：正在报名、报名结束
        status = soups_li[i].findAll(name="em", attrs={"class": "event-status-tip"})[0].string.strip()
        # 竞赛信息
        info = soups_li[i].findAll(name="p", attrs={"class": "event4-1-plan"})
        """
        info[0]:主办方
        info[1]:竞赛级别
        info[2]:报名时间
        info[3]:比赛时间
        """
        sponsor = re.search(pattern, str(info[0])).group(1)
        level = re.search(pattern, str(info[1])).group(1)
        if level.startswith(u"国际"):
            # level = 5
            level = "国际级"
        elif level.startswith(u"国家"):
            # level = 4
            level = "国家级"
        elif level.startswith(u"省"):
            # level = 3
            level = "省级"
        elif level.startswith(u"市"):
            # level = 2
            level = "市级"
        elif level.startswith(u"校"):
            # level = 1
            level = "校级"
        else:
            # level = 0
            level = "自由"
        # 0、自由  1、校级 2、市级 3、省级 4、国家级 5、国际级
        applicationTime = re.search(pattern, str(info[2])).group(1)
        competitionTime = re.search(pattern, str(info[3]), re.S).group(1).replace(' ', "").strip()

        # 需要进行NoneType检测

        """构建List，准备写入"""
        linkList.append(link)
        titleList.append(title)
        sponsorList.append(sponsor)
        levelList.append(level)
        applicationTimeList.append(applicationTime)
        competitionTimeList.append(competitionTime)
        statusList.append(status)

    return linkList, titleList, sponsorList, levelList, applicationTimeList, competitionTimeList, statusList


def getMore(linkList):
    """
    :param linkList: 具体链接
    :return:奖金，比赛种类，浏览量，费用
    """
    viewList = []
    typeList = []
    feeList = []
    priceList = []
    for link in linkList:
        soup = common_crawler(link, -1)
        information = soup.findAll("span", {"class": "title-desc"})
        '''
        改-----------将None全部改成‘None’，不然到时候在拼接的时候会出错---------------------------------------------------------
        '''
        if information:
            viewCount = information[0].string if information[0].string is not None else 'None'
            type = information[1].string if information[1].string is not None else 'None'
            fee = information[2].string if information[2].string is not None else 'None'
            viewList.append(viewCount)
            typeList.append(type)
            feeList.append(fee)
        else:
            viewList.append('None')
            typeList.append('None')
            feeList.append('None')

        divPrice = soup.find("div", {"class": "info-content clearfix"})
        if divPrice:
            prices = divPrice.findAll("span", {"class": "fl item-prize"})
            s = ""
            for price in prices:
                if u"奖" in str(price.string) or u"牌" in str(price.string):
                    s = s + price.string + "    "
            priceList.append(s)
        else:
            priceList.append('None')
        '''
        -----------------------------------------------------------------
        '''

    return viewList, typeList, feeList, priceList


if __name__ == '__main__':
    list = ['https://www.saikr.com/vse/jsai-smartcar', 'https://www.saikr.com/vse/39768',
            'https://www.saikr.com/vse/2020chuangyezhixin', 'https://www.saikr.com/vse/39769',
            'https://www.saikr.com/vse/39743', 'https://www.saikr.com/vse/38036', 'https://www.saikr.com/vse/37978',
            'https://www.saikr.com/vse/39767', 'https://www.saikr.com/vse/39632', 'https://www.saikr.com/vse/39659']
    getMore(list)
