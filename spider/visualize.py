# -----------------------------玫瑰图-----------------------------------------
'''
    竞赛级别和平均浏览量的关系_玫瑰图
    竞赛级别与平均浏览量之间的关系，观察是否是竞赛级别越高，平均浏览量越高。
    可以分析出。。。。。。
'''


# 1、级别 --- 平均浏览量（标出浏览量最大的那个竞赛）
def every_level_ave_viewCount(all_view_list, all_level_list):
    guoji_view = {"count": 0, "all_view_count": 0}
    guojia_view = {"count": 0, "all_view_count": 0}
    sheng_view = {"count": 0, "all_view_count": 0}
    shi_view = {"count": 0, "all_view_count": 0}
    xiao_view = {"count": 0, "all_view_count": 0}
    free_view = {"count": 0, "all_view_count": 0}

    max_guoji = 0
    max_guojia = 0
    max_sheng = 0
    max_shi = 0
    max_xiao = 0
    max_free = 0

    for i in range(len(all_level_list)):
        for j in range(len(all_level_list[i])):
            if all_level_list[i][j] == "国际级":
                guoji_view["count"] += 1
                if u"万" in all_view_list[i][j]:
                    all_view_list[i][j] = all_view_list[i][j][:-1] + "0000"
                all_view_list[i][j] = int(all_view_list[i][j])
                guoji_view["all_view_count"] += all_view_list[i][j]
                if all_view_list[i][j] > max_guoji:
                    max_guoji = all_view_list[i][j]
            if all_level_list[i][j] == "国家级":
                guojia_view["count"] += 1
                if u"万" in all_view_list[i][j]:
                    all_view_list[i][j] = all_view_list[i][j][:-1] + "0000"
                all_view_list[i][j] = int(all_view_list[i][j])
                guojia_view["all_view_count"] += all_view_list[i][j]

                if all_view_list[i][j] > max_guojia:
                    max_guojia = all_view_list[i][j]
            if all_level_list[i][j] == "省级":
                sheng_view["count"] += 1
                if u"万" in all_view_list[i][j]:
                    all_view_list[i][j] = all_view_list[i][j][:-1] + "0000"
                all_view_list[i][j] = int(all_view_list[i][j])
                sheng_view["all_view_count"] += all_view_list[i][j]
                if all_view_list[i][j] > max_sheng:
                    max_sheng = all_view_list[i][j]
            if all_level_list[i][j] == "市级":
                shi_view["count"] += 1
                if u"万" in all_view_list[i][j]:
                    all_view_list[i][j] = all_view_list[i][j][:-1] + "0000"
                all_view_list[i][j] = int(all_view_list[i][j])
                shi_view["all_view_count"] += all_view_list[i][j]
                if all_view_list[i][j] > max_shi:
                    max_shi = all_view_list[i][j]
            if all_level_list[i][j] == "校级":
                xiao_view["count"] += 1
                if u"万" in all_view_list[i][j]:
                    all_view_list[i][j] = all_view_list[i][j][:-1] + "0000"
                all_view_list[i][j] = int(all_view_list[i][j])
                xiao_view["all_view_count"] += all_view_list[i][j]
                if all_view_list[i][j] > max_xiao:
                    max_xiao = all_view_list[i][j]
            if all_level_list[i][j] == "自由":
                free_view["count"] += 1
                if u"万" in all_view_list[i][j]:
                    all_view_list[i][j] = all_view_list[i][j][:-1] + "0000"
                all_view_list[i][j] = int(all_view_list[i][j])
                free_view["all_view_count"] += all_view_list[i][j]
                if all_view_list[i][j] > max_free:
                    max_free = all_view_list[i][j]
    if guoji_view["count"] == 0:
        guoji_view["ave_view_count"] = 0
    else:
        guoji_view["ave_view_count"] = int(guoji_view["all_view_count"] / guoji_view["count"])
    if guojia_view["count"] == 0:
        guojia_view["ave_view_count"] = 0
    else:
        guojia_view["ave_view_count"] = int(guojia_view["all_view_count"] / guojia_view["count"])
    if sheng_view["count"] == 0:
        sheng_view["ave_view_count"] = 0
    else:
        sheng_view["ave_view_count"] = int(sheng_view["all_view_count"] / sheng_view["count"])
    if shi_view["count"] == 0:
        shi_view["ave_view_count"] = 0
    else:
        shi_view["ave_view_count"] = int(shi_view["all_view_count"] / shi_view["count"])
    if xiao_view["count"] == 0:
        xiao_view["ave_view_count"] = 0
    else:
        xiao_view["ave_view_count"] = int(xiao_view["all_view_count"] / xiao_view["count"])
    if free_view["count"] == 0:
        free_view["ave_view_count"] = 0
    else:
        free_view["ave_view_count"] = int(free_view["all_view_count"] / free_view["count"])

    from pyecharts.charts import Pie
    from pyecharts import options as opts
    import random

    # 随机颜色生成
    def randomcolor(kind):
        colors = []
        for i in range(kind):
            colArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
            color = ""
            for i in range(6):
                color += colArr[random.randint(0, 14)]
            colors.append("#" + color)
        return colors

    # 数据
    x_data = ["国际级", "国家级", "省级", "市级", "校级", "自由"]
    y_data = [guoji_view["ave_view_count"], guojia_view["ave_view_count"], sheng_view["ave_view_count"],
              shi_view["ave_view_count"], xiao_view["ave_view_count"], free_view["ave_view_count"]]
    max_data = [max_guoji, max_guojia, max_sheng, max_shi, max_xiao, max_free]
    color_series = randomcolor(len(x_data))

    # 创建饼图
    fig = Pie(init_opts=opts.InitOpts(width='1500px', height='1000px'))
    # 添加数据
    fig.add("", [list(z) for z in zip(x_data, y_data)],
            radius=['30%', '135%'],
            center=['50%', '65%'],
            rosetype='area')
    # 设置全局配置
    fig.set_global_opts(title_opts=opts.TitleOpts(title='竞赛级别vs平均浏览量_玫瑰图'),
                        legend_opts=opts.LegendOpts(is_show=False)
                        )

    # 设置系列配置和颜色
    fig.set_series_opts(label_opts=opts.LabelOpts(is_show=True, position='inside', font_size=12,
                                                  formatter='{b}:{c}次', font_style='italic', font_weight='bold',
                                                  font_family='Microsoft YaHei'))  # b:province;c:num
    fig.set_colors(color_series)

    fig.render('竞赛级别和平均浏览量的关系_玫瑰图.html')

