import requests
import datetime
import Security


portalurl = "https://www.arcgis.com"

serviceCountUrl = "https://services.arcgis.com/emS4w7iyWEQiulAb/arcgis/rest/services/EGT18_Gemeentehuizen/FeatureServer/0/query?f=json&where=1=1&returnCountOnly=true"

##Test without token
r = requests.get(serviceCountUrl) 
print("FeatureCount results:")
print(r.status_code)
print(r.text)

##Get Token       
print("requesting token with username: {}".format(Security.Portal_UserName))
token_URL = "{}/sharing/generateToken".format(portalurl)
token_params = {'username':Security.Portal_UserName,'password': Security.Portal_Password,'referer': portalurl,'f':'json','expiration':60}
      
r = requests.post(token_URL,token_params)
token_obj= r.json()
token = token_obj['token']
expires = token_obj['expires']
tokenExpires = datetime.datetime.fromtimestamp(int(expires)/1000)

print("token for user {}, valid till: {} : {}".format(Security.Portal_UserName,tokenExpires,token))

##Test with token
r = requests.get(serviceCountUrl + "&token="+token)
print("FeatureCount results:")
print(r.status_code)
print(r.text)