import requests

url = "https://maps.googleapis.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&size=400x400&key=YOUR_API_KEY&signature=YOUR_SIGNATURE"

base_url = "https://maps.googleapis.com/maps/api/staticmap?"

key_url = "&key=AIzaSyB0f3xpXM_cP_VZGppB2t-WNj9XmQy05-U"

# - Required

# Location Parameters:

# This can be either a comma separated latitude,longitude pair; or a string address
center = "RittenHouse+Square,Philadelphia"
center_url = f"&center={center}"

# 1: World, 5: Continent, 10: City, 15: Streets, 20: Buildings
zoom = "14"
zoom_url = f"&zoom={zoom}"

# size: horizontalxvertical i.e. 500x400 defines a map 500 pixels wide by 400 pixels high

# Map Parameters: 
size = "400x400"
size_url = f"&size={size}"


# - Optional

# Map Parameters:

# scale: Can be either "1" or "2", where 2 displays twice as many pixels for high detail

# format: default: PNG, can use GIF, JPEG or PNG.  JPEG: Greater compression, GIF and PNG: Better Detail

# maptype: roadmap, satellite, hybrid, and terrain
maptype = "roadmap"
maptype_url = f"&maptype={maptype}"

# Feature Parameters:

# map_id

# markers: define one or more to attach to the image at specified locations.  See documentation for details
location = "3400+Civic+Center+Blvd,Philadelphia"
markers_url = f"&markers=location:{location}"

# path: single path of two or more connected points

# visible: specifies one or more locations that should remain visible on the map, though no markers or other indicators will be displayed

# style

final_url = base_url + center_url + zoom_url + size_url + markers_url + key_url

