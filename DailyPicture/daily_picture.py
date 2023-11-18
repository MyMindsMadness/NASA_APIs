#!/usr/bin/python3

import requests
import json 
from dotenv import load_dotenv
from pathlib import Path
import os

my_dotenv_path = Path('NASAenv/env.env')
load_dotenv(dotenv_path=my_dotenv_path)

webexurl = os.getenv("WEBEX_URL")
webexbot = os.getenv("WEBEX_BEARER")
webexroomid = os.getenv("WEBEX_ROOM_ID")
nasaapodurl = os.getenv("NASE_APOD_BASE_URL")
nasaapi = os.getenv("NASA_API_KEY")

#This function modifies the values that are needed for the webex card
def sendWebex(title, desc, imurl, owner):    
    url = webexurl
    
    #open the card.json file
    with open ('DailyPicture/card.json') as f: 
        json_data = json.load(f)

    #If the daily picture is actually a youtube video, no image will be displayed.
    #As a result the if/else statement provides a default "image unavailable" image
    #if imurl is not a youtube link. proceed as normal.
    if "https://www.youtube.com/" not in imurl:
        json_data["body"][1]["url"] = imurl
    #else if imurl is a youtube link, replace image with a stand in
    else:    
        json_data["body"][1]["url"] = "https://github.com/MyMindsMadness/NASA_API_Projects/blob/main/Unavailable.png?raw=true"
        
    
    #Update Card decription field with the "explanation" information from the API get request.
    json_data["body"][3]["text"] = desc
    #Update Card by field with the "copyright" information from the API get request.
    json_data["body"][2]["columns"][1]["items"][1]["text"] = owner
    #Update Card Title field with the "Title" information from the API get request.
    json_data["body"][2]["columns"][1]["items"][0]["text"] = title
    #This builds the card information as an attachment.
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
        "text": title,
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

#Main Call to NASA Asto Picture of the Day (APOD)
def main():
    #APOD url
    url = nasaapodurl
    #Auth key provided to you by NASA
    api_key = nasaapi
    #Combine the URL and API key 
    full_api = url+api_key
    #Issue the API GET reguest
    json_get = requests.get(full_api).json()
    #Define image, Title, Description,URL and Owner
    img_title = json_get['title']
    img_desc = json_get['explanation']
    img_URL = json_get['url']    
    if "copyright" not in json_get:
        img_owner = "None"
    else:
        img_owner = json_get['copyright']
    #Send above information to the webex card creator function
    sendWebex(img_title, img_desc, img_URL, img_owner)



if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()