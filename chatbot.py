import pynder
import os
import argparse # TODO: nice args
from collections import Counter
from random import choice, random
import argparse
import pickle
from time import sleep
import argparse

# If you're gonna swipe, also sleep at random times during swipes (1-5 secs)!
# 🐝🐝🐝🐝🐝🐝 IDEA: MAKE SURE AUTH OF BROWSER AND APP ARE THE SAME!
# 🐝🐝🐝🐝🐝🐝 see https://gist.github.com/taseppa/66fc7239c66ef285ecb28b400b556938?

# Messages via argparse?
parser = argparse.ArgumentParser(description='Send predefined messages to matches')
parser.add_argument('--conf', "-c", type=str, default="~/.config/tinder_bot/conf", help='Configuration file path')
parser.add_argument('--history', "-f", type=str, default="conversations.pkl",  help='Conversation history file path')
args = parser.parse_args()

# CONVERSATIONS_F = "conversations.pkl"
MSG1 = "Hey %s wil je horen wat mijn algoritme over je zegt?"
MSG2 = 'Mijn algoritme zegt dat jij een "%s" bent. Dit is gebaseerd op je foto omdat %s. We worden steeds vaker beoordeeld door algoritmes op internet. Wil je meer weten? Kom naar mijn event! Check https://waag.org/nl/event/data-dating-hokjesbots'
LAST_MESSAGE = "ok thanks. als je niet wilt dat je data wordt gebruikt laat dan weten in deze chat"
msg_list = [MSG1, MSG2]
zzz = 12 # DEBUGGG 🐝🐝🐝🐝🐝🐝🐝🐝🐝🐝
# limit the people you're messaging
LIMIT = -1

def facebook_conf():
    f = os.path.expanduser(args.conf)
    token = None
    fb_id = None
    preference = None
    if not os.path.exists(f):
        print("No configuration file found. 😕")
        exit(0)

    # get api token and facebook id
    # (https://findmyfbid.com/ and https://github.com/pwntrik/facebook_app_token)
    with open(f, "r") as conf_f:
        for l in conf_f:
            if l.startswith("fb_id"):
                fb_id = l.split(" ")[1]
            elif l.startswith("tinder_token"):
                token = l.split(" ")[1]
            elif l.startswith("preference"):
                preference = l.split(" ")[1].rstrip()
            elif l.startswith("reden"):
                reden = (" ".join(l.split(" ")[1:])).rstrip()

    # note that profiles should have a preference before chatting
    if None in [fb_id, token, preference]:
        print("Invalid configuration file. 😕")
        exit(0)
    return fb_id, token, preference, reden

def matched_users(session):
    match_reader = session.matches()
    matches = []
    while True:
        try:
            matches.append(next(match_reader).user)
        except StopIteration:

            break
        except Exception as e:
            # print(e)
            print("Match retrival error, skipping...")
            continue
    return matches

# load this one with command line conf (So you can have one test user as well)
def conversation_history(users):
    with open(args.history, "rb") as f:
        return pickle.load(f)

def save_conversation_history(conversations):
    # keep a dict of ongoing convos in {USR_ID : MSG_COUNT, ...} format
    with  open(args.history, 'wb') as f:
        pickle.dump(conversations, f)

def chat(conversations, matches):
    # go through all conversations that need to be updated
    try:
        for m in matches:
            send_message(m, conversations[m.id])
            conversations[m.id] += 1
            sleep(2.5 + (random() * 15.5)) # 🐝 don't get caught as a bot, INCREASE?
    except:
        print("saving conf history")
        save_conversation_history(conversations)
        exit(0)
    # return conversations with updates values
    return conversations

def send_message(m, n):
    if n < len(msg_list):
        msg = msg_list[n]
    else:
        # msg = str(LAST_MESSAGE)# could be a list that is just something random
        return
    # get the username from the match object and generate personal message?
    # append it to the message with a format specifier or some shit
    if n == 0:
        msg = msg % (m.user.name)
    print("sending:", msg, "(%s)" % (m.user.name))
    # do a chat
    m.message(msg)
    

# return the right user object from some username
def user_by_id(matches, m_id):
    for m in matches:
        if m.id == m_id:
            return m
    # raise exception/return other random user?
    return None # not sure what would be good to return here

fb_id, token, preference, reden = facebook_conf() # pass in configuration if you want
# need those named keywords
session = pynder.Session(facebook_id=fb_id, facebook_token=token)
# include preference and reden in msg_list
msg_list = msg_list[:1] + [msg_list[1] % (preference, reden)]

# check if previous conversation history exists
# if not, create a new one
if not os.path.isfile(args.history):
    conv_hist = Counter()
    # you can also get a list of matched users but that is less flexible
    # we can't save match objects, so try users?
    for m in list(session.matches()):
        conv_hist[m.id] = 0
    save_conversation_history(conv_hist)

conv_hist = conversation_history(args.history)

while True:
    # retrieve new matches/messages
    matches = list(session.matches()) # safe?
    ids = {m.id for m in matches}
    new_matches = ids - conv_hist.keys()
    unmatched_users = conv_hist.keys() - ids
    # Update conversations
    for u in unmatched_users:
        del conv_hist[u]
    for u in new_matches: # start new history
        conv_hist[u] = 0
    # see which matches left  a reply last ("u have to reply to")
    # ... if the conv history is zero always send a message
    # cases "laaste woord" en n_messages==0 are not the same (so keep this line)
    msg_users = set(user_by_id(matches, m_id) for m_id, cnt in conv_hist.items() if cnt == 0)
    for m in matches:
        if not m.messages:
            continue
        # add names to msg_list
        msg_list2 = [msg_list[0] % m.user.name] + msg_list[1:]
        if conv_hist[m.id] > 0 and not str(m.messages[-1]) in msg_list2:
            msg_users.add(m)
    # print(msg_list2)
    # chat with the found users according to conversation history
    conv_hist = chat(conv_hist, set(list(msg_users)[:LIMIT])) # conv_hist is updated here
    save_conversation_history(conv_hist)
    sleep(zzz+(10*random()))
