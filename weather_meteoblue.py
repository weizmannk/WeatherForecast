import caching
import json
import os
from geopy.geocoders import Nominatim  # install geopy by using: pip install geopy
from datetime import datetime
import numpy as np
import requests
from astroplan import Observer, FixedTarget  # observation and Targeting
from astropy.coordinates import get_sun, get_moon, get_body
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import EarthLocation  # Location on the Earth
# Even if you don't have connexion, you will use teh cach of IERS Bulletin A
#conf.auto_max_age = None
from astropy.utils.data import conf
from datetime import datetime 

cache   = dict()

now = datetime.utcnow().strftime("%H:%M:%S")

API_key = "  " # input your Api key for download the json data of meteoblue

lat = 43.75203
lon = 6.92353
elev = 1320.0

position = np.array([lat, lon, elev])
timezone =  "utc" #"Europe%2FParis"  # we can replace "%2F" by "/",

#===================================================================
#Geolocation of the telescope
#===================================================================
def loclization(position):
    """This function get input the longitude, latitude and the elevetion, 
        and return the specificity rely on  this place.
    """
    latitude = float(position[0])
    longitude = float(position[1])
    elevation = float(position[2])


    location = EarthLocation.from_geodetic(longitude*u.deg, latitude*u.deg, elevation*u.m)
    zone     = Observer(location=location)
    return zone

def telescope_geo_location(position):
    """ In input  give  the city geographic coordinates 
        and get in output the name of the city 
    """

    latitude = str(position[0])
    longitude = str(position[1])
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        location = geolocator.reverse(latitude+","+longitude, language="en")
        address = location.raw['address']
        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')

        return city, state, country, address, location

    except ValueError:
        return 0

    except:
        print("Please enter a valid latidute and longitude of the telescope location ")
def geographical_coordinates():

    """ Return a numpy array list of the telescope locations for
        Global Rapid Advanced Network Devoted to the Multi-messenger Addicts, 
        as follow : [latitude, longitude, elevation]
    """
    ATLAS           = [20.7204, -156.1552, 3055.0, "ATLAS"]
    Abastunami_T48  = [41.754021, 42.820776, 1610.0, "Abastunami_T48 "]
    #Abastunami_T70 = [41.754021, 42.820776, 1610.0, "Abastunami_T70"]
    BlackGEM        = [-29.261165622, -70.731330408, 2400.0, "BlackGEM  "]
    CFHT            = [20.0203, -155.6719, 812.09, "CFHT"]
    DECam           = [-30.1691, -70.8062, 2241.4, " DECam"]
    F60             = [40.3942, 117.5750, 900.0, "F60"]
    FAKE            = [-30.1716, -70.8009, 2207.0, "FAKE"]
    FZU_Auger       = [-35.4956928, -69.4494508, 2200, "FZU_Auger"]
    FZU_CTA_N       = [28.7621233, -17.8899317, 2200, "FZU_CTA_N"]
    GIT             = [32.779444, 78.964167, 4500.0, "GIT"]
    GOTO_4          = [28.7134, -17.9058, 2396, "GOTO_4 "]
    GWAC            = [40.3942, 117.5750, 900.0, "GWAC"]
    Gattini         = [33.3563, -116.8648, 1742.0, "Gattini"]
    IRIS            = [43.9330, 5.7147, 648, "IRIS "]
    KPED            = [31.9599, -111.5997, 2096, "KPED"]
    LSST            = [-30.1716, -70.8009, 2207.0, "LSST"]
    Lisnyky_AZT8    = [50.297841, 30.524550, 156.0, "Lisnyky_AZT8 "]
    Makes_60        = [-21.201387, 55.407463, 970.0, "Makes_60"]
    NOWT            = [43.78, 87.28, 2080, "NOWT"]
    Nickel          = [37.3414, -121.6429, 1283, "Nickel"]
    OAJ             = [40.0420111, -1.0161911, 1957.0, "OAJ "]
    OSN             = [37.0629145, -3.3881303, 2896, "OSN"]
    PS1             = [20.7204, -156.1552, 3055.0, "PS1 "]
    SVOM_MXT        = [-30.0, -61.7, 1000, "SVOM_MXT"]
    SVOM_VT         = [0.0, 0.0, 0.0, "SVOM_VT"]
    SWOPE           = [-29.0182, -70.6915, 2380, "SWOPE "]
    ShAO_T60        = [40.782179, 48.600159, 156.0, "ShAO_T60"]
    TCA             = [43.75203, 6.92353, 1320.0, "TCA"]
    TCH             = [-29.2608, -70.7322, 2347.0, "TCH"]
    TNT             = [40.3942, 117.5750, 900, "TNT"]
    TRE             = [-21.201387, 55.407463, 970.0, "TRE"]
    #UBAI_T60N      = [38.67, 66.39, 2593.0, "UBAI_T60N"]
    UBAI_T60S       = [38.67, 66.39, 2593.0, "UBAI_T60S"]
    VIRT            = [18.35234, -64.9568, 420, "VIRT"]
    WINTER          = [33.3571, -116.8662, 1696.0, " WINTER "]
    ZTF             = [33.3563, -116.8648, 1742.0, "Zadko"]
    Zadko           = [-31.356667, 115.713611, 50.0, "Zadko  "]
    meniscus        = [41.754021, 42.820776, 1610.0, "meniscus"]
    #meniscus_50    = [41.754021, 42.820776, 1610.0, "meniscus_50"]

    coordinates = np.array([ATLAS, Abastunami_T48, BlackGEM, CFHT, DECam, F60, FAKE, FZU_Auger, FZU_CTA_N, GIT,\
                               GOTO_4, GWAC, Gattini, IRIS, KPED, LSST, Lisnyky_AZT8, Makes_60, NOWT, Nickel, OAJ, OSN,\
                               PS1, SVOM_MXT, SVOM_VT, SWOPE, ShAO_T60, TCA, TCH, TNT, TRE, UBAI_T60S, VIRT,
                               WINTER, ZTF, Zadko, meniscus])
    return coordinates



