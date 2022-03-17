def create_url(soup):
    """构建美味汤"""
    # soup = BeautifulSoup(response.text, 'lxml')

    """构建url"""
    soups_item_all = soup.find(name="div", attrs={"class": "item-box"})
    # 还要去下面遍历获取a标签
    a = soups_item_all.findAllNext(name="a", attrs={"class": "item-link"})
    level_count = []
    the_last_level = 0
    comp_type = {}
    comp_level = {}
    comp_range = {}
    for i in range(0, len(a) - 1):
        if a[i]['href'][-3] != '0':
            the_last_level = i
            level_count.append(i)
    # print("\n------------------竞赛类别的url----------------------------")
    for i in range(0, level_count[0] - 1):  # 竞赛类别
        comp_type[a[i].string] = a[i]["href"][0: -3]

    # print("\n------------------竞赛级别的url----------------------------")
    for i in range(level_count[0] - 1, level_count[-1] + 1):  # 竞赛级别
        comp_level[a[i].string] = a[i]["href"][8]

    index_count = the_last_level + 1  # 排序方式从这开始才是
    # print("\n------------------排序方式的url----------------------------")
    for i in range(index_count, len(a) - 1):  # 排序方式
        comp_range[a[i].string] = a[i]["href"][10]

    return comp_type, comp_level, comp_range


def connect_url(soup, type, level, range):
    """
    根据type，level，range拼接
    :param soup: soup
    :param type: 种类
    :param level: 等级
    :param range: 页数
    :return:
    """
    initial_url = "https://www.saikr.com"
    # 然后就要通过传入的参数来拼接获得最终需要爬取的url
    comp_type, comp_level, comp_range = create_url(soup)
    url = initial_url + comp_type[type] + comp_level[level] + "/" + comp_range[range]
    # print(type, level, range, url)
    return url