# -----------------------------柱形图-----------------------------------------
    '''
    竞赛级别和平均浏览量的关系_柱形图
    竞赛级别与平均浏览量之间的关系，观察是否是竞赛级别越高，平均浏览量越高。
    同时我们还展示了每个竞赛级别的竞赛的最高浏览量。
    可以分析出。。。。。。
    '''
    from pyecharts.charts import Bar
    from pyecharts.globals import ThemeType, CurrentConfig
    from pyecharts import options as opts

    #
    # CurrentConfig.ONLINE_HOST = 'D:/python/pyecharts-assets-master/assets/'
    # 数据
    x_data = ["国际级", "国家级", "省级", "市级", "校级", "自由"]
    y_data = [guoji_view["ave_view_count"], guojia_view["ave_view_count"], sheng_view["ave_view_count"],
              shi_view["ave_view_count"], xiao_view["ave_view_count"], free_view["ave_view_count"]]
    max_data = [max_guoji, max_guojia, max_sheng, max_shi, max_xiao, max_free]
    # 链式调用
    c = (
        Bar(
            init_opts=opts.InitOpts(           # 初始配置项
                theme=ThemeType.MACARONS,
                width='1500px',
                height='600px',
                animation_opts=opts.AnimationOpts(
                    animation_delay=1000, animation_easing="cubicOut"   # 初始动画延迟和缓动效果
                ))
            )
        .add_xaxis(xaxis_data=x_data)      # x轴
        .add_yaxis(series_name="最大浏览量", yaxis_data=max_data)       # y轴
        .add_yaxis(series_name="平均浏览量", yaxis_data=y_data)       # y轴
        .set_global_opts(
            title_opts=opts.TitleOpts(title='竞赛级别vs平均浏览量_柱形图',   # 标题配置和调整位置
                                      title_textstyle_opts=opts.TextStyleOpts(
                                      font_family='SimHei', font_size=25, font_weight='bold', color='red',
                                      ), pos_left="90%", pos_top="10",
                                      ),
            xaxis_opts=opts.AxisOpts(name='竞赛级别', axislabel_opts=opts.LabelOpts(rotate=45)),  # 设置x名称和Label rotate解决标签名字过长使用
            yaxis_opts=opts.AxisOpts(name='浏览量'),

        )
        .render("竞赛级别和平均浏览量的关系_柱形图.html")
    )

