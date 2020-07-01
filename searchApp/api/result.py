import flask
import searchApp

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
    
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    return response