# This is where functions will go
import requests
import json
from datetime import datetime, timedelta
import pytz
import time
from .models import House
from django.db.models import Q

key = "&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"

def Calc_Neighborhood_Scores(neighborhood):

    neighbor_scores = {
        "Point Breeze": {
            "food": 2,
            "shopping": 3,
            "errands": 2,
            "nightlife": 2,
        },
        "Grays Ferry": {
            "food": 1,
            "shopping": 1,
            "errands": 1,
            "nightlife": 1,
        },
        "West Passyunk": {
            "food": 2,
            "shopping": 2,
            "errands": 2,
            "nightlife": 2,
        },
        "Fairmount": {
            "food": 2,
            "shopping": 3,
            "errands": 2,
            "nightlife": 1,
        },
        "CentralSouth philly": {
            "food": 3,
            "shopping": 2,
            "errands": 2,
            "nightlife": 2,
        },
        "University City": {
            "food": 3,
            "shopping": 3,
            "errands": 3,
            "nightlife": 4,
        },
        "Graduate Hospital": {
            "food": 3,
            "shopping": 4,
            "errands": 3,
            "nightlife": 4,
        },
        "Newbold": {
            "food": 3,
            "shopping": 3,
            "errands": 3,
            "nightlife": 3,
        },
        "Passyunk Square": {
            "food": 4,
            "shopping": 4,
            "errands": 5,
            "nightlife": 3,
        },
        "Hawthorne": {
            "food": 4,
            "shopping": 4,
            "errands": 5,
            "nightlife": 4,
        },
        "Bella Vista": {
            "food": 5,
            "shopping": 5,
            "errands": 5,
            "nightlife": 5,
        },
        "Queen Village": {
            "food": 5,
            "shopping": 5,
            "errands": 5,
            "nightlife": 5,
        },
        "Society Hill": {
            "food": 5,
            "shopping": 5,
            "errands": 4,
            "nightlife": 5,
        },
        "Fitler Square": {
            "food": 4,
            "shopping": 5,
            "errands": 4,
            "nightlife": 4,
        },
        "Rittenhouse Square": {
            "food": 5,
            "shopping": 5,
            "errands": 4,
            "nightlife": 5,
        },
        "Washington Square": {
            "food": 5,
            "shopping": 5,
            "errands": 4,
            "nightlife": 5,
        },
        "Old City": {
            "food": 5,
            "shopping": 5,
            "errands": 4,
            "nightlife": 5,
        },
        "Chinatown": {
            "food": 5,
            "shopping": 5,
            "errands": 5,
            "nightlife": 5,
        },
    }

    food_score = neighbor_scores.get(neighborhood).get("food")
    shopping_score = neighbor_scores.get(neighborhood).get("shopping")
    errand_score = neighbor_scores.get(neighborhood).get("errands")
    nightlife_score = neighbor_scores.get(neighborhood).get("nightlife")

    return [food_score, shopping_score, errand_score, nightlife_score]


def Calc_Commutes(user, house):
     
    # grab user address
    dest = user.profile.work_address.replace(" ", "%")

    # grab house location
    loc = house.address.replace(" ", "%")

    # run a function to calculate time it takes to drive, bus, and walk
    key = "&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"

    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="

# We'll pass our user's address into this, as-well as the home address to capture their place_id
def CapturePlaceID(location):
    # Base URL
    base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="

    # Required Parameter: Input - Text string on which to search; this must be a place name, address, or category of establishments
    place_input = location.replace(" ", "%")

    # place_id URL | Combine the base url, with address provided, asking for the place_id field, and providing the API key
    place_id_url = base_url + place_input + "&inputtype=textquery&fields=place_id&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"
    payload = {}
    headers = {}

    # send a GET request to the places API URL, passing in our origin and 
    place_id_response = requests.request("GET", place_id_url, headers=headers, data=payload)

    # capture the place ID
    place_data = json.loads(place_id_response.text)
    place_id = place_data["candidates"][0]["place_id"]
    return place_id

def CaptureCoordinates(address):

    import requests

    # Key
    API_KEY = 'AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U'

    # Build the API URL for the Geocoding API
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'

    # Send a request to the Geocoding API
    response = requests.get(url)

    # Parse the JSON response
    data = response.json()

    # Extract the latitude and longitude from the response
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']

    # Print the latitude and longitude
    return {
        "lat": latitude,
        "long": longitude
    }