def meteoblue_link(position, API_key):
    """ Reseach the complet link of meteoblue
        to get the information about the forecast of city  
    """

    lat = str(position[0])
    lon = str(position[1])
    elev = str(position[2])
    
    API_link = "http://my.meteoblue.com/feed/seeing_json?apikey="+API_key +\
        "&lat="+lat+"&lon="+lon+"&asl="+elev+"&tz="+timezone

    return API_link


def json_file(position,  API_key):
    
    """Retun a json file  of weather forecast which we can 
       read the json data about  weather condition
    """
    
    forecast_data = requests.get(meteoblue_link(position, API_key))
    data          = forecast_data.json()

    return data

def get_json(position, API_key):
    """ Check if there is a json cache between 2 updates, 
        if not, download again.
    """
    link = meteoblue_link(position, API_key)
    if link not in cache:
        cache[link]= json_file(position, API_key)
    return cache[link]

def last_forcast_update (data_json):
    """Retur the date and hour of the las update forecast by meteoblue
    """
  
    last_update = data_json["meta"]["last_model_update"]
    timezone = data_json["meta"]["timezone_abbreviation"]
    return last_update, timezone

def daylight_night(data_json):
    
    """This function determine if it's daylight time or night-time
        about the hourly  
    """
    return  data_json["hourly"]["is_daylight"]
   

def hourly_prediction(data_json):
    """Gives the forecast about each hour corresponding of the days .
       We apply a filter to this function and we filter out all daylight data. 
    """
    night = data_json["hourly"]["is_daylight"]
    date = []
    hour = []
    for i in range(len(night)):
        if night[i] ==0 :
            date.append(data_json["hourly"]["date"][i])
            hour.append(data_json["hourly"]["hour"][i])
        else : 
            pass

    return date, hour


