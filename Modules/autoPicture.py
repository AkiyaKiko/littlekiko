import requests


def getAutoPicture(url,params):

    response = requests.get(url, params=params)
    json = response.json()
    return json['data']['url']
    #json -> data -> url
    # print(json['data']['url'])