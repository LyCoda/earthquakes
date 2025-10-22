# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests

def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"},


            timeout = (5,45)  # (connect timeout, read timeout)
    )
    print(response.status_code)  # 200 means success
    response.raise_for_status()  # Raise an error if the request failed

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    data = response.json()
    

    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    return data
    
def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return (len(data.get("features", [])))


def get_magnitude(feature):
    """Retrive the magnitude of an earthquake item."""
    return (feature.get("properties") or {}).get("mag")


def get_location(feature):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    coords = (feature.get("geometry") or {}).get("coordinates") or []
    return (coords[1], coords[0]) if len(coords) >= 2 else (None, None)

def get_maximum(data):
    features = data.get("features", [])
    candidates = []
    for f in features:
        mag = get_magnitude(f)
        loc = get_location(f)
        if mag is not None and loc != (None, None):
            candidates.append((mag, loc))
    best = max(candidates, key=lambda x: x[0])
    return best

# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
best_mag , best_loc = get_maximum(data)
print(f"The strongest earthquake was at {best_loc} with magnitude {best_mag}")