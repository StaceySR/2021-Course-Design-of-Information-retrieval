# 配置文件
from Recmd.forCompetition import visualize, test


class Const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __init__(self):
        self.CLUSTER_NUMBER = 5
        self.PATH_COMP_DATA_RAW = 'data/compdata.dat'
        self.PATH_COMP_DATA = 'data/compdata.pkl'
        self.PATH_USER_DATA_RAW = 'data/userdata.dat'
        self.PATH_USER_DATA = 'data/userdata.pkl'
        self.PATH_CLUSTER_DATA = 'data/clusters.pkl'
        self.TOP_CLUSTER_NUM = 5  # 选取最近邻群组数量
        self.TOP_USER_NUM = 100  # 相似用户的数量上限
        self.TOP_COMP_NUM = 30  # 推荐竞赛的数量上限
        self.TOP_RE_USER_NUM = 9  # 推荐的潜在合作伙伴
        self.USER_MIN_COMPS = 5  # 有效用户的最小有评分竞赛的数量(大于这个数值视为有效用户)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConstError, "Can't change const value!")
        if not name.isupper():
            raise (self.ConstCaseError, 'const "%s" is not all letters are capitalized' % name)
        self.__dict__[name] = value


config = Const()

# coding=utf-8
# 用户信息
profile = {
    "tags": ['国际级', '组队赛', '免费', '自由', '国家级', '校级'],  # 这里填入感兴趣的一些话题
    "comps": ["2020年“华数杯”全国大学生数学建模竞赛", "MathorCup高校数学建模挑战赛——大数据竞赛", "2020年第十届APMCM亚太地区大学生数学建模竞赛", "中国建设教育协会第十二届全国高等院校学生“斯维尔杯”BIM-CIM创新大赛"]
}

# profile2 = {
#     "tags": ['程序设计', '国际级', '组队赛', '免费', '自由', '国家级', '校级'],  # 这里填入感兴趣的一些话题
#     "comps": ["2020第八届CCF大数据与计算智能大赛", "第45届ICPC国际大学生程序设计竞赛亚洲区域赛（南京）", "2020第十届IT科技节--程序设计大赛"]
# }
#
# profile3 = {
#     "tags": ['商科', '国际级', '组队赛', '免费', '自由', '国家级', '校级'],  # 这里填入感兴趣的一些话题
#     "comps": ["“广纳英才，发现科技未来” 广发银行数字精英校园挑战赛", "“创青春”互联网创意营销大赛", "2020全球农创客大赛"]
# }
#
# profile4 = {
#     "tags": ['体育', '国际级', '组队赛', '免费', '自由', '国家级', '校级'],  # 这里填入感兴趣的一些话题
#     "comps": ["2019年全国大学生国际象棋锦标赛", "第四届中国青海国际民族传统射箭精英赛", "2016珠海高校学生魔方联赛"]
# }


# coding=utf-8
import re
import pickle
import json
import time
import math
import os
import logging
import numpy as np
from sklearn.cluster import KMeans, MiniBatchKMeans
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(levelname)s - %(filename)s:%(lineno)d:%(funcName)s - %(message)s')
logger = logging.getLogger(__name__)

# 参与评分的标签，选自所有图书标签中频数最大的1000个
# 将明确的竞赛类别标签全部提取出来之后，其余的就从其他竞赛特征（主办方、浏览量）中去找topN的作为TOPTAG
TOP_TAGS = [
            "全部", "校级", "市级", "省级", "国家级", "国际级", "自由",
            "免费", "收费",
            "工科", "数学建模", "程序设计", "机器人", "工程机械", "土木建筑", "大数据", "交通车辆", "航空航天", "船舶海洋", "环境能源", "计算机&信息技术", "材料高分子", "电子&自动化",
            "商科", "创业", "商业", "创青春",
            "理科", "数学", "物理", "化学化工", "健康生命&医学", "力学",
            "综合", "职业技能", "挑战杯", "环保公益", "社会综合",
            "文体", "工业&创意设计", "外语", "演讲主持&辩论", "模特", "歌舞书画&摄影", "体育", "科技文化艺术节", "UI设计", "服装设计", "电子竞技",
            ]

TOP_TAGS_INDEXS = {i: TOP_TAGS.index(i) for i in TOP_TAGS}

USER_CLUSTERS = {}
COMP_DICT = {}
USER_DICT = {}

