import json
import random


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
    keys = list(keys)
    for i in range(100000):
        # 生成100000个用户
        id = str(randomNum(0, 1000000))
        if id not in userIds:
            userIds.append(id)
            string = id.zfill(7)
            # 1、为该用户随机抽取一个竞赛类别curType：【0，len(type_id)】区间中取随机数
            curType = randomNum(0, len(type_id)-1)
            # 2、为该用户确定总共有几条有效竞赛记录rightComNum:[4, 10]区间中取随机数
            rightComNum = randomNum(4, 10)
            # 3、为该用户确定总共有几条无效竞赛记录errorComNum：[0, 3]区间中取随机数
            errorComNum = randomNum(0, 3)
            compIds = []
            errorCompIds = []
            count1 = 0
            count2 = 0
            while count1 <= rightComNum:
                compId = randomNum(int(type_id[keys[curType]]['start_id']), int(type_id[keys[curType]]['end_id']))
                if compId not in compIds:
                    curString = string + "::" + str(compId).zfill(4) + "::" + str(randomNum(3, 5))
                    write(curString + '\n')
                    count1 += 1

            while count2 < errorComNum:
                n = randomNum(0, len(keys)-1)
                key = keys[n]
                compId = randomNum(int(type_id[key]['start_id']), int(type_id[key]['end_id']))
                if compId not in errorCompIds and compId not in compIds:
                    curString = string + "::" + str(compId).zfill(4) + "::" + str(randomNum(0, 3))
                    write(curString + '\n')
                    count2 = errorComNum


if __name__ == '__main__':
    with open("typeId.dat", "r", encoding='utf-8') as f:  # 打开文件
        type_id = f.read()  # 读取，读出的是字符串
        # 将字符串转成字典格式
        type_id_dic = json.loads(type_id)  # 输出dict类型
        f_userInfo = open('user.dat', 'w', encoding='utf-8')
        generator(type_id_dic)
