import os
import time
from slackclient import SlackClient
from random import randint

#Starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
#U44PLAXD5 

#Instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
#xoxb-140802371447-ZBv5ZaefXqZoMHVtU87O6TWm

#constants
AT_BOT = "<@" + BOT_ID + ">" 
EXAMPLE_COMMAND = "do"

TROLL = "favourite"
FAV_GAME = "League of Legends"

GAME_IDENTIFIER = "play"
START = "go"
END = "bye"

#command = "/anon" + str(command)

a = ["Describe last night.", 
            "I love you.", 
            "I hate you.", 
            "Im tired.", 
            "Merry Christmas!", 
            "Oh my God.", 
            "Tell me about yourself.", 
            "My grandma died.", 
            "I feel empty inside.", 
            "Lets make a child.", 
            "HELP! HELP! HELP!", 
            "Good Morning :)", 
            "Can you send me the answers to the calc assignment?," 
            "How was the interview?", 
            "How was the physics exam?", 
            "Are you busy this weekend?", 
            "Yo! Where you at?", 
            "What should I make for dinner?", 
            "What do you want to do when you get home?", 
            "Do you want to hang out?", 
            "How was your date?", 
            "Why are you single?",
            "What are you wearing right now?", 
            "What is your opinion on euthanasia?", 
            "Can I get a ride?", 
            "How was your day?"]

b = ["Most Narrative Answer",
     "Most Hilarious Answer",
     "Most Inappropriate Answer",
     "Most Accurate Answer",
     "Most Creative Answer",
     "Personal Favourite"]

#Receives commands directed at the bot, determines valid commands. 
#If so, then acts on the commands
#If not, returns back what it needs for clarification.
def handle_command(command, channel):
    #==== FUNCTIONALITY ====#
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure... write some more code then I can do that!"
        slackPrint(response)

    elif command == "hi" or command == "hello" or command == "hey":
        slackPrint("Hey there!")

    #==== RANDOM COMMANDS ===#
    elif TROLL in command:
        response = "My favourite game is " + FAV_GAME +"."
        slackPrint(response)

    #==== MAIN GAME METHOD ====#
    elif GAME_IDENTIFIER in command:
        #suspend = True 
        response = "Okay, let's go!\n\n" + \
                    "Welcome to Emoji Blitz:\n" + \
                    "I'm going to give you a series of questions, statements, and prompts - \n" + \
                    "Your job is to respond with your choice of message, as best as you can :)\n\n" + \
                    "Score the best response according to the round rule amongst player, by reacting with emojis. \n" + \
                    "Here are some *rules*: \n" + \
                    " - 30 sec answers\n" + \
                    " - Emojis\n" + \
                    " - Short language\n" +\
		    "Here are some additional round rules to guide voting:\n" + \
                    " 1. Most Narritive Answer\n" + \
                    " 2. Most Hilarious Answer\n" +\
		    " 3. Most Inappropriate Answer\n" +\
		    " 4. Most Accurate Answer\n" +\
		    " 5. Most Creative Answer\n" +\
		    " 6. Personal Favourite\n" +\
                    "Ready to go?"

        slackPrint(response)

        '''
        while suspend == True:
            if command == "yes":
                response = "kk fam"
                slackPrint(response)
                suspend = False
                #put in randomly generated prompts
            elif command == "no":
                response == "alright then"
                slackPrint(response) 
                suspend = False
        '''

    elif START in command:
        #put in randomly generated prompts
        #= array of prompts, questions
        #= randomly generated selection and print
        #= give 15 seconds to answer
        #= collect responses, print 
        #= let users vote
        #= command next 
        #= repeat
        slackPrint(a[randint(0,len(a)-1)])
        slackPrint("Round Rule: " + b[randint(0,len(b)-1)])
        time.sleep(30)
        slackPrint("Please vote!")
    elif END in command:
        slackPrint("Thanks for playing! Bye.")

    else:
        response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
        "* command with numbers, delimited by spaces."
        slackPrint(response)


def slackPrint(call):
    slack_client.api_call("chat.postMessage", channel=channel, text=call, as_user=True)


def parse_slack_output(slack_rtm_output):
    #The Slack Real Time Messaging API is an events firehose.
    #Parsing function returns None unless a message is directed at the Bot, based on ID.

    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Mattbott connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
