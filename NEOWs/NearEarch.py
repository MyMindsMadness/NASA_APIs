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

apikey = os.getenv('NASA_API_KEY')

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
#
#def url_generator():
#    neo_url = os.getenv('NASA_BASE_URL')
#    start_date = datetime.datetime.today().strftime('%Y-%m-%d')
#    end_date = datetime.datetime.now() + datetime.timedelta(days=1)
#    end_date = end_date.date()
#    print ("Dates to be used are: ",
#           start_date, "and", 
#           end_date)
#    start_date = "start_date="+str(start_date)
#    end_date = "end_date="+str(end_date)+"&"
#    api_key = apikey
#    url_constructor = neo_url + start_date + end_date + api_key
#    return url_constructor
#
#def neo_request(url):
#    json_get = requests.get(url).json()
#    return json_get
#
#def informant(json_data):
#    i = 0
#    totalobjects = json_data["element_count"]
#    for dates in json_data["near_earth_objects"]:
#        date = dates
#        for object in json_data["near_earth_objects"][date]:
#            if object["is_potentially_hazardous_asteroid"] == True:
#                i += 0
#                object_name = str(object["name"])
#                object_size = object["estimated_diameter"]["meters"]["estimated_diameter_max"]
#                object_miss = float(object["close_approach_data"][0]["miss_distance"]["kilometers"])
#                object_approach = object["close_approach_data"][0]["close_approach_date_full"]
#                object_speed = float(object["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
#                object = NEO(object_name,object_size,object_miss,object_approach,object_speed)
#                print (object)
#                #print (f"Here an object that is potentially Hazardous {object}")
#    #print (f"There are {totalobjects} objects near earth")
#    #print (f"{i} of them are Hazardous to earth")

def card_builder():
    #open the card.json file
    with open ('NEOWs/neo_card.json') as f: 
        json_data = json.load(f)
    
    #Update Card decription field with the "explanation" information from the API get request.
    print (json_data["body"][0]["columns"][1]["items"][1]["text"]) #name
    print (json_data["body"][1]["columns"][1]["items"][0]["text"]) #date
    print (json_data["body"][1]["columns"][1]["items"][1]["text"]) #size
    print (json_data["body"][1]["columns"][1]["items"][2]["text"]) #sizelike
    print (json_data["body"][1]["columns"][1]["items"][3]["text"]) #magentude
    print (json_data["body"][1]["columns"][1]["items"][4]["text"]) #magentudelike
    print (json_data["body"][1]["columns"][1]["items"][5]["text"]) #speed
    print (json_data["body"][1]["columns"][1]["items"][6]["text"]) #speed like

#    #Update Card by field with the "copyright" information from the API get request.
#    json_data["body"][2]["columns"][1]["items"][1]["text"] = owner
#    #Update Card Title field with the "Title" information from the API get request.
#    json_data["body"][2]["columns"][1]["items"][0]["text"] = title
#    #This builds the card information as an attachment.
#    attachment = {
#        "contentType": "application/vnd.microsoft.card.adaptive",
#        "content": json_data
#    }
#
#def PostToWebex():    
#    webexurl = "https://api.ciscospark.com/v1/messages"
#    
#    #Auth Key to post via bot to webex.
#    bearer = os.getenv("WEBEX_BEARER")
#    #Room ID for the webex room you wish to post in
#    room_id = os.getenv("WEBEX_ROOM_ID")
#    #Payload to including the room id, its title and the attachment defined earlier.
#    payload = {
#        "roomId": room_id,
#        "text": title,
#        "attachments": attachment
#    }
#    #Headers required to post to Webex room using Bot Auth Key defined earlier.
#    headers = {
#        "Authorization": "Bearer " + bearer,
#        "Content-Type": "application/json"
#    }
#    #The POST action to webex room taking the ciscospark url defined at top of def,
#    #the payload, and headers.
#    reponse = requests.post(webexurl, json=payload, headers=headers)

#if __name__ == '__main__':
#    URL = url_generator()
#    get_data = neo_request(URL)
#    informant(get_data)

card_builder()