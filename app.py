import random
import os
import datetime
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    image_url = date_selector()
                    bot.send_image_url(recipient_id, image_url)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message():
    response = "Well, something isn't working"
    # return selected item to the user
    return response

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

#determines which image to send based on day
def date_selector():
    day = datetime.datetime.today().weekday()
    day_to_url = {
        0: "https://i.kym-cdn.com/photos/images/original/001/094/502/ac2.png",
        1: "https://i.kym-cdn.com/photos/images/facebook/001/094/500/b1f.png",
        2: "https://i.imgur.com/n7I7cKp.jpg",
        3: "https://i.kym-cdn.com/photos/images/original/001/091/402/9d6.jpg",
        4: "https://pics.me.me/it-is-friday-my-lads-me-irl-21746454.png",
        5: "https://i.redd.it/xx24ryi1zl501.jpg",
        6: "https://i.imgur.com/RogyXPP.jpg"
    }
    return day_to_url.get(day, "https://i.imgur.com/n7I7cKp.jpg")


if __name__ == "__main__":
    app.run()