def seeing_index(data_json):    
    """Seeing is a state of the air - it is therefore independent of cloud cover
       Seeing1 and Seeing2 are two different models to calculate the visibility of atmospheric air
       Seeing2 gives more weight to the effect of density fluctuations, and is more likely 
         to indicate air "flickering" due to turbulence.
        The arsecond  used to estimate the minimal size of an object which is still visible using telescope aimed at the open sky, 
        expressed as an angle. The arcsecond measures shown are based on "Seeing 1", "Seeing 2" and "Bad layers"
        We apply a filter to this function and we filter out all daylight data. 
    """
    night = data_json["hourly"]["is_daylight"]
    
    seeing1 = []
    seeing2 = []
    arcsec  = []
    for i in range(len(night)):
        if night[i] == 0:
            seeing1.append(data_json["hourly"]["seeing1"][i])
            seeing2.append(data_json["hourly"]["seeing2"][i])
            arcsec.append(data_json["hourly"]["seeing_arcsec"][i])
            
        else:
            pass

    for j in range(len(seeing1)):
        if  seeing1[j]  ==1:
            seeing1[j]  = "Bad "
        elif seeing1[j] ==2:
            seeing1[j]  = "Rather Poor"
        elif seeing1[j] == 3:
            seeing1[j]  = "Average Good"
        elif seeing1[j] == 4:
            seeing1[j]  = "Rather Good"
        else:
            seeing1[j]  = "Excellent"

    for k in range(len(seeing2)):
        if seeing2[k] == 1:
            seeing2[k] = "Bad"
        elif seeing2[k] == 2:
            seeing2[k] = "Rather Poor"
        elif seeing2[k] == 3:
            seeing2[k] = "Average Good"
        elif seeing2[k] == 4:
            seeing2[k] = "Rather Good"
        else:
            seeing2[k] = "Excellent"

    return seeing1, seeing2, arcsec

def cloud_forecast(data_json):

    """Return the weather forecast about clouds and jetstream
       We apply a filter to this function and we filter out all daylight data. 
    """
    night = data_json["hourly"]["is_daylight"]

    high_cloud = []
    mid_cloud  = []
    low_cloud  = []
    jet_stream = []
    for i in range(len(night)):
        if night[i] == 0:
            high_cloud.append(data_json["hourly"]["high_clouds"][i])
            mid_cloud.append(data_json["hourly"]["mid_clouds"][i])
            low_cloud.append(data_json["hourly"]["low_clouds"][i])
            jet_stream.append(data_json["hourly"]["jetstream"][i])
        
        else :
            pass

   
    for j in range(len(jet_stream)):
        if jet_stream[j] < 5 or jet_stream[j] > 30:
            jet_stream[j] = f"{jet_stream[j]} m/s Bad seeing "
        else:
            jet_stream[j] = f"{jet_stream[j]} m/s Good Seeing"
  

    return low_cloud, mid_cloud, high_cloud, jet_stream

def ground_forecast(data_json):

    """ Return the temperature, relative humidity at ground  
        We apply a filter to this function and we filter out all daylight data. 
    """

    night = data_json["hourly"]["is_daylight"]

    temp     = []
    humidity = []
 
    for i in range(len(night)):
        if night[i] == 0:
            temp.append(data_json["hourly"]["temperature"][i])
            humidity.append(data_json["hourly"]["relative_humidity"][i])
            
        else:
            pass
    
    return temp, humidity

def bad_layer(data_json):
    """Bad layers are the atmosphere layers in which turbulence is producing disturbance 
       of air and particles, and thereby influencing the astronomical "Seeing".
       We apply a filter to this function and we filter out all daylight data. 
    """
    night = data_json["hourly"]["is_daylight"]

    top_bad_layer    = []
    bottom_bad_layer = []
    layer_gradient   = []

    for i in range(len(night)):
        if night[i] == 0:

            top_bad_layer.append(data_json["hourly"]["badlayer_top"][i])
            bottom_bad_layer.append(data_json["hourly"]["badlayer_bottom"][i])
            layer_gradient.append(data_json["hourly"]["badlayer_gradient"][i])
        else:
            pass
    
    for j in range(len(layer_gradient)):
        if layer_gradient[j] > 0.5 :
            layer_gradient[j] = str(layer_gradient[j]) + " k/100m"+  " it's a Bad seeing (the seeing is realy impact by bad atmosphere layers)"
        else :
            layer_gradient[j] = str(layer_gradient[j]) + " k/100m" + " it's a Good Seeing" 
    return bottom_bad_layer, top_bad_layer,  layer_gradient

