# Connect to the Google Maps Platform and query a location

'''

https://developers.google.com/maps/documentation/directions/get-directions#TravelModes
https://developers.google.com/maps/documentation/places/web-service/search-find-place


'''

import requests
import json
from datetime import datetime, timedelta
import pytz
import time

key = "&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"

# ex_url = "https://maps.googleapis.com/maps/api/directions/json?origin=Toronto&destination=Montreal&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"


# = = Capture the ID of an inputted location/address, and return the id

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
    print("============")
    print(place_data["candidates"])
    print("============")
    print(place_data)
    return place_id


# = = Build the URL that will query directions between two locations = = #
# - Required Parameters: origin, destination

def QueryDirections():
    starting_point = input("Where are you leaving from? | In the app, this will be each house's address. ")
    origin = CapturePlaceID(starting_point)

    ending_point = input("Where are you going? | In the app, this will be a person's work. ")
    destination = CapturePlaceID(ending_point)

    base_directions_url = f"https://maps.googleapis.com/maps/api/directions/json?origin=place_id:{origin}&destination=place_id:{destination}"

    # mode: driving, walking, bicycling, transit ; I want to be able to see a few of these, can I do it in one request?
    fields = [
        "&departure_time=now",
        "&traffic_model=best_guess",
        ""
    ]

    key = "&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"

    '''
    final_url = base_directions_url
    for field in fields:
        final_url = final_url += field
    final_url += key
    return final_url
    '''

    final_directions_url = base_directions_url + key

    payload = {}
    headers = {}

    directions_response = requests.request("GET", final_directions_url, headers=headers, data=payload)

    print(directions_response.text)


# = = Build the URL that will query distance (in time and distance) between two locations = = #
# - Required Parameters: origin, destination
def QueryDistance():
    starting_point = input("Where are you leaving from? | In the app, this will be each house's address. ") or "1922 South Lambert Street Philadelphia"
    origin = CapturePlaceID(starting_point)

    ending_point = input("Where are you going? | In the app, this will be a person's work. ") or "3400 Civic Center Blvd Philadelphia"
    destination = CapturePlaceID(ending_point)

    base_distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=place_id:{origin}&destinations=place_id:{destination}"

    # = = = FIELDS = = = #
    # Do I want to make a list of fields, and a loop that builds my url string based on which are enterred?  Or should each be individual like it is?

    # - Mode : Method of transportation
    mode_dict = {
        1: "driving",
        2: "walking",
        3: "bicycling",
        4: "transit",
    }
    mode_selection = mode_dict.get(int(input("Select a mode of transportation.\n - 1 : driving \n - 2 : walking \n - 3 : bike \n - 4 : public transit \n")))
    mode_field = f"&mode={mode_selection}"
    base_distance_url += mode_field

    # - Transit Mode : specifies one or more preferred modes of transit
    transit_mode_dict = {
        1: "bus",
        2: "subway",
        3: "train",
    }
    if mode_selection == "transit":
        transit_mode_selection = transit_mode_dict.get(int(input("Select a mode of transit.\n - 1 : bus \n - 2 : subway \n - 3 : train \n")))
        transit_mode_field = f"&transit_mode={transit_mode_selection}"
        base_distance_url += transit_mode_field

    # - Arrival Time
    arrival_choice = input("Would you like to set arrival time to 9:00am ET? (Enter 'y' for Yes) ")
    if arrival_choice == 'y':
        arrival_field = f"&arrival={CalcWorkArrival()}"
        base_distance_url += arrival_field

    # - Traffic Model : Assumptions to use when calculating traffic
    # Options are "best_guess (default), pessimistic, and optimistic"; since I'm using default I won't add it to my url string
    #choice = input("Would you like to specify a traffic model? \nWould you like your estimate to be the best guess, pessimistic, or optimistic? (y/n) \n")
    traffic_model_field = "&traffic_model="

    # Units : Imperial or Metric
    units_field = "&units=imperial"

    final_distance_url = base_distance_url + units_field + key

    payload = {}
    headers = {}

    distance_response = requests.request("GET", final_distance_url, headers=headers, data=payload)

    distance_data = json.loads(distance_response.text)

    # Display where you're travelling from/to, and how
    if mode_selection == "transit" and arrival_choice == 'y':
        print(f"Going from {starting_point} to arriving at \n{ending_point} by 9:00am ET via {transit_mode_selection}")
    elif mode_selection == "transit":
        print(f"Going from {starting_point} to \n{ending_point} via {transit_mode_selection}")
    else:
        print(f"Going from {starting_point} to \n{ending_point} via {mode_selection}")
        

    # Display the duration (in minutes) and distance (in miles)
    print(distance_data["rows"][0]["elements"][0]["duration"].get("text"))
    print(distance_data["rows"][0]["elements"][0]["distance"].get("text"))
    

def CalcWorkArrival():
    # Set timezone to ET
    tz = pytz.timezone('US/Eastern')

    # Get current datetime in ET
    now = datetime.now(tz)

    # Get date for tomorrow
    tm = now + timedelta(days=1)

    # Create a new datetime object for tomorrow at 9:00am ET
    nine_am_tm = datetime(tm.year, tm.month, tm.day, 9, 0, 0, tzinfo=tz)

    # Get the integer version of the new datetime object
    int_time = int(nine_am_tm.timestamp())
    
    return str(int_time)


# = = = Determine the distance of nearby parks from a location = = = #
# Right now I have a way of capturing place_id from feeding google an address or general location
# This API requires location to be latitidue and longitude
# I can use the Geocoding API to provide address and geocode the API key.  Response will give me JSON object with lat and long
# SO: I'm able to query park locations, however it's not 100% accurate.  When I enter dog_park as my keyword, only 1 dog park comes up in a 5km radius
# and when I just look for parks, it does not see a lot of them, and recomends parks that are far away.  Could still use the feature to determine if there's a park within 1km
def CalcNearbyParkDistance(location, radius):

    response = requests.get(f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&keyword=dog_park&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U")

    result = response.json()

    #results = [json.loads(places_response.text)]
    results = [[result['results'][0]['name'], result['results'][0]['geometry']['location']['lat'], result['results'][0]['geometry']['location']['lng']]]

    i = 0
    # Look for a next page token in the response received from the places API request for parks nearby our location (in coordinates)
    while 'next_page_token' in result:
        # Capture next page token
        next_page_token = result['next_page_token']
        
        # Wait for 2 seconds
        time.sleep(2)

        # Request a response from the next page passed from the previous response
        token_response = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U')

        result = json.loads(token_response.text)

        #print(result['results'][0]['name']) # Access the park's name
        #print(result['results'][0]['geometry']['location']['lat']) # Access the park's latitude
        #print(result['results'][0]['geometry']['location']['lng'])# Access the park's longitude
        #print("====================================================")

        results.append([result['results'][0]['name'], result['results'][0]['geometry']['location']['lat'], result['results'][0]['geometry']['location']['lng']])

    for place in results:
        print(place[0], place[1], place[2])



# = = = RUNNING = = = #
#QueryDistance()
#CalcWorkArrival()

#loc = CapturePlaceID("1922 South Lambert St Philadelphia")
loc = '39.927720, -75.180290'
CalcNearbyParkDistance(loc, str(2000))

# NEXT STEPS
# Make it so that an enterred address captures everything we want in one call
    # Everything we want:  Applicable commutes, Whether or not there's a park in a 1 mile radius; how close it is walking
# Add to your app and potentially redesign the fields to be cleaner/better for comparison
# Determine what views you need, and create them
# Test

# Idea:  Could you potentially pass a Zillow link to the app, and it'd scrape everything for you?