out_fp = open(r'./output.txt', 'w', encoding='utf-8')


def save_pickle(path, data):
    with open(path, 'wb') as fp:
        pickle.dump(data, fp)


def load_pickle(path):
    with open(path, "rb") as fp:
        return pickle.load(fp)


def save_json(path, data):
    with open(path, 'w') as fp:
        json.dump(data, fp)


def load_json(path):
    with open(path, "r") as fp:
        return json.load(fp)


def save_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_user_data():
    print("正在加载用户数据...")
    # print("正在加载用户数据...", file=out_fp)
    global USER_DICT
    if not USER_DICT:
        USER_DICT = load_pickle(config.PATH_USER_DATA)
    return USER_DICT


def load_comps_data():
    print("正在加载竞赛数据...")
    # print("正在加载竞赛数据...", file=out_fp)
    global COMP_DICT
    if not COMP_DICT:
        COMP_DICT = load_pickle(config.PATH_COMP_DATA)
    return COMP_DICT


def load_cluster_data():
    print("正在加载用户聚类数据...")
    # print("正在加载用户聚类数据...", file=out_fp)
    global USER_CLUSTERS
    if not USER_CLUSTERS:
        # clusters.pkl为用户聚类的数据结果，通过pickle包直接保存
        USER_CLUSTERS = load_pickle(config.PATH_CLUSTER_DATA)
        # print("USER_CLUSTERS:", USER_CLUSTERS[0])
    return USER_CLUSTERS


def process_comp_data():
    """
    对竞赛数据进行处理
    原格式： [compid]::[compname]::[tags]
    处理后： {
        compid: {
            "compname": compname,
            "tags": tags
        }
        ...
    }
    """
    path = config.PATH_COMP_DATA_RAW
    data = load_file(path).strip()

    comps_dict = {}
    for line in data.split('\n'):
        compid, compname, tags = line.split('::', 2)
        compname = compname.strip()
        tags = tags.split()
        comps_dict[compid] = {"compname": compname, "tags": tags}
        comps_dict[compname] = {"compid": compid, "tags": tags}
        # comps_dict2[compname] = tags

    path = config.PATH_COMP_DATA
    save_pickle(path, comps_dict)
    COMP_DICT = comps_dict


def process_user_data():
    # print("------------------------------process_user_data--------------------------\n")
    """
    对用户评分数据进行处理，feature 为用户特征向量，由参加过的竞赛计算得出
    原格式： [userid]::[compid]::[score] 
    处理后： {
        userid: {
            "review": [(compid1, score1), (compid2, score2), ... ],
            "feature": {feature1:weight1, feature2:weight2, ...}
        }
        ...
    }
    """
    path = config.PATH_USER_DATA_RAW
    data = load_file(path)
    data = data.split()
    data = [i.split('::') for i in data]

    # print("userData:", data)  # 正常

    compcount = {}
    users_dict = {}

    for userid, compid, score in data:
        try:
            compcount[userid] += 1
        except:
            compcount[userid] = 0

    # print("compcount[userid]:", compcount)

    for userid, compid, score in data:
        if compcount[userid] < config.USER_MIN_COMPS:
            continue
        try:
            users_dict[userid]['review'].append((compid, score))
        except:
            users_dict[userid] = {'review': [(compid, score)]}

    # print("users_dict[userid]:", users_dict)

    top_tags = set(TOP_TAGS)
    comps_dict = load_comps_data()
    # users_dict = load_user_data()
    usercnt = 0
    for userid in users_dict:
        dic = {}
        compcnt = 0
        for compid, score in users_dict[userid]['review']:
            if compid not in comps_dict:
                continue
            comp_tags = set(comps_dict[compid]['tags'])

            compcnt += 1
            tags = comp_tags & top_tags

            for t in tags:
                try:
                    dic[t] += 1
                except:
                    dic[t] = 1

        dic = {i: math.sqrt(dic[i] / compcnt) for i in dic}

        # print("\n-----------------dic:-------------------\n", dic)

        coefficient = math.sqrt(sum([dic[i] ** 2 for i in dic]))  # 归一化，使向量模长为1
        dic = {i: dic[i] / coefficient for i in dic}

        users_dict[userid]['feature'] = dic
        usercnt += 1
        if usercnt % 1000 == 0:
            logger.info("processed {}/{}".format(usercnt, len(users_dict)))

    path = config.PATH_USER_DATA
    save_pickle(path, users_dict)
    USER_DICT = users_dict
    # print("------------------------------finish--------------------------\n")


