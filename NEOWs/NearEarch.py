#!/home/mccube/PersonalProjects/NASA_API/NASAenv/bin/python3

# Import dependancies #
import requests 
import datetime 
import json
from dotenv import load_dotenv
from pathlib import Path
import os
import copy

#Set path to enviroment variables
my_dotenv_path = Path('NASAenv/env.env')
load_dotenv(dotenv_path=my_dotenv_path)

# set enviroment variables as code variables
webexurl = os.getenv("WEBEX_URL")
webexbot = os.getenv("WEBEX_BEARER")
webexroomid = os.getenv("WEBEX_ROOM_ID")
nasaneourl = os.getenv("NASA_NEO_BASE_URL")
nasaapi = os.getenv("NASA_API_KEY")

def url_generator():
    #pull the base url
    neo_url = nasaneourl
    #generate dates
    start_date = datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = datetime.datetime.now() + datetime.timedelta(days=1)
    end_date = end_date.date()
    start_date = "start_date="+str(start_date)
    end_date = "end_date="+str(end_date)+"&"
    #pull personal nasa api key
    api_key = nasaapi
    #construct url from all above
    url_constructor = neo_url + start_date + end_date + api_key
    return url_constructor

def neo_request(url):
    json_get = requests.get(url).json()
    return json_get

def informant(json_data):
    #set hazards to 0 
    total_haz = 0
    #pull total amount of object from the retrieved json data
    totalobjects = json_data["element_count"]
    hazard_objects = []
    #for loop that looks for all objects with that 'hazardous' value set to true
    for dates in json_data["near_earth_objects"]:
        date = dates
        for object in json_data["near_earth_objects"][date]:
            if object["is_potentially_hazardous_asteroid"] == True:
                hazard_object = []
                #add to total amount of hazardous objects
                total_haz += 1
                #identify the name of the object
                object_name = str(object["name"])
                #identify the data the object will pass
                object_date = date
                #calculate miss distance and convert it to GigaMeters(Gm)
                object_miss = float(object["close_approach_data"][0]["miss_distance"]["kilometers"]) /1000000
                #the sun is ~1.4Gm in diameter, this will determine how many suns away the object is.
                size_in_suns = object_miss / 1.4
                object_miss = str(round(size_in_suns, 2))
                #appends information to list for passing to card builder
                hazard_object.append(object_name)
                hazard_object.append(object_date)
                hazard_object.append(object_miss)
                hazard_objects.append(hazard_object)
    #pass list of lists, total objects and count of hazards to card builder
    card_builder(hazard_objects, totalobjects, total_haz)

def card_builder(object_details, tot_objects, tot_hazards):
    #open the card.json file
    with open ('NEOWs/neo_card.json') as f: 
        json_data = json.load(f)
    json_data["body"][1]["columns"][1]["items"][0]["text"] = str(tot_objects)
    json_data["body"][2]["columns"][1]["items"][0]["text"] = str(tot_hazards)

    with open('NEOWs/columnset_builder.json') as g:
        #take a copy of the data for a template.
        columnset_template= json.load(g)
    #loop to generate information to be appended to the card.
    for object in object_details:
        #takes a temp copy of the template
        columnsetdata = copy.deepcopy(columnset_template)
        #change desired fields
        columnsetdata["columns"][0]["items"][0]["text"] = object[0]
        columnsetdata["columns"][1]["items"][0]["text"] = object[1]
        columnsetdata["columns"][2]["items"][0]["text"] = object[2]
        #append temp data to the data that will be passed to the card as attachment content
        json_data["body"].append(columnsetdata)
    #set webex url
    url = webexurl
    #pull all information in that is to be used in the card.
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
    