import Security
import requests
import datetime
import json

_featureLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/EGT18_Gemeentehuizen/FeatureServer/0"
_fieldName = "provincie"
_csvFile = "provincies.csv"

def main():
    token = GetToken()

    print("Getting service info")
    layerInfoUrl = "{}?f=json&token={}".format(_featureLayerUrl,token)
    layerInfo = requests.get(layerInfoUrl).json()

    currentField = [field for field in layerInfo["fields"] if field["name"]==_fieldName][0]
    print("Currently field {} has {} domain values".format(_fieldName,len(currentField["domain"]["codedValues"])))
    f = open(_csvFile,"r")
    lines = f.readlines()
    newCodedValues = []
    for line in lines:
        parts = line.split(",")
        newCodedValues.append({"code":parts[0],"name":parts[1].strip()})

    currentField["domain"]["codedValues"] = newCodedValues
    
    print("Updating field {} to have  {} domain values".format(_fieldName,len(newCodedValues)))
    featureLayerAdminUrl = _featureLayerUrl.replace("/rest/","/rest/admin/")
    params = {"f":"json","token":token}
    params["updateDefinition"] = json.dumps({"fields":[currentField]})
    
    layerUpdateUrl = "{}/updateDefinition".format(featureLayerAdminUrl)
    layerResult = requests.post(layerUpdateUrl,params).json()
    print(layerResult)

    print("script complete")




def GetToken():
    portalurl = "https://www.arcgis.com"
       
    token_URL = "{}/sharing/generateToken".format(portalurl)
    token_params = {'username':Security.Portal_UserName,'password': Security.Portal_Password,'referer': portalurl,'f':'json','expiration':60}
       
    print("requesting token with username: {}".format(Security.Portal_UserName))
    r = requests.post(token_URL,token_params)
    
    token_obj= r.json()
        
    token = token_obj['token']
    expires = token_obj['expires']

    tokenExpires = datetime.datetime.fromtimestamp(int(expires)/1000)

    print("token for user {}, valid till: {}".format(Security.Portal_UserName,tokenExpires))
    return token


if __name__=="__main__":
    main()
