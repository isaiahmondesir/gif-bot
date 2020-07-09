# Example
# Use Helix to retrieve user objects from live chat messages

import twitch
import requests
import json
import pdb


apikey = "VGS81FE9IW0B"  # test value
lmt = 1
url = "https://streamlabs.com/api/v1.0/alerts"

# add timeout, (?)multithreading, no spam
def handle_message(message: twitch.chat.Message) -> None:
    if message.text.startswith('!gif'):
        #pdb.set_trace()
        identifier = message.text[5:]
        if len(identifier) > 0:
        # # message.chat.send(f'@{message.user().display_name}, you have {message.user().view_count} views.')
            r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (identifier, apikey, lmt))
            message.chat.send(json.loads(r.content)["results"][0]["url"])
            querystring = {
                "type":"gif",
                "image_href":json.loads(r.content)["results"][0]["url"],
                "sound_href":"https://www.randomwebsite.com/honksound.wav",
                "message":"Here's a gif",
                "duration":"3000",
                "special_text_color":"Orange",
                "access_token": "hi"
            }

            print(open("accesstoken.txt", 'r').readline())
            response = requests.request("POST", url, params=querystring)
            print(response.text)
            return
        # message.chat.send('hi')
def main():
    # pdb.set_trace()
    chat = twitch.Chat(channel='isaiahmonday',
                       nickname='bot',
                       oauth=open("awd.txt").read(),
                       helix=twitch.Helix(client_id='lmpf9a1btnphwvvy879gqly1voc4ak', use_cache=True))

    chat.subscribe(handle_message)


if __name__ == '__main__':
    main()