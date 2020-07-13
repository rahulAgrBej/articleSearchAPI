import flask
import searchApp
from searchApp.api import scheduler, resultHelpers
import math
import json

# "https://article-search-requester.herokuapp.com/api/sendReqs"
REQUESTERS = [
    "http://127.0.0.1:7000/api/sendReqs"
]

@searchApp.app.route('/api/outputList', methods=["GET"])
def getOutputTypes():
    context = {}
    context["results"] = []
    outputTypes =  ["URL List", "Article Freq Graph", "Title Common Terms"]

    for i in range(len(outputTypes)):
        context["results"].append(
            {
                "id": "outType" + str(i),
                "name": outputTypes[i],
                "selected": 0
            }
        )
    
    resp = flask.jsonify(**context)
    return resp

@searchApp.app.route('/api/search', methods=["GET"])
def returnResults():
    req = flask.request.json

    # for each sourceCountry set up an individual request
    reqList = []
    sourceCountries = req["countries"]

    for country in sourceCountries:
        currReq = []

        currReq.append(req["searchStr"])
        currReq.append(country)
        currReq.append(req["startDate"])
        currReq.append(req["startTime"])
        currReq.append(req["endDate"])
        currReq.append(req["endTime"])

        reqList.append(currReq)

    # a list of request batches for the requesters
    reqBatches = []
    
    if len(reqList) > len(REQUESTERS):
        minReqs = math.floor(len(reqList) / len(REQUESTERS))
        remainderReqs = len(reqList) % len(REQUESTERS)

        startIdx = 0
        endIdx = minReqs

        for i in range(len(REQUESTERS)):

            if remainderReqs != 0:
                if i < remainderReqs:
                    endIdx += 1
            
            reqBatches.append(reqList[startIdx:endIdx])
            startIdx = endIdx
            endIdx += minReqs

    else:
        for i in range(len(reqList)):
            reqBatches.append([reqList[i]])

    for reqIdx in range(len(reqBatches)):
        resp = resultHelpers.sendReqBatch(reqBatches[reqIdx], REQUESTERS[reqIdx])
        print(json.loads(resp.text))

    context = {}
    context["reqBatches"] = json.loads(resp.text)
    return flask.jsonify(**context)
