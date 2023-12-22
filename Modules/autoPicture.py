import requests


def getAutoPicture(url,params) -> str: 

    response = requests.get(url, params=params)
    json = response.json()
    url = json['data']['url']
    return url[0]
    #json -> data -> url
    # print(json['data']['url'])

if __name__ == "__main__" :
    print(getAutoPicture('https://api.nyan.xyz/httpapi/sexphoto', params = {'num': '1', 'r18': 'true'}))