def dic2vec(features):
    res = [0] * len(TOP_TAGS_INDEXS)
    # res是一个包含1000个元素的列表（这1000个元素分别对应：参与评分的标签，选自所有竞赛标签中频数最大的1000个TOP_TAGS）
    # 会记载所有包含的用户数据中的features值
    # -----将用户所有的feature值与已经整理出的1000个TOP_TAGS一一对应
    for i in features:
        # print("feature:", i, features[i])
        if i in TOP_TAGS_INDEXS:
            res[TOP_TAGS_INDEXS[i]] = features[i]
    return res


def tags2vec(dic):
    coefficient = math.sqrt(sum([dic[i] ** 2 for i in dic]))  # 归一化，使向量模长为1
    dic = {i: dic[i] / coefficient for i in dic}
    # print("dic2vec:", dic2vec(dic))
    v = np.array(dic2vec(dic))
    return v


def draw_pic(data_list):
    # 画出散点图
    for x in range(len(data_list)):
        plt.scatter(data_list[x][0], data_list[x][1], s=30, c='b', marker='.')


def draw_cluster_centers(centers_mat):
    # 画出聚类中心
    for k in range(len(centers_mat)):
        plt.scatter(centers_mat[k][0], centers_mat[k][1], s=60, c='r', marker='D')


def classify_user():
    # print("--------------------------classify_user---------------------------------\n")
    """
    运用 KMeans 算法对用户进行分组，每组取质心作为组特征向量，计算时先找到与用户特征向量近的用户组，降低计算量
    """
    users_dict = load_user_data()
    u = list(users_dict.keys())
    # print("用户总数：", len(users_dict.keys()))  # 用户总数： 158434
    # print(users_dict)

    # print(users_dict[i]["feature"] for i in u)
    # feature: {'房地产': 0.1132277034144596, '思维': 0.19611613513818407}

    X = np.array([dic2vec(users_dict[i]['feature']) for i in u])  # 二维数组，每个用户的feature值对应的dic占据一行
    print("x的值为：\n", X)
    # print(X.shape)  # 二维数组的shape：(158434, 1000)，总共158434个用户的数据，每个用户总共1000个数据
    # 将获取到的所有用户数据中的feature值全部与整理出来的1000个TOP_TAGS一一对应，然后填入一个size为1000的列表中

    # MiniBatchKMeans类似于KMeans算法，只不过是K-Means算法的一种优化变种，采用小规模的数据子集，减少计算时间
    # n_clusters: 即我们的k值，和KMeans类的n_clusters意义一样，因此这里的CLUSTER_NUMBER是最终需要聚成多少类别
    # init_size: 用来做质心初始值候选的样本个数，默认是batch_size的3倍，一般用默认值就可以了。
    # 最终返回的结果是指，每个用户所属的类别，用一个数组array来记录。y:  [2 2 1 1 2 2 2 0]
    y = MiniBatchKMeans(n_clusters=config.CLUSTER_NUMBER, random_state=0, verbose=True, max_no_improvement=100,
                        init_size=3 * config.CLUSTER_NUMBER).fit_predict(X)

    # print("x：", X)
    # print("y: ", y)
    # print(type(y))
    print("预测结果y值：", y)  # 这个值是什么意思，y是一个ndarray类型的值（数组），其中每一个元素代表第i个用户所属的用户聚类别
    clusters = [{} for _ in range(config.CLUSTER_NUMBER)]
    # print("clusters:", clusters)
    for i in range(config.CLUSTER_NUMBER):
        users = [u[j] for j in range(len(y)) if y[j] == i]
        # print("users", i, ':', users)
        vects = [X[j] for j in range(len(y)) if y[j] == i]
        # print("vects:" i, ':',vects)
        # print(type(vects))
        # print("vects:", vects)
        # print("sum(vect):", sum(vects))
        # print(type(sum(vects)))  # ndarray类型
        centroid = sum(vects) / len(vects)
        # vects里面包含多个array，求sum也是将每个array进行求和
        # 求len是计算出vects中包含几个array，也就是一个用户聚类中包含的用户个数
        # 那么这里就是对于一个群体的用户的feature求 **均值**(centroid=质心)
        # print("len(vects):", len(vects))
        clusters[i]['users'] = users
        clusters[i]['centroid'] = centroid
    print("clusters:", clusters)
    # print("len(clusters):", len(clusters))  # 聚类成几类用户，这个len就是多少，
    # 然后clusters中的每一个元素都是一个字典[{'users(第几类用户群体)':['user1', 'user2', 'user3'....], 'centroid': array([])}]
    path = config.PATH_CLUSTER_DATA
    # print(clusters)
    save_pickle(path, clusters)
    USER_CLUSTERS = clusters
    # print("---------finish--------------\n")


