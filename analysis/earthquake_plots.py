from datetime import date
import matplotlib.pyplot as plt
import requests
from collections import Counter
import matplotlib.ticker as mticker


url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson'
params = {
    'starttime': "2000-01-01",
    "maxlatitude": "58.723",
    "minlatitude": "50.008",
    "maxlongitude": "1.67",
    "minlongitude": "-9.756",
    "minmagnitude": "1",
    "endtime": "2018-10-11",
    "orderby": "time-asc",
}

def get_data():
    """Retrieve the data we will be working with."""
    response = requests.get(url = url, params = params, timeout=(5,45))
    response.raise_for_status()  # Raise an error if the request failed
    data = response.json()
    return data
    


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    magnitude = earthquake['properties']['mag']
    return magnitude


# This is function you may want to create to break down the computations,
# although it is not necessary. You may also change it to something different.
def get_magnitudes_per_year(earthquakes):
    """Retrieve the magnitudes of all the earthquakes in a given year.
    
    Returns a dictionary with years as keys, and lists of magnitudes as values.
    """
    mg_per_year = {}
    features = earthquakes.get('features', [])
    for f in features:
        mag = get_magnitude(f)
        if mag is None:
            continue
        year = date.fromtimestamp(f['properties']['time']/1000).year
        if year not in mg_per_year:
            mg_per_year[year] = []
        mg_per_year[year].append(mag)
    return mg_per_year


def plot_average_magnitude_per_year(earthquakes):
    mg_per_year = get_magnitudes_per_year(earthquakes)
    years = sorted(y for y, mags in mg_per_year.items() if mags)
    if not years:
        print("No data after filtering.")
        return
    avg_magnitudes = [sum(mg_per_year[y]) / len(mg_per_year[y]) for y in years]

    plt.figure()
    plt.plot(years, avg_magnitudes, marker='x')
    plt.title('Average Earthquake Magnitude per Year')
    plt.xlabel('Year'); plt.ylabel('Average Magnitude')
    plt.grid(True)
    ax = plt.gca()
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
    plt.tight_layout()
    plt.show()

def plot_number_per_year(earthquakes):
    features = earthquakes.get('features', [])
    years = [get_year(f) for f in features]
    counts = Counter(years)
    xs = sorted(counts.keys())
    ys = [counts[y] for y in xs]
    plt.figure()
    plt.plot(xs, ys, marker='o')
    ax = plt.gca()
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter('%d'))
    plt.title('Number of Earthquakes per Year')
    plt.xlabel('Year'); plt.ylabel('Count')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Run
quakes = get_data()
plot_number_per_year(quakes)
plt.clf()
plot_average_magnitude_per_year(quakes)