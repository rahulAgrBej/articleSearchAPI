import requests
import json
import searchApp
from datetime import date
import datetime
import math

def sendReqBatch(reqList, requesterURL):

    payload = {}
    
    reqListSent = {}
    reqListSent["requests"] = reqList
    payload["trendReqs"] = json.dumps(reqListSent)
    resp = requests.get(requesterURL, params=payload)
    return resp

def distributeBatches(numReqs, numRequesters):

    distributions = []

    if numReqs > numRequesters:
        minReqs = math.floor(numReqs / numRequesters)
        remainder = numReqs % numRequesters
        
        for reqIdx in range(numRequesters):
            
            distributions.append(minReqs)
            if (remainder != 0) and reqIdx < remainder:
                distributions[reqIdx] += 1
    else:
        for reqIdx in range(numReqs):
            distributions.append(1)

    return distributions

def summarizeResults(respResults, overallResults):
    granularReqs = []

    for result in respResults:
        if result[0] == "granular":
            granularReqs.extend(makeMoreGranular(result[1]))
        elif result[0] == "hits":
            # guarantees results exist
            for articleHit in result[1]:
                sourceCountry = articleHit["sourcecountry"]
                
                if not (sourceCountry in overallResults):
                    overallResults[sourceCountry] = []
                
                overallResults[sourceCountry].append(articleHit)
        elif result[0] == "none":
            sourceCountry = result[1]
            if not (sourceCountry in overallResults):
                overallResults[sourceCountry] = []

    return granularReqs

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

    month = str(inDate.month)
    day = str(inDate.day)

    if inDate.day < 10:
        day = '0' + day
    
    if inDate.month < 10:
        month = '0' + month

    return month + '/' + day + '/' + str(inDate.year)

def createTime(inDate):

    hour = str(inDate.hour)
    minute = str(inDate.minute)
    second = str(inDate.second)

    if inDate.hour < 10:
        hour = '0' + hour

    if inDate.minute < 10:
        minute = '0' + minute
    
    if inDate.second < 10:
        second = '0' + second
    
    return hour + ':' + minute + ':' + second

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

