
from spider import GetInfo
from spider.Connection import common_crawler
from spider.GetInfo import getInfo
from spider.CreateUrl import connect_url
from spider.infoFormatter import formatter
from spider.DataWriter import save_to_excel
from spider.visualize import radar, every_level_ave_viewCount


def spider(soup_initial, type, level, order, scope, xlsx_name):
    """
    :param soup_initial:soup
    :param type: 用户输入的种类
    :param level: 用户输入的等级
    :param order: 用户输入的排序方式
    :param scope: 用户输入的页数
    :param xlsx_name: 写入的Excel名
    :return:  None
    """

    url = connect_url(soup_initial, type, level, order)
    all_info_list = []
    all_appliTime_list = []
    all_compTime_list = []

    all_view_list = []
    all_level_list = []
    for page in range(scope):
        soup = common_crawler(url, page)
        linkList, titleList, sponsorList, levelList, applicationTimeList, competitionTimeList, statusList = getInfo(
            soup)
        viewList, typeList, feeList, priceList = GetInfo.getMore(linkList)
        list = formatter(linkList, titleList, sponsorList, levelList, applicationTimeList, competitionTimeList,
                         statusList, viewList, typeList, feeList, priceList)

        if len(applicationTimeList) > 0:
            all_appliTime_list.append(applicationTimeList)
        if len(competitionTimeList) > 0:
            all_compTime_list.append(competitionTimeList)

        if len(viewList) > 0:
            all_view_list.append(viewList)
        if len(levelList) > 0:
            all_level_list.append(levelList)
        if len(list) > 0:
            all_info_list.append(list)

    """可视化"""
    # # 将比赛报名时间、比赛时间传到visualize中进行可视化
    radar(all_appliTime_list, all_compTime_list)
    # 将竞赛级别、浏览量传到visualize中进行可视化
    every_level_ave_viewCount(all_view_list, all_level_list)

    """数据写入"""
    save_to_excel(xlsx_name, all_info_list)
    print('信息保存完成！')
    # print(all_info_list)


