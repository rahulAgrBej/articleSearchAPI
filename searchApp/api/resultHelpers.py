import requests
import json
import searchApp

def sendReqBatch(reqList, requesterURL):

    payload = {}
    
    reqListSent = {}
    reqListSent["requests"] = reqList
    payload["reqListSent"] = json.dumps(reqListSent)
    resp = requests.get(requesterURL, params=payload)
    return resp