import flask
import searchApp
from searchApp.api import scheduler
import math

REQUESTERS = [
    "",
    ""
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
        currReq.append(country["id"])
        currReq.append(req["startDate"])
        currReq.append(req["startTime"])
        currReq.append(req["endDate"])
        currReq.append(req["endTime"])

        reqList.append(currReq)
    
    if len(reqList) > len(REQUESTERS):
        distr = math.floor(len(reqList) / len(REQUESTERS))
        modulo = len(reqList) % len(REQUESTERS)
        reqBatches = []
        startIdx = 0
        endIdx = distr
    else:
        # do this


    """

    inList = []
    inList.append(req['searchStr'])
    inList.append(req['countries'][0])
    inList.append(req['startDate'])
    inList.append(req['startTime'])
    inList.append(req['endDate'])
    inList.append(req['endTime'])

    urls = scheduler.getUrlList(inList)

    context = {
        'urlList': urls
    }

    resp = flask.jsonify(**context)
    
    return resp

    """