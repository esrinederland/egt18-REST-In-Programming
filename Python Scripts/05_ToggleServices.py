import requests
import Security
import datetime

_serverurl = "http://localhost:6080/arcgis/admin"
_action = "stop";
def main():
    
    token = GetToken()

    servicesUrl = "{}/services?f=json&token={}".format(_serverurl,token)
    r = requests.get(servicesUrl)
    services = r.json()

    for service in services["services"]:
        print("Set service {} to {}".format(service["serviceName"],_action))

        serviceActionUrl = "{}/services/{}.{}/{}?f=json&token={}".format(_serverurl,service["serviceName"],service["type"],_action,token)

        r = requests.post(serviceActionUrl)

        print("result: {}".format(r.text))

    print("Script complete")

def GetToken():

    token_url = "{}/generateToken".format(_serverurl)
    token_params = {'username':Security.Server_UserName,'password': Security.Server_Password,'client': 'requestip','f':'json','expiration':60}
    print("requesting token with username: {}".format(Security.Server_UserName))
    r = requests.post(token_url,token_params)
        
    print("Resultcode: {}".format(r.status_code))
    token_obj= r.json()
        
    token = token_obj['token']
    expires = token_obj['expires']

    tokenExpires = datetime.datetime.fromtimestamp(int(expires)/1000)

    print("token for user {}, valid till: {} : {}".format(Security.Server_UserName,tokenExpires,token))
    return token  

if __name__ == "__main__":
    main()