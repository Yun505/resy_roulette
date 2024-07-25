import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from geopy import geocoders


# Getting the current date in YY:MM:DD to set as default day
today = datetime.today()
formatted_date = today.strftime("%Y %m %d")

# Cuisines on Resy Website that the user can choose from
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

"""
Get user inputs  for date, party size, time, location, cuisines
"""
def user_input_json()-> tuple[str, str, str, dict, list[str]]:
    location = get_location("New York City, New York")
    cuisines_list = []

    print("We will be giving you a random restaurant!\n")
    date = input("What date would you like to seat?Respond in the format YYYY-MM-DD: ")
    print("\n")

    time = input("What time would you like to seat?Respond in the format HH:MM: ")
    print("\n")

    party_size = input("How many people are in your party? ")
    print("The default location is NYC")
    print("Is there a specific location or cuisine you have in mind?\n")
    specific_location_cuisine = input("Answer 'y' (yes) or 'n' (no)")
    print("\n")

    # User's choice if they want a specific cuisine or location they want to dine at
    if specific_location_cuisine == "y":
        location  = get_location(input("Location? [include country and state if you can]"))
        print("\nApplicable cuisine List: ")
        print(applicable_cuisine_list)
        print("\n")
        print("What cuisine would you like to eat?\n")
        cuisine = input("format:\nJapanese, Korean, American").lower()
        cuisines_list = [cuisine.strip() for cuisine in cuisine.split(',')]
        # Check if user inputted any cuisines
        if cuisines_list[0] =='':
            cuisines_list = []

    return date, party_size, time, location, cuisines_list

"""
Take in String input of location and return dictionary of the location's latitude and longitude
"""
def get_location(address:str) -> dict:
    gn = geocoders.GeoNames(username='yunjun505')
    try:
        location = gn.geocode(address)
        return {"latitude":location.latitude,"longitude":location.longitude,"radius":35420}
    except Exception as e:
        print("Error, defaulting to NYC")
        return {"latitude":location.latitude,"longitude":location.longitude,"radius":35420}

"""
 Return restaurant list based on the user's inputs through querying and call filtered_restaurants method to filter for the cuisine 
"""

def get_restaurants(
    date : str = formatted_date,
    party_size: str = "2",
    time : str = "",
    location: dict = {"latitude":40.712941,"longitude":-74.006393,"radius":35420},
    cuisine_list: list[str] = []
) -> list[dict]:
    restaurant_list = []
    # If user didn't choose a specific time, defalt to current time
    if time == "":
      param = {"day": date,"party_size":int(party_size)}
    else:
      param = {"day": date,"party_size":int(party_size),"time_filter":time}

    # Query resy api
    query = {"availability":True,"page":1,"per_page":20,
             "slot_filter":param,"types":["venue"],
             "order_by":"availability","geo":location,"query":""}
    url = "https://api.resy.com/3/venuesearch/search"
    resy_request = requests.post(url,headers=header,json=query)
    resy_request_object = resy_request.json()

    # Create a list of dictionaries of restaurants with name, cuisine, and location key
    for i in range(len(resy_request_object['search']['hits'])):
        add_dict = {}
        name = resy_request_object['search']['hits'][i]['_highlightResult']['name']['value']
        parsed_name = BeautifulSoup(name, "html.parser")

        cuisine = resy_request_object['search']['hits'][i]['_highlightResult']['cuisine'][0]['value']
        location = resy_request_object['search']['hits'][i]['_geoloc']
        add_dict['name']= parsed_name
        add_dict['cuisine'] = cuisine.lower().strip()
        add_dict['location'] = location
        restaurant_list.append(add_dict)

    # Check if there are no restaurants or specific cuisines based on user's needs
    if len(restaurant_list) != 0 and len(cuisine_list) != 0:
        # Filter by cuisine
        restaurant_list = filtered_restaurants(restaurant_list, cuisine_list)

    return restaurant_list

"""
Filter restaurants by the cuisine
"""
def filtered_restaurants(restaurant_list: list[dict], cuisine_list: list[str]) -> list[dict]:
    return_list = []
    for x in range(len(restaurant_list)):
        restaurant_cuisine = restaurant_list[x]['cuisine']
        if restaurant_cuisine in cuisine_list:
            return_list.append(restaurant_list[x])

    return return_list
