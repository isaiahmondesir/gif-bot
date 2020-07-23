# -*- coding: utf-8 -*-
"""
**This program was written live on Twitch.tv/IsaiahMonday**

Name: gif-bot.py
Author(s): isaiahmonday, Cuken, Spensarrr, thelopster

"""
import twitch
import requests
import json
import pdb
import wget
import os
import time
import urllib
import random
from googletrans import Translator

from flask import Flask
app = Flask(__name__)

apikey = "VGS81FE9IW0B"  # test value
lmt = 1
url = "https://streamlabs.com/api/v1.0/alerts"
gif_url = ""
chat_message = ""
translated_message = ""

# The purpose of this function is to read through twitch chat messages and initiate
# the gif search upon the entry of '!gif <phrase>'. Interacts witht the Tenor GIF 
# API to pick a related gif.
def handle_message(message: twitch.chat.Message) -> None:
    global gif_url
    global chat_message
    global translated_message
    if message.text.startswith('!gif'):
        identifier = message.text[5:]
        querystring = { "response_type":"access_token",
                        "client_id":"y1e3BGmc2GTdT3mYNlLrp1LPIzqdtMt8Yk1lANK2",
                        "redirect_uri":"https://twitchapps.com/tmi/#access_token=40chvcdsjbfcc94nqdwkra0qb1d06o",
                        "scope":"chat/read chat/edit channel/moderate whispers/read"}
        response = requests.request("GET", url, params=querystring)
        
        if len(identifier) > 0:
            r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (identifier, apikey, lmt))
            #print(json.loads(r.content))
            gif_url = json.loads(r.content)["results"][0]["media"][0]["gif"]["url"]

            #wget.download(gif_url)
    
    #50/50
    elif message.text.startswith('!5050'):
        #Advice
        if(random.randint(1,2) == 1):
            slip = urllib.request.urlopen('https://api.adviceslip.com/advice')
            for line in slip:
                chat_message = json.loads(line)['slip']['advice']
                break
        
        #Insult
        else:
            slip = urllib.request.urlopen('https://evilinsult.com/generate_insult.php?lang=en&type=text')
            for line in slip:
                chat_message = line.decode('utf-8')
                break

        message.chat.send('@{}, {}'.format(message.sender, chat_message))
    
    #Translate
    elif message.text.startswith('!translate'):
        translator = Translator()
        untranslated_message = message.text[11:]
        # raw_message = message.text[:10].split(' ')
        # no dest lang set
        # untranslated_message.join(raw_message[1:])
        translated_message = translator.translate(untranslated_message).text
        message.chat.send('@{} says: {}'.format(message.sender, translated_message))

        
    return

# This is for the Flask server that is holding the latest image on its site.
# On SLOBS/OBS, Browser source should be set to 'http://localhost:5000/'
@app.route('/')
def index():
    return '<img src={} alt=MyAwesomeGif>'.format(gif_url)

# This is for the Flask server that is holding the latest image on its site.
# On SLOBS/OBS, Browser source should be set to 'http://localhost:5000/'
def main():
    # pdb.set_trace()
    chat = twitch.Chat(channel='isaiahmonday', # adjust this for your channel name
                       nickname='bot',
                       
                       # awd contains an oauth key which is not shared publicly. Create your own awd.txt file
                       oauth=open("awd.txt").read(),

                       # adjust this for your client ID
                       helix=twitch.Helix(client_id='lmpf9a1btnphwvvy879gqly1voc4ak', use_cache=True)) 

    chat.subscribe(handle_message)
    app.run()

if __name__ == '__main__':
    main()
