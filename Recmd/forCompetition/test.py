import pygal
from pygal.style import LightColorizedStyle, LightenStyle

# 需要自己先构造一个推荐结果的url——lists（这里应该再竞赛数据集中进行改进的，但是这次来不及了）
url_lists = {"2019年东北三省大学生数学建模联赛—哈尔滨商业大学校内报名专用": "https://www.saikr.com/vse/huc2019jmss",
             "2014年广州地区六校数学建模联赛": "https://www.saikr.com/gdmec/mcm",
             "2017年沈阳工业大学数学建模校赛暨东北三省数学建模联赛报名通知": "https://www.saikr.com/vse/34645",
             "山东理工大学2018年第八届MathorCup高校数学建模挑战赛": "https://www.saikr.com/vse/35570",
             "第十届华中地区大学生数学建模邀请赛——精英挑战赛": "https://www.saikr.com/vse/jyhuazhongliansai/2017",
             "宁夏第五届大学生数学建模竞赛暨全国选拔赛": "https://www.saikr.com/vse/35645",
             "2019年第九届APMCM亚太地区大学生数学建模竞赛(塔里木大学报名处）": "https://www.saikr.com/vse/37396",
             "2015年第七届北京理工大学数学建模与计算机应用竞赛": "https://www.saikr.com/bit/mcm",
             "2014年四川财经职业学院 第一届“挑战杯”数学建模竞赛报名官网": "https://www.saikr.com/scpcfe/tzb",
             "2017年巢湖学院校内数学建模竞赛暨统计建模竞赛": "https://www.saikr.com/chtc/shumo",
             "中南大学2020年数学建模竞赛校内赛": "https://www.saikr.com/vse/csu/shumo/2020",
             "2018年西南交通大学“新秀杯”数学建模竞赛": "https://www.saikr.com/vse/36417",
             "中国矿业大学第一届“科技杯”数学建模大赛": "https://www.saikr.com/cumt/kejibei",
             "第十一届华中地区大学生数学建模邀请赛": "https://www.saikr.com/vse/35651",
             "2015年第四届数学中国数学建模国际赛": "https://www.saikr.com/camcm",
             "2014年山西省大学生数学建模竞赛暨深圳杯选拔赛": "https://www.saikr.com/tymcm",
             "第十三届塔里木大学数学建模竞赛暨2020国赛拔赛": "https://www.saikr.com/vse/37859",
             "2015交叉学科数学建模学生论坛SFIMM2015": "https://www.saikr.com/sfimm2015",
             "“我爱建模”里仁学院大学生数学建模竞赛暨2017年全国大学生数学建模竞赛选拔赛": "https://www.saikr.com/vse/liren/jianmo/2017",
             "2018山东科技大学大学生数学建模竞赛": "https://www.saikr.com/vse/35704",
             "2015年山东省大学生科技节": "https://www.saikr.com/sdast",
             "2018年APMCM亚太地区大学生数学建模竞赛": "https://www.saikr.com/vse/36455",
             "2014年首届“智慧海洋杯”京津地区高校数学建模竞赛": "https://www.saikr.com/wisdomocean",
             "2014年东北大学第十二届大学生数学建模竞赛": "https://www.saikr.com/neu/mcm",
             "2016青岛高校数学建模联赛": "https://www.saikr.com/tsingtaoMCM/2016",
             "2019第十五届芜湖高校数学建模联赛": "https://www.saikr.com/vse/36970",
             "2015年东北三省数学建模联赛": "https://www.saikr.com/ldxy",
             "UI设计大赛": "https://www.saikr.com/caijingwen",
             "江苏省第五届数学建模竞赛": "https://www.saikr.com/nnutc/math",
             "宁夏第七届大学生数学建模竞赛暨全国选拔赛": "https://www.saikr.com/vse/nxmcm2020"
             }


def manySimilarCompsPic(recommend_comps, comps_dict):
    names, plot_dicts = [], []
    for compid, val in recommend_comps:
        item = comps_dict[compid]
        compName = item['compname']
        names.append(compName)
        plot_dict = {
            'value': val,
            # 有些描述很长很长，选最前一部分
            # 'label': str(item['tags'])[:200] + '...',
            'label': str(item['tags']),
            'xlink': url_lists[compName]
        }
        plot_dicts.append(plot_dict)

    # 改变默认主题颜色，偏蓝色
    my_style = LightenStyle('#333366', base_style=LightColorizedStyle)
    # 配置
    my_config = pygal.Config()
    # x轴的文字旋转45度
    my_config.x_label_rotation = -45
    # 隐藏左上角的图例
    my_config.show_legend = False
    # 标题字体大小
    my_config.title_font_size = 30
    # 副标签，包括x轴和y轴大部分
    my_config.label_font_size = 20
    # 主标签是y轴某数倍数，相当于一个特殊的刻度，让关键数据点更醒目
    my_config.major_label_font_size = 24
    # 限制字符为15个，超出的以...显示
    my_config.truncate_label = 6
    # 不显示y参考虚线
    my_config.show_y_guides = False
    # 图表宽度
    my_config.width = 1000

    # 第一个参数可以传配置
    chart = pygal.Bar(my_config, style=my_style)
    chart.title = '竞赛推荐TOP30'
    # x轴的数据
    chart.x_labels = names
    # 加入y轴的数据，无需title设置为空，注意这里传入的字典，
    # 其中的键--value也就是y轴的坐标值了
    chart.add('', plot_dicts)
    chart.render_to_file('竞赛推荐TOP30.svg')
