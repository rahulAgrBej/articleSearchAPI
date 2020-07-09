import requests
import json
import searchApp

MAX_ARTICLES = 250
STRIPPED = lambda s: "".join(i for i in s if 31 < ord(i) < 127)

def addSourceCountry(searchQuery, country):
    return searchQuery + ' sourcecountry:' + country['id']

def createDateStr(inDate, inTime):

    dateParts = inDate.split('/')
    month = dateParts[0]
    day = dateParts[1]
    year = dateParts[2]

    timeParts = inTime.split(':')
    hours = timeParts[0]
    minutes = timeParts[1]
    seconds = timeParts[2]

    queryDate = year + month + day + hours + minutes + seconds

    return queryDate

# cleans Response from GDELT
def gdeltCleanResp(resp):

    try:
        results = resp.json()
    except json.decoder.JSONDecodeError:
        firstStrip = re.sub('\\\\', '', resp.text)
        correctStr = STRIPPED(firstStrip)
        
        try:
            results = json.loads(correctStr)
        except:
            return None

    return results

'''
inList is a list containing (in this order):
- search query
- source country object
- start date
- start time
- end date
- end time
'''
def getArtList(inList):


    fullQuery = addSourceCountry(inList[0], inList[1])

    # builds payload for GDELT request
    payload = {}
    payload['QUERY'] = fullQuery
    payload['MODE'] = 'ArtList'
    payload['FORMAT'] = 'JSON'
    payload['MAXRECORDS'] = MAX_ARTICLES
    payload['STARTDATETIME'] = createDateStr(inList[2], inList[3])
    payload['ENDDATETIME'] = createDateStr(inList[4], inList[5])
    

    # make GDELT API call
    gdeltURL = 'https://api.gdeltproject.org/api/v2/doc/doc'

    resp = requests.get(gdeltURL, params=payload)
    processedResp = gdeltCleanResp(resp)

    if processedResp == None:
        raise Exception('RESULTS COULD NOT BE CLEANED')

    return processedResp

'''
inList is a list containing (in this order):
- search query
- source country object
- start date
- start time
- end date
- end time
'''
def getUrlList(inList):

    urls = []

    fullArtList = getArtList(inList)
    if len(fullArtList.keys()) > 0:
        articles = fullArtList['articles']
        for result in articles:
            urls.append(result['url'])

    return urls