def loctated(data_json):
    
    """Return the latitude, longitude and elevation 
    """
    lat = data_json["meta"]["lat"]
    lon = data_json["meta"]["lon"]
    asl = data_json["meta"]["asl"]

    return lat, lon, asl

def  week_days(data_json):
    """This function gives the date of week's days the prediction the prediction and the date  the the date of the         
    """
    date = data_json["daily"]["date"]
    day = data_json["daily"]["weekday"]
    for i in range(len(day)):
        if   day[i] == "Sun":
             day[i]  = "Sunday"
        elif day[i] == "Mon":
             day[i]  = "Monday"
        elif day[i] == "Tue":
             day[i]  = "Tuesday"
        elif day[i] == "Wed":
             day[i]  = "Wednesday"
        elif day[i] == "Thu":
             day[i]  = "Thursday"
        elif day[i] == "Fri":
             day[i]  = "Friday"
        else:
             day[i]  = "Saturday"
    
    return day, date

def sun_weather(data_json):

    """Return the sunrise and sunset 
    """
    sunset_time = data_json["daily"]["sunset"]
    sunrise_time = data_json["daily"]["sunrise"]

    return  sunrise_time, sunset_time


def moon_weather(data_json):
    """ The different phase of the moon
    """
    moonrise_time   = data_json["daily"]["moonrise"]
    moonset_time    = data_json["daily"]["moonset"]
    moon_phase_name = data_json["daily"]["moonphase_name"]
    moon_age        = data_json["daily"]["moonage"]
    moon_angle      = data_json["daily"]["moonphase_angle"]
    moon_fraction   = data_json["daily"]["moon_illum_fraction"]

    return moonrise_time, moonset_time, moon_phase_name, moon_age, moon_angle, moon_fraction


def sorting_information(data_json):
    """ Information extract, we get telescopet description, and the week weather forecast
    """

    telescope_place = telescope_geo_location(position)
    city_place = telescope_place[0]
    state = telescope_place[1]
    country = telescope_place[2]
    telescope_discription = telescope_place[4]
    if city_place == "":
        city = state
    else:
        city = city_place

    week      = week_days(data_json)
    update    = last_forcast_update(data_json)
    sun       = sun_weather(data_json)
    moon      = moon_weather(data_json)
    timetable = hourly_prediction(data_json)

    ground    = ground_forecast(data_json)
    seeing    = seeing_index(data_json)
    cloud     = cloud_forecast(data_json)
    bad       = bad_layer(data_json)

    with open("forecast_data.txt", "w") as file:
        file.write(f"Welcome to {telescope_discription} \n \
                Here we are at {city} in {country} the weather forecast has been updated on {update[0]} {update[1]}, is as follows: \n")
    
    for i in range(len(week[1])):
        with open("forecast_data.txt", "a") as file:
            file.write(f" On {week[0][i]} {week[1][i]}, sunrise: {sun[0][i]}, sunset: {sun[1][i]}, moonrise: {moon[0][i]}, moonset: {moon[1][i]}, moon's ligth fraction: {moon[5][i]*100} % \n")
        for j in range(len(timetable[0])):
            if timetable[0][j] == week[1][i]:
                with open("forecast_data.txt", "a") as file:
                    file.write(f" *** {timetable[1][j]} h:00 mn - {timetable[1][j]}h :59 mn \n  \
                low clouds: {cloud[0][j]}%, mid clouds:{cloud[1][j]}%, high clouds: {cloud[2][j]}%  jet stream: {cloud[3][j]} \n \
                the seeing1 :{seeing[0][j]}, the seeing2: {seeing[1][j]}, average temperature: {ground[0][j]} °C, relative humidity: {ground[1][j]}% \n \
                from {bad[0][j]}  to {bad[1][j]} m : {bad[2][j]}.\n")

   
    return file #        pdf.output("teter.pdf")  # locate, glob_info,  forecast  # file




