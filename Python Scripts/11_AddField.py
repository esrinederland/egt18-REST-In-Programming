import Security
import requests
import datetime
import json

_featureLayerUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/EGT18_Gemeentehuizen/FeatureServer/0"
_newField = {
      "name" : "Klasse", 
      "type" : "esriFieldTypeString",   
      "alias" : "My Dummy Field", 
      "sqlType" : "sqlTypeOther", 
      "length" : 42,
      "nullable" : True, 
      "editable" : True, 
      "visible" : True, 
      "domain" : None, 
      "defaultValue" : "HelloWorld"
    }

def main():
    token = GetToken()

    print("Getting service info")
    
    featureLayerAdminUrl = _featureLayerUrl.replace("/rest/","/rest/admin/")

    params = {"f":"json","token":token}
    params["addToDefinition"] = json.dumps({"fields":[_newField]})

    print("Adding field")
    layerUpdateUrl = "{}/addToDefinition".format(featureLayerAdminUrl)
    layerResult = requests.post(layerUpdateUrl,params)
    print(layerResult.text)

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

