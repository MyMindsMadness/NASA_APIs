# NASA_APIs

These are scripts utilizing the NASA APIs and a Webex notification bot. 

---USE---
Create a virtual environment
# python3 -m venv MYVENV

Create a .env file to store your environment variables. 
# touch MYVENV/env.env 

Use the TemplateEnv.env and generate your 
 - Webex room id = https://developer.webex.com/docs/api/v1/rooms/get-room-details 
 - Webex BOT token = https://developer.webex.com/docs/bots 
 - Nasa API Token = https://api.nasa.gov/

With these completed, scripts will run an post cards to webex. 

DailyPicture, if ran daily will provide the daily APOD picture as a Webex card by a Webex bot.
NEOs, will assess any hazardous near earth objects from today for the next 7 days. a Webex card will be created for each object.
