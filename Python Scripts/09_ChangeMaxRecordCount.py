import Security
import requests
import datetime
import json

_featureServiceUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/EGT18_Gemeentehuizen/FeatureServer"
_newMaxRecordCount = 3000

def main():
    token = GetToken()

    print("Getting service info")
    serviceInfoUrl = "{}?f=json&token={}".format(_featureServiceUrl,token)
    serviceInfo = requests.get(serviceInfoUrl).json()

    featureServiceAdminUrl = _featureServiceUrl.replace("/rest/","/rest/admin/")

    params = {"f":"json","token":token}
    params["updateDefinition"] = json.dumps({"maxRecordCount":_newMaxRecordCount})

    print("Update service root")
    fsUpdateUrl = "{}/updateDefinition".format(featureServiceAdminUrl)
    fsResult = requests.post(fsUpdateUrl,params).json()
    print(fsResult)

    for layer in serviceInfo["layers"]:
        print("Update layer: {}".format(layer["name"]))

        layerUpdateUrl = "{}/{}/updateDefinition".format(featureServiceAdminUrl,layer["id"])
        fsResult = requests.post(layerUpdateUrl,params).json()
        print(fsResult)

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

    print("token for user {}, valid till: {} : {}".format(Security.Portal_UserName,tokenExpires,token))
    return token


if __name__=="__main__":
    main()