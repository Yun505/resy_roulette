import requests
import json
import re
from bs4 import BeautifulSoup
from geopy import geocoders

header = {
    # secret
    }

from datetime import datetime
today = datetime.today()
formatted_date = today.strftime("%Y %m %d")

applicable_cuisine_list = [
    'American',
    'Chinese',
    'Cocktail Bar',
    'French',
    'Indian',
    'Italian',
    'Japanese',
    'Korean',
    'Mediterranean',
    'Mexican',
    'New American',
    'Pizza',
    'Seafood',
    'Sushi',
    'Thai'
]




def userInputJson()-> tuple[str, str, str, dict, list[str]]:
    location = get_Location("New York City, New York")
    cuisines_list = []

    print("We will be giving you a random restaurant based on it's availability of that given date!\n")
    date = input("What date would you like to seat?Respond in the format YYYY-MM-DD: ")
    print("\n")

    time = input("What time would you like to seat?Respond in the format HH:MM: ")
    print("\n")

    party_size = input("How many people are in your party? ")
    filter = input("Is there a specific location or cuisine you have in mind? Answer 'y' (yes) or 'n' (no)[no answer will default to NYC]")
    print("\n")

    if filter == "y":
      location  = get_Location(input("What location(city) would you like to eat at? [include country and state if you can]"))
      print("\nApplicable cuisine List: ")
      print(applicable_cuisine_list)
      print("\n")
      cuisine = input("What cuisine would you like to eat? format:\nJapanese, Korean, American").lower()
      cuisines_list = [cuisine.strip() for cuisine in cuisine.split(',')]
      if cuisines_list[0] =='':
        cuisines_list = []

    return date, party_size, time, location, cuisines_list

def get_Location(address:str) -> dict:
  gn = geocoders.GeoNames(username='yunjun505')

  try:
      location = gn.geocode(address)

      if location:
          return {"latitude":location.latitude,"longitude":location.longitude,"radius":35420}
      else:
          print("Address not found")
          return {"latitude":location.latitude,"longitude":location.longitude,"radius":35420}

  except Exception as e:
      print("Error, defaulting to NYC")
      return {"latitude":location.latitude,"longitude":location.longitude,"radius":35420}
  
def getRestaurants(date: str = formatted_date, party_size: str = "2", time: str = "", location: dict = {"latitude":40.712941,"longitude":-74.006393,"radius":35420}, cuisine_list: list[str] = []) -> list[dict]:
    restaurant_list = []

    if time == "":
      param = {"day": date,"party_size":int(party_size)}
    else:
      param = {"day": date,"party_size":int(party_size),"time_filter":time}
    query = {"availability":True,"page":1,"per_page":20,"slot_filter":param,"types":["venue"],"order_by":"availability","geo":location,"query":""}
    url = "https://api.resy.com/3/venuesearch/search"
    resy_request = requests.post(url,headers=header,json=query)
    resy_request_object = resy_request.json()

    for i in range(len(resy_request_object['search']['hits'])):
        add_dict = {}
        name = resy_request_object['search']['hits'][i]['_highlightResult']['name']['value'] 
        parsed_name = BeautifulSoup(name, "html.parser")

        cuisine = resy_request_object['search']['hits'][i]['_highlightResult']['cuisine'][0]['value']

        location = resy_request_object['search']['hits'][i]['_geoloc']
        
        add_dict['name']= name
        add_dict['cuisine'] = cuisine.lower().strip()
        add_dict['location'] = location

        restaurant_list.append(add_dict)


    if len(restaurant_list) != 0 and len(cuisine_list) != 0:
        # print(cuisine_list)
        restaurant_list = filtered_restaurants(restaurant_list, cuisine_list)

    return restaurant_list
    
def filtered_restaurants(restaurant_list: list[dict], cuisine_list: list[str]) -> list[dict]: 
    
    return_list = []
    for x in range(len(restaurant_list)):
        restaurant_cuisine = restaurant_list[x]['cuisine']
        
        if restaurant_cuisine in cuisine_list:
            
            return_list.append(restaurant_list[x])
    return return_list

location = get_Location("New York City, New York")
restaurants = getRestaurants("2024-07-24", "2", "15:30", location, ["japanese"])

for x in range(len(restaurants)):
  print(restaurants[x])
  print(restaurants[x]['cuisine'])







