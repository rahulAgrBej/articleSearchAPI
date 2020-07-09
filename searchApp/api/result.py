import flask
import searchApp
import scheduler

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

@searchApp.app.route('/api/search', methods=["POST"])
def returnResults():
    req = request.json()

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