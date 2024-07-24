import requests
import json
import re
from bs4 import BeautifulSoup

def userInputJson():
    print("We will be giving you a random restaurant based on it's availability of that given date!\n")
    date = input("What date would you like to seat?Respond in the format YYYY-MM-DD: ")
    print("\n")
    time = input("What time would you like to seat?Respond in the format HH:MM: ")
    print("\n")
    party_size = input("How many people are in your party? ")
    return date, party_size, time


def getRestaurant(date, party_size, time):
    list_names = []

    param = {"day": date,"party_size":int(party_size),"time_filter":time}
    query = {"availability":True,"page":1,"per_page":20,"slot_filter":param,"types":["venue"],"order_by":"availability","geo":{"latitude":40.712941,"longitude":-74.006393,"radius":35420},"query":""}
    url = "https://api.resy.com/3/venuesearch/search"
    header = {
    "Authorization":'ResyAPI api_key="SECRET"',
    "X-Resy-Auth-Token":"SECRET",
    "X-Resy-Universal-Auth":"SECRET"
    }

    resy_request = requests.post(url,headers=header,json=query)
    resy_request_object = resy_request.json()

    for i in range(len(resy_request_object['search']['hits'])):
        names = resy_request_object['search']['hits'][i]['_highlightResult']['name']['value']
        soup = BeautifulSoup(names, "html.parser")
        list_names.append(soup.get_text())
        # print(names)
    return list_names


print(getRestaurant(userInputJson()))
