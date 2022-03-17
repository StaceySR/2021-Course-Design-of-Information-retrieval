# TODO:将数据写入Df，数据分析
import xlsxwriter


def save_to_excel(xlsx_name, all_info_list):
    xlsx_name = xlsx_name + ".xlsx"
    workbook = xlsxwriter.Workbook(xlsx_name)
    worksheet = workbook.add_worksheet("0")

    # 设置列宽（起始列，结束列，宽度）
    worksheet.set_column(0, 0, 8)
    worksheet.set_column(1, 1, 77)
    worksheet.set_column(2, 2, 55)
    worksheet.set_column(3, 3, 158)
    worksheet.set_column(4, 4, 12)
    worksheet.set_column(5, 6, 30)
    worksheet.set_column(7, 10, 15)
    worksheet.set_column(11, 11, 55)

    # 第0行标题单元格格式
    title_style = workbook.add_format({
        "bold": True,
        'font_name': '仿宋',
        'font_size': 14,
        'font_color': 'red',
        "align": 'center',
        "valign": 'vcenter',
        'text_wrap': 1
    })
    # 其余行单元格格式
    style = workbook.add_format({
        "align": 'center',
        "valign": 'vcenter',
        "font_size": 10,
        'font_name': '黑体'
    })

    # 第0行设置各列名称
    worksheet.write(0, 1, 'title', title_style)
    worksheet.write(0, 2, 'link', title_style)
    worksheet.write(0, 3, 'sponsor', title_style)
    worksheet.write(0, 4, 'level', title_style)
    worksheet.write(0, 5, 'applicationTime', title_style)
    worksheet.write(0, 6, 'competitionTime', title_style)
    worksheet.write(0, 7, 'status', title_style)
    worksheet.write(0, 8, 'viewCount', title_style)
    worksheet.write(0, 9, 'type', title_style)
    worksheet.write(0, 10, 'fee', title_style)
    worksheet.write(0, 11, 'award', title_style)

    count = 1  # 控制现在写入的是第几行
    index = 1  # 标记序号，是第几个老师
    for list in all_info_list:
        for item in list:
            title = item['title']
            link = item['link']
            sponsor = item['sponsor']
            level = item['level']
            applicationTime = item['applicationTime']
            competitionTime = item['competitionTime']
            status = item['status']
            viewCount = item['viewCount']
            type = item['type']
            fee = item['fee']
            award = item['award']

            # 写入
            worksheet.write(count, 0, index, style)
            worksheet.write(count, 1, title, style)
            worksheet.write(count, 2, link, style)
            worksheet.write(count, 3, sponsor, style)
            worksheet.write(count, 4, level, style)
            worksheet.write(count, 5, applicationTime, style)
            worksheet.write(count, 6, competitionTime, style)
            worksheet.write(count, 7, status, style)
            worksheet.write(count, 8, viewCount, style)
            worksheet.write(count, 9, type, style)
            worksheet.write(count, 10, fee, style)
            worksheet.write(count, 11, award, style)

            count += 1
            index += 1
    workbook.close()