def calc_euclidean_distance(vector1, vector2):
    # 计算两向量的欧几里得距离
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    res = np.linalg.norm(vector1 - vector2)
    return res


def calc_cosine_distance(vector1, vector2):
    # 计算两向量的余弦距离
    vector1 = np.array(vector1)
    vector2 = np.array(vector2)
    res = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * (np.linalg.norm(vector2)))
    return res


def show_user(users_dict, comps_dict, userid):
    u = users_dict[userid]
    b = [comps_dict[compid]['compname'] for (compid, score) in u['review'] if compid in comps_dict]
    _ = [(val, key) for (key, val) in u['feature'].items()]
    _.sort(reverse=True)

    t = ["{}({})".format(tag, str(score)[:5]) for (score, tag) in _]
    t = ', '.join(t)
    print("[{}] - [{}] - [{}]\n".format(userid, b, t))
    print("[{}] - [{}] - [{}]\n".format(userid, b, t), file=out_fp)


def recommend_by_feature(vector):
    # print("------------------------------recommend_by_feature--------------------------\n")
    # 根据用户特征向量进行匹配

    clusters = load_cluster_data()
    comps_dict = load_comps_data()
    users_dict = load_user_data()
    clu_dist = [(calc_euclidean_distance(vector, clusters[index]['centroid']), index) for index, item in
                enumerate(clusters)]  # 将该用户特征与每个聚类群体的组特征向量“质心”进行“距离”计算
    clu_dist.sort()
    clu_dist = clu_dist[:config.TOP_CLUSTER_NUM]
    # print一下看看这是什么样的
    # print("clu_dist:", clu_dist)

    similar_users = []
    for _, i in clu_dist:
        clu = clusters[i]
        similar_users.extend(clu['users'])
    similar_users = [(calc_euclidean_distance(vector, dic2vec(users_dict[item]['feature'])), item) for index, item in
                     enumerate(similar_users)]
    similar_users.sort(reverse=True)
    similar_users = similar_users[:config.TOP_USER_NUM]
    similar_users = [i for i in similar_users if i[0] > 0.5][:config.TOP_RE_USER_NUM]
    # print(similar_users[:100])
    # for s,n in similar_users[:100][::-1]:
    #     print((n, s))

    recommend_comps = []
    for k, u in similar_users:
        comps = [(int(score) * k, compid) for (compid, score) in users_dict[u]['review']]
        recommend_comps.extend(comps)

    d = {}
    for score, compid in recommend_comps:
        if compid in d:
            d[compid] += score
        else:
            d[compid] = score

    recommend_comps = list(d.items())
    recommend_comps.sort(reverse=True, key=lambda x: x[1])
    recommend_comps = recommend_comps[:config.TOP_COMP_NUM]
    # print("------------------------------finish--------------------------\n")
    return recommend_comps, similar_users


def process_data():
    if not os.path.exists(config.PATH_COMP_DATA):
        if not os.path.exists(config.PATH_COMP_DATA_RAW):
            print("未找到竞赛数据：{}".format(config.PATH_COMP_DATA_RAW))
            exit()
        print("正在处理竞赛数据：{}".format(config.PATH_COMP_DATA_RAW))
        process_comp_data()
    if not os.path.exists(config.PATH_USER_DATA):
        if not os.path.exists(config.PATH_USER_DATA_RAW):
            print("未找到用户评分数据：{}".format(config.PATH_USER_DATA_RAW))
            exit()
        print("正在处理用户评分数据：{}".format(config.PATH_USER_DATA_RAW))
        process_user_data()
    if not os.path.exists(config.PATH_CLUSTER_DATA):
        print("正在对用户进行聚类...")
        classify_user()
    pass


