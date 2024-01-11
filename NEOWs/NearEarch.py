#!/home/mccube/PersonalProjects/NASA_API/NASAenv/bin/python3

import requests 
import datetime 
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import copy

my_dotenv_path = Path('NASAenv/env.env')
load_dotenv(dotenv_path=my_dotenv_path)

webexurl = os.getenv("WEBEX_URL")
webexbot = os.getenv("WEBEX_BEARER")
webexroomid = os.getenv("WEBEX_ROOM_ID")
nasaapodurl = os.getenv("NASA_NEO_BASE_URL")
nasaapi = os.getenv("NASA_API_KEY")

#class NEO(object):
#    name = ""
#    size = 0.0
#    miss = 0.0
#    approach = 0.0
#    speed = 0.0
#    def __init__(self, name, size, miss, approach, speed):
#        self.name = name
#        self.size = size
#        self.miss = miss
#        self.approach = approach
#        self.speed = speed
#    def __str__(self):
#        return f"{self.name}"

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
    total_haz = 0
    totalobjects = json_data["element_count"]
    hazard_objects = []
    for dates in json_data["near_earth_objects"]:
        date = dates
        for object in json_data["near_earth_objects"][date]:
            if object["is_potentially_hazardous_asteroid"] == True:
                hazard_object = []
                total_haz += 1
                object_name = str(object["name"])
                object_date = date
                object_miss = float(object["close_approach_data"][0]["miss_distance"]["kilometers"]) /1000000
                size_in_suns = object_miss / 1.4
                object_miss = str(round(size_in_suns, 2))
                hazard_object.append(object_name)
                hazard_object.append(object_date)
                hazard_object.append(object_miss)

                hazard_objects.append(hazard_object)
    card_builder(hazard_objects, totalobjects, total_haz)

def card_builder(object_details, tot_objects, tot_hazards):
    #open the card.json file
    with open ('NEOWs/neo_card.json') as f: 
        json_data = json.load(f)
    json_data["body"][1]["columns"][1]["items"][0]["text"] = str(tot_objects)
    json_data["body"][2]["columns"][1]["items"][0]["text"] = str(tot_hazards)

    with open('NEOWs/columnset_builder.json') as g:
        columnset_template= json.load(g)
    for object in object_details:
        columnsetdata = copy.deepcopy(columnset_template)
        columnsetdata["columns"][0]["items"][0]["text"] = object[0]
        columnsetdata["columns"][1]["items"][0]["text"] = object[1]
        columnsetdata["columns"][2]["items"][0]["text"] = object[2]
        print (f"The data to be added is \n{columnsetdata}\n")
        json_data["body"].append(columnsetdata)
#    for object in object_details:
#        print (object)
#        temp_csd["columns"][0]["items"][0]["text"] = object[0]
#        temp_csd["columns"][1]["items"][0]["text"] = object[1]
#        temp_csd["columns"][2]["items"][0]["text"] = object[2]
#        json_data["body"].append(temp_csd)
#    print(json_data)

    #pretty_print = json.dumps(json_data)
    #pretty_print = json.dumps(json.loads(pretty_print), indent=2)
    #print (pretty_print)
    #for object in object_details:

    url = webexurl   
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
        "text": "NEOW",
        "attachments": attachment
    }
    #Headers required to post to Webex room using Bot Auth Key defined earlier.
    headers = {
        "Authorization": "Bearer " + bearer,
        "Content-Type": "application/json"
    }
    #The POST action to webex room taking the ciscospark url defined at top of def,
    #the payload, and headers.
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    URL = url_generator()
    get_data = neo_request(URL)
    informant(get_data)
    