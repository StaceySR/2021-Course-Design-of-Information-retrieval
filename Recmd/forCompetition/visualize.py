import pygal


def similarUserPicCircle(similar_users, users_dict, comps_dict):
    my_config = pygal.Config()
    # 标题字体大小
    my_config.title_font_size = 50
    # 隐藏左上角的图例
    my_config.legend_at_bottom = True
    my_config.legend_at_bottom_columns = 9
    my_config.margin_bottom = 30
    gauge = pygal.SolidGauge(my_config, inner_radius=0.70)
    gauge.title = "相似用户群（9个最有可能的潜在竞赛队友）"
    # percent_formatter = lambda x: '{:.10g}%'.format(x)
    # dollar_formatter = lambda x: '{:.10g}$'.format(x)
    # gauge.value_formatter = percent_formatter

    max_value = 1
    for sim, user in similar_users:
        sim = sim
        # print(users_dict[user]['review'])
        # print("UserID: {} 相似度: {:.3}".format(user, sim))
        comps = [(comps_dict[i[0]]['compname'] + "  评分：{}".format(i[1])) for i in users_dict[user]['review'] if
                 i[0] in comps_dict]
        # print("comps:", comps)
        plot_dict = {
            'value': sim,
            # 有些描述很长很长，选最前一部分
            'max_value': max_value,
            'label': str(comps)[:50] + '...',
            # 'xlink': url_lists[compName]
        }

        gauge.add("user:" + user, [plot_dict])

    gauge.render_to_file('相似用户群（9个最有可能的潜在竞赛队友）.svg')


def similarUserPicZhu(similar_users):
    line_chart = pygal.Bar()
    line_chart.title = '相似用户群（30个潜在竞赛队友）'

    line_user_list = []
    line_sim_list = []
    for sim, user in similar_users:
        sim = sim
        line_user_list.append("user:" + user)
        line_sim_list.append(sim)

    line_chart.x_labels = map(str, line_user_list)
    line_chart.add('相似度', line_sim_list)

    line_chart.render_to_file('相似用户群（30个潜在竞赛队友）.svg')