# -----------------------------雷达图-----------------------------------------
    '''
    竞赛时间（月分）分布——雷达图
    竞赛在12个月中的分布，分析发现，xxx月聚集了很多竞赛的报名时间。。。。
    '''
# 4、竞赛时间（月分）分布。
from pyecharts import options as opts  # 用以设置
from pyecharts.charts import Radar  # 导入雷达类


def radar(all_appliTime_list, all_compTime_list):  # 定义绘图函数
    # 拿到数据首先要对数据进行处理，因为每个时间数据都是2020.11.26～2020.11.30，但是只需要提取出其中的月分即可。
    start_signup_time = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0,
                         "11": 0, "12": 0}
    end_signup_time = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0,
                       "11": 0, "12": 0}
    for alist in all_appliTime_list:
        for item in alist:
            # print(item)
            # print(item[5:7])
            start = item[5:7]
            finish = item[-5:-3]
            start_signup_time[start] += 1
            end_signup_time[start] += 1
            # print("---------start, finish", start, finish)

    start_time = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0,
                  "12": 0}
    end_time = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0,
                "12": 0}
    for i in range(len(all_compTime_list)):
        for j in range(len(all_compTime_list[i])):
            if all_compTime_list[i][j] != "比赛时间待定":
                start = all_compTime_list[i][j][5:7]
                finish = all_compTime_list[i][j][-5:-3]
                start_time[start] += 1
                end_time[start] += 1
                # print("---------start, finish", start, finish)
            else:
                start = all_appliTime_list[i][j][5:7]
                finish = all_appliTime_list[i][j][-5:-3]
                start_time[start] += 1
                end_time[start] += 1
                # print("---------start, finish", start, finish)

    # print(list(start_signup_time.values()))
    # print(end_signup_time.values())
    # print(start_time.values())
    # print(end_time.values())

    max = 10
    c_schema = [
        opts.RadarIndicatorItem(name='一月', max_=max),  # 设置指示器名称和最大值
        opts.RadarIndicatorItem(name='二月', max_=max),
        opts.RadarIndicatorItem(name='三月', max_=max),
        opts.RadarIndicatorItem(name='四月', max_=max),
        opts.RadarIndicatorItem(name='五月', max_=max),
        opts.RadarIndicatorItem(name='六月', max_=max),
        opts.RadarIndicatorItem(name='七月', max_=max),
        opts.RadarIndicatorItem(name='八月', max_=max),
        opts.RadarIndicatorItem(name='九月', max_=max),
        opts.RadarIndicatorItem(name='十月', max_=max),
        opts.RadarIndicatorItem(name='十一月', max_=max),
        opts.RadarIndicatorItem(name='十二月', max_=max)
    ]
    radar = Radar()  # 初始化对象,单独调用
    radar.add("竞赛报名开始时间", [list(start_signup_time.values())], color="#f9713c",
              linestyle_opts=opts.LineStyleOpts(width=3))  # 添加第一类数据并绘图
    radar.add("竞赛报名结束时间", [list(end_signup_time.values())], color="#4169E1")  # 添加第二类数据并绘图
    radar.add("竞赛进行开始时间", [list(start_time.values())], color="#00BFFF",
              linestyle_opts=opts.LineStyleOpts(width=3))  # 添加第一类数据并绘图
    radar.add("竞赛进行结束时间", [list(end_time.values())], color="#3CB371")  # 添加第二类数据并绘图
    radar.add_schema(schema=c_schema, shape="polygon")  # schema设置
    radar.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 是否打标签
    radar.set_global_opts(title_opts=opts.TitleOpts(title="竞赛时间分析_雷达图"))  # 标题
    return radar.render("竞赛时间分析_雷达图.html")  # 渲染成html格式
