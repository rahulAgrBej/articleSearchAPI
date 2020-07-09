import flask
import searchApp


def prepRespHeaders(context):
    resp = flask.jsonify(**context)
    resp = flask.jsonify(**context)
    resp.headers.add('Access-Control-Allow-Origin', '*')
    resp.headers.add('Access-Control-Request-Method', 'POST,GET')
    resp.headers.add('Access-Control-Request-Headers', 'access-control-allow-origin,content-type')
    return resp

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
    
    response = prepRespHeaders(context)
    return response

@searchApp.app.route('/api/search', methods=["POST"])
def returnResults():
    context = {}
    context["placeholder"] = ["testing response"]

    response = prepRespHeaders(context)
    
    return response