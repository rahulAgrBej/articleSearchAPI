import flask
import searchApp
from searchApp.api import scheduler, resultHelpers
import math
import json
import queue
import threading
import concurrent.futures

# 
REQUESTERS = [
    "https://article-search-requester.herokuapp.com/api/getTrends",
    "https://article-search-requester1.herokuapp.com/api/getTrends"
]



@searchApp.app.route('/api/outputList', methods=["GET"])
def getOutputTypes():
    context = {}
    context["results"] = []
    outputTypes =  ["Article Freq Graph"]

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

@searchApp.app.route('/api/searchTrends', methods=['GET'])
def returnTrends():

    req = flask.request.json
    sourceCountries = req['countries']

    reqsUnserviced = queue.Queue()

    for country in sourceCountries:
        currReq = []

        currReq.append(req["searchStr"])
        currReq.append(country)
        currReq.append(req["startDate"])
        currReq.append(req["startTime"])
        currReq.append(req["endDate"])
        currReq.append(req["endTime"])

        reqsUnserviced.put(currReq)

    
    requestResponse = {}
    requestResponse["results"] = []
    
    while not reqsUnserviced.empty():
        batchSizes = resultHelpers.distributeBatches(reqsUnserviced.qsize(), len(REQUESTERS))
        startIdx = 0
        endIdx = 0
        currBatches = []

        for batchSize in batchSizes:
            insertBatch = []
            for i in range(batchSize):
                insertBatch.append(reqsUnserviced.get())
            currBatches.append(insertBatch)
        
        # make multithreaded requests to requesters
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            results = []
            requesterIdx = 0
            for batch in currBatches:
                results.append(executor.submit(resultHelpers.sendReqBatch, batch, REQUESTERS[requesterIdx]))
                requesterIdx += 1
            
            for f in concurrent.futures.as_completed(results):
                requestResponse["results"].extend(f.result().json()['results'])

    return flask.jsonify(**requestResponse)


@searchApp.app.route('/api/search', methods=["GET"])
def returnResults():
    req = flask.request.json
    
    reqsUnserviced = queue.Queue()
    reqsServiced = {}

    # for each sourceCountry set up an individual request
    sourceCountries = req["countries"]
    for country in sourceCountries:
        currReq = []

        currReq.append(req["searchStr"])
        currReq.append(country)
        currReq.append(req["startDate"])
        currReq.append(req["startTime"])
        currReq.append(req["endDate"])
        currReq.append(req["endTime"])

        reqsUnserviced.put(currReq)
    
    overallResults = {}

    while not reqsUnserviced.empty():
        batchSizes = resultHelpers.distributeBatches(reqsUnserviced.qsize(), len(REQUESTERS))
        startIdx = 0
        endIdx = 0
        currBatches = []

        for batchSize in batchSizes:
            insertBatch = []
            for i in range(batchSize):
                insertBatch.append(reqsUnserviced.get())
            currBatches.append(insertBatch)
        
        
        # make multithreaded requests to requesters
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            results = []
            requesterIdx = 0
            for batch in currBatches:
                results.append(executor.submit(resultHelpers.sendReqBatch, batch, REQUESTERS[requesterIdx]))
                requesterIdx += 1
            
            for f in concurrent.futures.as_completed(results):
                print(f.result())
                granularReqs = resultHelpers.summarizeResults(json.loads(f.result().text)["results"], overallResults)
                print("GRANULAR")
                print(granularReqs)
                for gReq in granularReqs:
                    reqsUnserviced.put(gReq)
    
    response = {}
    response["articleResults"] = overallResults
    return flask.jsonify(**response)