# jsn weather forecast data 
data_json= json_file(position, API_key)
#cache = get_json(position, API_key)

#data_json = json.dump(cache, indent=4, sort_keys=False)
#data =json.dumps(data_json, indent=1, sort_keys=False)

sorting_information(data_json)


with open("forecast_data.txt", "r") as data:
    for line in data:
        print(line)
"""

#telescope description 


for i in range(0, 23) :
    date_hour = json_file(position, API_key)["hourly"]["hour"][i]
    weather = json_file(position, API_key)["hourly"]["is_daylight"][i]
    if weather == 1 :
        forecast = "Clear, cloudless sky"
    elif weather == 2:
        forecast = "clear and few cirrus"
    elif weather == 3 :
        forecast = "clear with cirrus"
    elif weather == 4 :
        forecast = "clear with few low clouds"
    elif weather == 5 :
        forecast = "clear with few low clouds and few cirrus"
    elif weather == 6 :
        forecast = "clear with few low clouds and cirrus"
    elif weather == 7 :
        forecast = "partly cloudy"
    elif weather == 8 :
        forecast = "partly cloudy and few cirrus"
    elif weather == 9 :
        forecast = "partly cloudy and cirrus"
    elif weather == 10 :
        forecast = "mixed with some thunderstorm clouds possible"
    elif weather == 11 :
        forecast = "mixed with few cirrus with some thunderstorm louds possible"
    elif weather == 12 :
        forecast = "mixed with cirrus with some thunderstorm clouds possible"
    elif weather == 13 :
        forecast = "clear but hazy"
    elif weather == 14 :
        forecast = "clear but hazy with few cirrus"
    elif weather == 15 :
        forecast = "clear but hazy with cirrus"
    elif weather == 16 : 
        forecast = "fog/low stratus clouds"
    elif weather == 17 :
        forecast = "fog/low stratus clouds few cirrus"
    elif weather == 18 :
        forecast = "fog/low stratus clouds with cirrus"
    elif weather == 19:
        forecast = "mostly cloudy"
    elif weather == 20 :
        forecast = "mostly cloudy and few cirrus"
    elif weather == 21 :
        forecast = "mostly cloudy and cirrus"
  elif weather == 22 :
        forecast = "overcast(cloudy) "
  elif weather == 23 :
        forecast = "overcast(cloudy) with rain"
  elif weather == 24 :
        forecast = "overcast(cloudy) with snow"
 elif weather == 25 :
        forecast = "overcast(cloudy) with heavy rain"
 elif weather == 26 :
        forecast = "overcast(cloudy) with heavy snow"
 elif weather == 27 :
        forecast = "rain, thunderstorms likely"
 elif weather == 28 :
        forecast = "ligth rain, thunderstorms likely"
 elif weather == 29 :
        forecast = "storm with heavy snow"
 elif weather == 30 :
        forecast = "heavy rain, thunderstorms likely"
 elif weather == 31 : 
        forecast = "mixed with showers"
 elif weather == 32 :
        forecast = "mixed with snow showers"
 elif weather == 33 :
        forecast = "overcast(cloudy) with light rain"
 elif weather == 34 :
        forecast = "overcast(cloudy)  with light snow"
 else :
        forecast = "overcast(cloudy) with mixture of snow and rain"
        




    day1=[]
    day2=[]
    day3=[]
    day4=[]
    day5=[]

    n = 0
    j = 0
    while n < len(week_day)
    date = data_json["daily"]["date"][n]
    for i in range(j, len(data_json["hourly"]["hour"])):
        if date == data_json["hourly"]["date"][i]:
            day1.append(data_json["hourly"]["hour"])
                 
        elif data:
            
            n +=if data:
                

"""
