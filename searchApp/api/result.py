import flask
import searchApp
from searchApp.api import scheduler, resultHelpers
import math
import json
import queue
import threading
import concurrent.futures

REQUESTERS = [
    "https://article-search-requester.herokuapp.com/api/getTrends",
    "https://article-search-requester1.herokuapp.com/api/getTrends",
    "https://article-search-requester2.herokuapp.com/api/getTrends",
    "https://article-search-requester3.herokuapp.com/api/getTrends",
    "https://article-search-requester4.herokuapp.com/api/getTrends",
    "https://article-search-requester5.herokuapp.com/api/getTrends",
    "https://article-search-requester6.herokuapp.com/api/getTrends",
    "https://article-search-requester7.herokuapp.com/api/getTrends",
    "https://article-search-requester8.herokuapp.com/api/getTrends",
    "https://article-search-requester9.herokuapp.com/api/getTrends"
]

REQUESTERS_FULL_INFO = [
    "https://article-search-requester.herokuapp.com/api/getFullInfo",
    "https://article-search-requester1.herokuapp.com/api/getFullInfo",
    "https://article-search-requester2.herokuapp.com/api/getFullInfo",
    "https://article-search-requester3.herokuapp.com/api/getFullInfo",
    "https://article-search-requester4.herokuapp.com/api/getFullInfo",
    "https://article-search-requester5.herokuapp.com/api/getFullInfo",
    "https://article-search-requester6.herokuapp.com/api/getFullInfo",
    "https://article-search-requester7.herokuapp.com/api/getFullInfo",
    "https://article-search-requester8.herokuapp.com/api/getFullInfo",
    "https://article-search-requester9.herokuapp.com/api/getFullInfo"
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

    reqsUnserviced = queue.Queue()
    incomingReqs = resultHelpers.decodeParams(flask.request.args.get('requestsSent'))

    for iR in incomingReqs:
        reqsUnserviced.put(iR)
    
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
                results.append(executor.submit(resultHelpers.sendReqBatch, batch, REQUESTERS[requesterIdx % len(REQUESTERS)]))
                requesterIdx += 1
            
            for f in concurrent.futures.as_completed(results):
                #print(f.result())
                requestResponse["results"].extend(f.result().json()['results'])

    print(requestResponse)

    print("EXITI TITITITIIT")

    return flask.jsonify(**requestResponse)



@searchApp.app.route('/api/getFullInfo', methods=["GET"])
def returnFullInfo():
    incomingReqs = resultHelpers.decodeParams(flask.request.args.get('requestsSent'))

    reqsUnserviced = queue.Queue()

    for iR in incomingReqs:
        reqsUnserviced.put(iR)
    
    requestResponse = {}
    requestResponse["results"] = []
    
    while not reqsUnserviced.empty():
        batchSizes = resultHelpers.distributeBatches(reqsUnserviced.qsize(), len(REQUESTERS_FULL_INFO))
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
                results.append(executor.submit(resultHelpers.sendFullReq, batch, REQUESTERS_FULL_INFO[requesterIdx % len(REQUESTERS_FULL_INFO)]))
                requesterIdx += 1
            
            for f in concurrent.futures.as_completed(results):
                test = f.result()
                try:
                    requestResponse["results"].extend(test.json()['results'])
                except:
                    print('HERE HERE HERE')
                    print(test.content)
    
    return flask.jsonify(**requestResponse)








#@searchApp.app.route('/api/getFullInfo', methods=["GET"])
def returnResults():

    sourceCountries = resultHelpers.decodeParams(flask.request.args.get('countries'))
    searchQuery = resultHelpers.decodeParams(flask.request.args.get('q'))
    startDate = resultHelpers.decodeParams(flask.request.args.get('startDate'))
    startTime = resultHelpers.decodeParams(flask.request.args.get('startTime'))
    endDate = resultHelpers.decodeParams(flask.request.args.get('endDate'))
    endTime = resultHelpers.decodeParams(flask.request.args.get('endTime'))
    
    reqsUnserviced = queue.Queue()
    reqsServiced = {}

    # for each sourceCountry set up an individual request
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
