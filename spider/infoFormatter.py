def formatter(linkList, titleList, sponsorList, levelList, applicationTimeList, competitionTimeList, statusList,
              viewList, typeList, feeList, priceList):
    maxLength = max(len(linkList), len(titleList), len(sponsorList), len(levelList), len(applicationTimeList),
                    len(competitionTimeList), len(statusList), len(viewList), len(typeList), len(feeList),
                    len(priceList))
    temp = []
    for i in range(maxLength):
        dict = {"title": titleList[i], "link": linkList[i], "sponsor": sponsorList[i], "level": levelList[i],
                "applicationTime": applicationTimeList[i], "competitionTime": competitionTimeList[i],
                "status": statusList[i], "viewCount": viewList[i], "type": typeList[i], "fee": feeList[i],
                "award": priceList[i]}
        temp.append(dict)
    return temp
