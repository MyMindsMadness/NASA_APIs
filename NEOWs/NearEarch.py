#!/home/mccube/PersonalProjects/NASA_API/NASAenv/bin/python

import requests 
import inquirer 
import datetime 
import json
from dotenv import load_dotenv
from pathlib import Path
import os

my_dotenv_path = Path('NASAenv/env.env')
load_dotenv(dotenv_path=my_dotenv_path)

webexurl = os.getenv("WEBEX_URL")
webexbot = os.getenv("WEBEX_BEARER")
webexroomid = os.getenv("WEBEX_ROOM_ID")
nasaapodurl = os.getenv("NASA_NEO_BASE_URL")
nasaapi = os.getenv("NASA_API_KEY")

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

def url_generator():
    neo_url = os.getenv('NASA_NEO_BASE_URL')
    start_date = datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = datetime.datetime.now() + datetime.timedelta(days=1)
    end_date = end_date.date()
    print ("Dates to be used are: ",
           start_date, "and", 
           end_date)
    start_date = "start_date="+str(start_date)
    end_date = "end_date="+str(end_date)+"&"
    api_key = nasaapi
    url_constructor = neo_url + start_date + end_date + api_key
    return url_constructor

def neo_request(url):
    json_get = requests.get(url).json()
    return json_get

def informant(json_data):
    i = 0
    totalobjects = json_data["element_count"]
    for dates in json_data["near_earth_objects"]:
        date = dates
        for object in json_data["near_earth_objects"][date]:
            if object["is_potentially_hazardous_asteroid"] == True:
                i += 1
                object_name = str(object["name"])
                object_date = date
                object_magnitude = str(object["absolute_magnitude_h"])
                object_size = object["estimated_diameter"]["meters"]["estimated_diameter_max"]
                object_miss = float(object["close_approach_data"][0]["miss_distance"]["kilometers"])
                object_approach = object["close_approach_data"][0]["close_approach_date_full"]
                object_speed = float(object["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
                #object = NEO(object_name,object_size,object_miss,object_approach,object_speed)
                card_builder(object_name, object_size, object_miss, object_approach, object_speed, object_magnitude, object_date)
                #print (object)
                #print (f"Here an object that is potentially Hazardous {object}")
    print (f"There are {totalobjects} objects near earth")
    print (f"{i} of them are Hazardous to earth")

def card_builder(name, size, miss, approach, speed, magnitude, date):
    url = webexurl
    #open the card.json file
    with open ('NEOWs/neo_card.json') as f: 
        json_data = json.load(f)
    
    #Update Card decription field with the "explanation" information from the API get request.
    json_data["body"][0]["columns"][1]["items"][1]["text"] = name
    json_data["body"][1]["columns"][1]["items"][0]["text"] = approach
    json_data["body"][1]["columns"][1]["items"][1]["text"] = str(round(size, 2))
    json_data["body"][1]["columns"][1]["items"][2]["text"] = str(round(miss, 2))
    json_data["body"][1]["columns"][1]["items"][3]["text"] = magnitude
    json_data["body"][1]["columns"][1]["items"][4]["text"] = approach
    json_data["body"][1]["columns"][1]["items"][5]["text"] = str(round(speed, 2))
    #json_data["body"][1]["columns"][1]["items"][6]["text"] #speed like
    attachment = {
        "contentType": "application/vnd.microsoft.card.adaptive",
        "content": json_data
    }
    #Auth Key to post via bot to webex.
    bearer = webexbot
    #Room ID for the webex room you wish to post in
    room_id = webexroomid
    #Payload to including the room id, its title and the attachment defined earlier.
    payload = {
        "roomId": room_id,
        "text": name,
        "attachments": attachment
    }
    #Headers required to post to Webex room using Bot Auth Key defined earlier.
    headers = {
        "Authorization": "Bearer " + bearer,
        "Content-Type": "application/json"
    }
    #The POST action to webex room taking the ciscospark url defined at top of def,
    #the payload, and headers.
    requests.post(webexurl, json=payload, headers=headers)

if __name__ == '__main__':
    URL = url_generator()
    get_data = neo_request(URL)
    informant(get_data)
