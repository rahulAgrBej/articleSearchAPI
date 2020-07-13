import requests
import json
import searchApp
from datetime import date
import datetime

def sendReqBatch(reqList, requesterURL):

    payload = {}
    
    reqListSent = {}
    reqListSent["requests"] = reqList
    payload["reqListSent"] = json.dumps(reqListSent)
    resp = requests.get(requesterURL, params=payload)
    return resp

def nextGranularSearch(startDate, startTime, endDate, endTime):
    startDiv = startDate.split('/')
    startYear = startDiv[2]
    startMonth = startDiv[0]
    startDay = startDiv[1]
    start = date(int(startYear), int(startMonth), int(startDay))
    startTimeDiv = startTime.split(':')
    startHour = startTimeDiv[0]

    endDiv = endDate.split('/')
    endYear = endDiv[2]
    endMonth = endDiv[0]
    endDay = endDiv[1]
    end = date(int(endYear), int(endMonth), int(endDay))
    endTimeDiv = endTime.split(':')
    endHour = endTimeDiv[0]

    delta = end - start


    if delta.days > 1 and delta.days <= 31:
        return "daily"

    if delta.days <= 1:
        if startDay == endDay:
            if startHour == endHour:
                return "minutely"
            else:
                return "hourly"
        return "hourly"

    return None

def createDate(inDate):
    return str(inDate.month) + '/' + str(inDate.day) + '/' + str(inDate.year)

def createTime(inDate):
    return str(inDate.hour) + ':' + str(inDate.minute) + ':' + str(inDate.second)

def makeGranularReqs(reqList, nextGranularity):

    granularReqs = []
    searchQuery = reqList[0]
    country = reqList[1]

    startDateDiv = reqList[2].split('/')
    startTimeDiv = reqList[3].split(':')
    startDate = datetime.datetime(
        int(startDateDiv[2]),
        int(startDateDiv[0]),
        int(startDateDiv[1]),
        int(startTimeDiv[0]),
        int(startTimeDiv[1]),
        int(startTimeDiv[2])
        )

    endDateDiv = reqList[4].split('/')
    endTimeDiv = reqList[5].split(':')
    endDate = datetime.datetime(
        int(endDateDiv[2]),
        int(endDateDiv[0]),
        int(endDateDiv[1]),
        int(endTimeDiv[0]),
        int(endTimeDiv[1]),
        int(endTimeDiv[2])
    )

    newStart = startDate
    while newStart != endDate:
        if nextGranularity == "daily":
            newEnd = newStart + datetime.timedelta(days=1)
        elif nextGranularity == "hourly":
            newEnd = newStart + datetime.timedelta(hours=1)
        elif nextGranularity == "minutely":
            newEnd = newStart + datetime.timedelta(minutes=1)
        newReq = []
        newReq.append(searchQuery)
        newReq.append(country)
        newReq.append(createDate(newStart))
        newReq.append(createTime(newStart))
        newReq.append(createDate(newEnd))
        newReq.append(createTime(newEnd))
        granularReqs.append(newReq)

        newStart = newEnd

    return granularReqs

def makeMoreGranular(reqList):
    startDate = reqList[2]
    startTime = reqList[3]
    endDate = reqList[4]
    endTime = reqList[5]

    nextGranularity = nextGranularSearch(startDate, startTime, endDate, endTime)

    granularReqs = makeGranularReqs(reqList, nextGranularity)

    return granularReqs

