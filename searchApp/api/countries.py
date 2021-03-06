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
        countryList.append(
                {
                "id": countryCode,
                "name": countryName,
                "selected": 0
                }
            )
    
    f.close()

    context = {}
    context["results"] = countryList

    response = flask.jsonify(**context)
    
    return response