def CalcWorkArrival(hour=9, minutes=0):
    # Set timezone to ET
    tz = pytz.timezone('US/Eastern')

    # Get current datetime in ET
    now = datetime.now(tz)

    # Get date for tomorrow
    tm = now + timedelta(days=1)

    # Create a new datetime object for tomorrow at 9:00am ET
    nine_am_tm = datetime(tm.year, tm.month, tm.day, hour, minutes, 0, tzinfo=tz)

    # Get the integer version of the new datetime object
    int_time = int(nine_am_tm.timestamp())
    
    return str(int_time)

def QueryDistance(user, house):
#def QueryDistance():
    # Dictionary that will be returned containing each commute's information such as method
    commutes = {
        "work": {
            "driving":{
                "time":None,
                "distance":None,
            },
            "walking":{
                "time":None,
                "distance":None,
            },
            "bus":{
                "time":None,
                "distance":None,
            }
        }, 
        "gym":{
            "driving":{
                "time":None,
                "distance":None,
            },
            "walking":{
                "time":None,
                "distance":None,
            },
            "bus":{
                "time":None,
                "distance":None,
            }
        }
    }

    # Starting Location | House's Address
    origin = CapturePlaceID(house.address)
    #origin = CapturePlaceID("1922 South Lambert St Philadelphia")

    # Destination | Work and Gym Addresses
    if user.profile.work_address is None and user.profile.gym_address is None:
        return commutes
    elif user.profile.work_address is None:
        gym = CapturePlaceID(user.profile.gym_address)
        locations = [gym]
    elif user.profile.gym_address is None:
        work = CapturePlaceID(user.profile.work_address)
        locations = [work]
    else:
        work = CapturePlaceID(user.profile.work_address)
        gym = CapturePlaceID(user.profile.gym_address)
        locations = [work, gym]
    #work = CapturePlaceID("3400 Civic Center Blvd Philadelphia")
    #gym = CapturePlaceID("1168 South Broad Street Philadelphia")

    # method of travel
    methods = ["driving", "walking", "bus"]

    # Capture the time it takes to drive/walk/bus to work and the gym based on each house's address
    
    # access both destinations
    for destination in locations:
        if destination == work: # if we're going to work we want to arrive at 9am
            hour=9
            minutes= 0
        else: # if we're going to the gym we want to arrive at 6pm
            hour=6
            minutes = 0

        # Build a URL to request the API based on house address (origin), destination, and method of transport
        # Make a request for each method of transport, for each destination
        for method in methods:
            if method == "bus":
                base_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{origin}&destinations=place_id:{destination}&mode=transit&transit_mode=bus&arrival={CalcWorkArrival(hour, minutes)}&units=imperial&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"
            else:
                base_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{origin}&destinations=place_id:{destination}&mode={method}&arrival={CalcWorkArrival(hour, minutes)}&units=imperial&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"

            payload = {}
            headers = {}

            # Send a request to the API
            response = requests.request("GET", base_url, headers=headers, data=payload)

            # Parse the API response into json so that we can capture the data that we want
            data = json.loads(response.text)
            #print(data)

            # Capture desired data
            commute_time = data["rows"][0]["elements"][0]["duration"].get("text")
            commute_distance = data["rows"][0]["elements"][0]["distance"].get("text")

            # add to our commutes dictionary, the time and distance for that method beneath its destination
            if destination == work:
                commutes["work"][method]["time"] = commute_time
                commutes["work"][method]["distance"] = commute_distance
            else:
                commutes["gym"][method]["time"] = commute_time
                commutes["gym"][method]["distance"] = commute_distance
            
            time.sleep(2)

    #print(commutes)
    return commutes


# function to update all of the latitude and longitudes for houses who don't have one
# def UpdateBlankLatLongs():
#     # query houses who don't have a latitude or longitude
#     houses = House.objects.filter(Q(latitude__isnull=True) | Q(longitude__isnull=True))
#     # run capture coordinates on it
#     for house in houses:
#         print("House:", house.address)
#         house_coordinates = CaptureCoordinates(house.address)
#         house.latitude = house_coordinates["lat"]
#         house.longitude = house_coordinates["long"]
#         house.save()
#         print("Coordinates updated!")

# - - - Run - - - #
# =============== #
#QueryDistance()

#location = "3400 Civic Center Blvd Philadelphia"
#CapturePlaceID(location)

# You need to make a button on the update house individual page, that you click and it updates your commute times for you
# Have a side box that says your addresses; and you can have a button for recalculating work and gym commutes.  May make sense to separate them
# Have it be a separate entity from your form; and if you run the update it will update and then re-load the same page

# Test:  Work address is None
# Test: Gym address is None

class House():
    address = "1922 South Lambert Street Philadelphia"

house1 = House()

#CaptureCoordinates(house)
