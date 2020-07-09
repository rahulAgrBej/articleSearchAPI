import flask
import searchApp
from flask_cors import cross_origin

@searchApp.app.route('/api/outputList', methods=["GET"])
@cross_origin()
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
    context = {}
    context["placeholder"] = ["testing response"]

    resp = flask.jsonify(**context)
    
    return resp