import flask
import searchApp

@searchApp.app.route('/api/outputList', methods=["GET"])
def getOutputTypes():
    context = {}
    context["outputTypes"] = ["URL List", "Article Freq Graph", "Title Common Terms"]
    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    return response