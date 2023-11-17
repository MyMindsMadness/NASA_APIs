#!/home/mccube/PersonalProjects/NASA_API/NASAenv/bin/python

import requests 
import inquirer 
import datetime 
import json

class NEO(object):
    name = ""
    size = 0.0
    miss = 0.0
    approach = 0.0
    speed = 0.0
    def __init__(self, name, size, miss, approach, speed):
        self.name = name
        self.size = size
        self.miss = miss
        self.approach = approach
        self.speed = speed
    def __str__(self):
        return f"{self.name}"


def date_get(date_input):
    #date_input = input ("Please enter a date: ")
    try:
        from dateutil import parser
        date = parser.parse(date_input)
    except:
        date = datetime.datetime.strptime(date_input, "%d/%m/%Y")
    date_output = date.strftime("%Y-%m-%d")
    return date #date_output

def url_generator():
    neo_url = "https://api.nasa.gov/neo/rest/v1/feed?"
    start_date = date_get("12 nov 2023") #start_date=yyyy-mm-dd&
    end_date = date_get("18 nov 2023")#"end_date=2019-12-10&"
    difference = end_date.date() - start_date.date()
    if difference.days > 7:
        end_date = start_date + datetime.timedelta(days=7)
        print ("End date selected is greater than 7 days, the system will use the following date instead " , end_date.date())
    print ("Dates to be used are: ",
           start_date.date(), "and", 
           end_date.date())
    start_date = "start_date="+str(start_date.date())
    end_date = "end_date="+str(end_date.date())+"&"
    api_key = "api_key=FQGOrEgIrGfb2wh23XXshYhOhMwOEueDKEMUzOzE"
    url_constructor = neo_url + start_date + end_date + api_key
    neo_request(url_constructor)

def neo_request(url):
    json_get = requests.get(url).json()
    informant(json_get)

def informant(json_data):
    i = 0
    totalobjects = json_data["element_count"]
    for dates in json_data["near_earth_objects"]:
        date = dates
        for object in json_data["near_earth_objects"][date]:
            if object["is_potentially_hazardous_asteroid"] == True:
                i += 1
                object_name = str(object["name"])
                object_size = object["estimated_diameter"]["meters"]["estimated_diameter_max"]
                object_miss = float(object["close_approach_data"][0]["miss_distance"]["kilometers"])
                object_approach = object["close_approach_data"][0]["close_approach_date_full"]
                object_speed = float(object["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
                object = NEO(object_name,object_size,object_miss,object_approach,object_speed)
                print (f"Here an object that is potentially Hazardous {object}")
    print (f"There are {totalobjects} objects near earth")
    print (f"{i} of them are Hazardous to earth")

if __name__ == '__main__':
    url_generator()