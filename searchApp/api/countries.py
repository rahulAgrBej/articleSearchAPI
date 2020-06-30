import flask
import searchApp

@searchApp.app.route('/api/countryList', methods=["GET"])
def getCountryList():

    f = open('searchApp/static/supportedCountries.txt', 'r')
    numCountries = int(f.readline().rstrip('\n'))
    countryList = []

    for i in range(numCountries):
        countryLine = f.readline().rstrip('\n').split('\t')
        countryCode = countryLine[0]
        countryName = countryLine[1]
        countryList.append({"code": countryCode, "name": countryName})
    
    f.close()

    context = {}
    context["countryList"] = countryList

    response = flask.jsonify(**context)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Content-Type', 'application/json')
    
    return response