def recommend(profile):
    # print("------------------------------recommend-------------------------------\n")
    top_tags = set(TOP_TAGS)
    # print("COMP_DICT:", COMP_DICT)
    comps_dict = COMP_DICT
    dic = {}
    compcnt = 0
    for compname in profile['comps']:
        if compname not in comps_dict:
            continue
        comp_tags = set(comps_dict[compname]['tags'])
        compcnt += 1  # 用户填写的有效comp数量
        tags = comp_tags & top_tags
        # 将该用户填写的comp_name去所有的comp标签comp_dict中寻找，然后同时找到这些comp_name的tags，
        # 将这些tags与整理出来的参与评分的1000个标签取交集（找到相同的元素）
        # print(tags)
        for t in tags:
            try:
                dic[t] += 1
            except:
                dic[t] = 1

    # print("dic0:", dic)  # 这里的dic便是记录着用户填写的所有comp_name中包含的所有tags，并且还包含了每个tag出现的频率：dic0: {'科幻小说'（tag): 2(频率)}
    for t in profile['tags']:
        # 这里是遍历用户自己填写的profile中的所有tags，将之与之前用户填写的所有comp_name中包含的所有tags，合并起来，
        # 新出现的tag就将其频率赋值为1；重复出现的就将其出现的频率增加
        try:
            dic[t] += (compcnt // 2) if compcnt >= 2 else 1
            # print("1", t, dic[t], (compcnt // 2) if compcnt >= 2 else 1)
        except:
            dic[t] = (compcnt // 2) if compcnt >= 2 else 1
            # print("2", t, dic[t], (compcnt // 2) if compcnt >= 2 else 1)

    # print("compcnt:", compcnt)
    # print("dic1:", dic)
    dic = {i: math.sqrt(dic[i] / (compcnt if compcnt > 0 else 1)) for i in dic}  # tag出现的频率 / 用户填写的comp数量，之后再开根号
    # print("dic2:", dic)
    coefficient = math.sqrt(sum([dic[i] ** 2 for i in dic]))  # 归一化，使向量模长为1（所有经过计算的tag频率的平方和求和，再开根号）
    dic = {i: dic[i] / coefficient for i in dic}
    # print("dic3:", dic)
    vector = tags2vec(dic)  # 将dic转成array形式，将dic装进1000个topTags对应的数组array中，将每个数据装到对应的每个标签位置处
    # print("vector:", vector)
    # print("len(vector):", len(vector))
    # print("------------------------------finish--------------------------\n")
    return recommend_by_feature(vector)  # 然后进入该函数分析


def load_data():
    load_user_data()
    load_comps_data()
    load_cluster_data()
    print("数据加载完成")


if __name__ == '__main__':
    process_data()
    load_data()
    recommend_comps, similar_users = recommend(profile)

    comps_dict = COMP_DICT
    users_dict = USER_DICT

    print("------------------------------推荐结果--------------------------------")
    print("与您参赛兴趣相似的用户：")
    # similar_users传给可视化
    visualize.similarUserPicCircle(similar_users, users_dict, comps_dict)

    for sim, user in similar_users:
        print("\nUserID: {} 相似度: {:.3}".format(user, sim))
        print("\nUserID: {} 相似度: {:.3}".format(user, sim), file=out_fp)
        comps = [(comps_dict[i[0]]['compname'] + "  评分：{}".format(i[1])) for i in users_dict[user]['review'] if
                 i[0] in comps_dict]
        print("Ta 参加过的竞赛：\n    {}".format("\n    ".join(comps)))
        print("Ta 参加过的竞赛：\n    {}".format("\n    ".join(comps)), file=out_fp)

    print("\n为您推荐的竞赛：\n")
    print("\n为您推荐的竞赛：\n", file=out_fp)

    # 显示推荐内容，格式为 [推荐指数, compname, comptags]
    for compid, val in recommend_comps:
        if compid not in comps_dict:
            continue
        item = comps_dict[compid]
        if item['compname'] in profile['comps']:
            continue
        print('推荐度[{:.4}] - [{}] - [{}]'.format(val, item['compname'], item['tags']))
        print('推荐度[{:.4}] - [{}] - [{}]'.format(val, item['compname'], item['tags']), file=out_fp)

    # 推荐竞赛结果TOP30可视化
    test.manySimilarCompsPic(recommend_comps, comps_dict)


