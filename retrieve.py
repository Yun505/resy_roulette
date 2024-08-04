"""This module retrieves and randomizes restaurants based on user preferences. This is done through a ResyRetriever object
that takes in user preferences and filters restaurants based on those preferences."""

import requests
import os
import random
from bs4 import BeautifulSoup
from geopy import geocoders
from dotenv import load_dotenv
from datetime import datetime
import logging

class ResyRetriever(object):
    """Class that retrieve and randomizes restaurants based on user preferences. 

    Attributes:
        date (str): A string representing the date of the reservation.
        party_size (int): A string representing the number of people in the party.
        time (str): A string representing the time of the reservation.
        location (dict): A dictionary representing the location of the reservation.
        cuisine_list (list[str]): A list of strings representing the cuisines the user wants to eat.
    """

    # Total set of cuisines, static variable
    # Gathered from all available cuisines in Resy
    applicable_cuisine_list = (
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
    )

    @staticmethod
    def get_location(address:str) -> dict:
        """ Helper method to find the longitude and latitude of the location given in address form, defaults to NYC if address is not found
        Takes address of restaurants then, parses through geopy and geonames api to get the latitude and longitude of the location to return
        
        :param str address: String input of user location
        :return dict: dictionary of location's latitude and longitude 
        """

        logger = logging.getLogger(__name__)
        gn = geocoders.GeoNames(username='yunjun505')
        try:
            location = gn.geocode(address)
            return {"latitude":location.latitude,"longitude":location.longitude,"radius":35420}
        except Exception as e:
            logger.info(e)
            logger.info("Error, defaulting to NYC")
            return {"latitude":location['latitude'],"longitude":location['longitude'],"radius":35420}
   
    def __init__(self,
                 date:str=datetime.today().strftime('%Y-%m-%d'),
                 time:str="",
                 location:dict = None,
                 party_size:int = 2,
                 cuisine_list:list[str] = applicable_cuisine_list):
        """Constructor Method

        Args:
            date (str): The date of the reservation.
            time (str): The time of the reservation.
            location (dict, optional): The location of the reservation, in the form {longitude: _, latitude: _, radius: _}. Defaults to that of NYC.
            party_size (int, optional): Requested party size for the reservation. Defaults to 2.
            cuisine_list (list[str], optional): The list of cuisines to search. Defaults to all available cuisines available in Resy.
        """
        self.date = date
        self.party_size = party_size
        self.time = time
        self.location = location

        if not self.location:
            self.location = ResyRetriever.get_location("New York City, New York")

        self.cuisine_list = []

        for cuisine in cuisine_list:
            if cuisine in ResyRetriever.applicable_cuisine_list:
                self.cuisine_list.append(cuisine)
        
        if not self.cuisine_list:
            self.cuisine_list = list(ResyRetriever.applicable_cuisine_list)

        # Logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='myapp.log', level=logging.INFO)

        load_dotenv()
        self.header = {"Authorization":os.environ["AUTHORIZATION"],
                "X-Resy-Auth-Token":os.environ["XRESYAUTHTOKEN"],
                "X-Resy-Universal-Auth": os.environ["XRESYUNIVERSALAUTH"]}
   
    def get_restaurants(self) -> list[dict]:
        """Returns a list of restaurants based on user preferences through filtering and querying Resy Api. Preferences
        already set as fields of ResyRetriever object.

        :return list[dict]: list of filtered restaurants based on the user's inputs
        """    
        restaurant_list = []

        # If user didn't choose a specific time, default to current time
        if self.time == "":
            param = {"day": self.date,"party_size":int(self.party_size)}
        else:
            param = {"day": self.date,"party_size":int(self.party_size),"time_filter":self.time}
    
        # Create a list of dictionaries of restaurants based on the cuisine with attributes of name, cuisine, and location
        self.logger.info(self.cuisine_list)
        for number, cuisine in enumerate(self.cuisine_list):
            self.logger.info("Cuisine number %d: %s", number, cuisine)

            # Query Resy api for the cuisine 
            query = {"availability":True,"page":1,"per_page":20,
                "slot_filter":param,"types":["venue"],
                "order_by":"availability","geo":self.location,"query":"","venue_filter":{"cuisine":cuisine}}
            url = "https://api.resy.com/3/venuesearch/search"
            resy_request_for_total = requests.post(url,headers=self.header,json=query)
            resy_request_object_for_total = resy_request_for_total.json()
            
            # Query Resy api again for the total amount of restaurants in that cuisine to be on one page
            total = resy_request_object_for_total['meta']['total']
            full_query = {"availability":True,"page":1,"per_page":total,
                "slot_filter":param,"types":["venue"],
                "order_by":"availability","geo":self.location,"query":"","venue_filter":{"cuisine":cuisine}}
            resy_request = requests.post(url,headers=self.header,json=full_query)
            resy_request_object = resy_request.json()
        
            # Create a list of dictionaries of restaurants with name, cuisine, and location key
            for i in range(len(resy_request_object['search']['hits'])):
                add_dict = {}
                name = resy_request_object['search']['hits'][i]['_highlightResult']['name']['value']
                parsed_name = BeautifulSoup(name, "html.parser")

                cuisine = resy_request_object['search']['hits'][i]['_highlightResult']['cuisine'][0]['value']
                restaurant_location = resy_request_object['search']['hits'][i]['_geoloc']
                add_dict['name']= parsed_name
                add_dict['cuisine'] = cuisine.lower().strip()
                add_dict['location'] = restaurant_location
                restaurant_list.append(add_dict)
        return restaurant_list
   
    def randomize_restaurants(self, restaurant_list: list[dict]) -> dict:
        """Returns a random restaurant in the filtered restaurant list. If no
        restaurant is provided, calls the get_restaurants method to get a list of restaurants.

        :param list[dict] restaurant_list: restaurant list filtered to user's preferences
        :return dict: returns a dictionary of one restaurant with it's name, cuisine, and location
        """    
        
        if not restaurant_list:
            restaurant_list = self.get_restaurants()
        
        return random.choice(restaurant_list)

def user_input_json()-> ResyRetriever:
    """(Deprecated Method) - Currently used for testing purposes. Actual user input takes place within the Flask application.
    
    Generates a tuple of user preferences based on user input. 

    :return tuple[str, str, str, dict, list[str]]: Generates a tuple of user preferences based on date, party size, time, location, and cuisines they want to eat
    """   

    location = ResyRetriever.get_location("New York City, New York")
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
        location  = ResyRetriever.get_location(input("Location? [include country and state if you can]"))
        print("\nApplicable cuisine List: ")
        print(ResyRetriever.applicable_cuisine_list)
        print("\n")
        print("What cuisine would you like to eat?\n")
        cuisine = input("format:\nJapanese, Korean, American").lower()
        cuisines_list = [cuisine.strip() for cuisine in cuisine.split(',')]

    return ResyRetriever(
        date=date,
        time=time,
        location=location,
        party_size=party_size,
        cuisine_list=cuisines_list
    )

#Testing
# location = get_location("New York City, New York")
# restaurants = get_restaurants("2024-07-30", "2", "15:30", location, [ "Korean","Japanese"])
# for i in range(10):
#     print(randomize_restaurants(restaurants))