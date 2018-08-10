import pynder
import os
import argparse # TODO: nice args
# If you're gonna swipe, also sleep at random times during swipes (1-5 secs.)


# 🐝🐝🐝🐝🐝🐝 MAKE SURE AUTH OF BROWSER AND APP ARE THE SAME!
# 🐝🐝🐝🐝🐝🐝 see https://gist.github.com/taseppa/66fc7239c66ef285ecb28b400b556938?

f = os.path.expanduser("~/.config/tinder_bot/conf")
token = None
fb_id = None
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

if None in [fb_id, token]:
    print("Invalid configuration file. 😕")
    exit(0)



# need those named keywords
session = pynder.Session(facebook_id=fb_id, facebook_token=token)
users = session.nearby_users() # returns a iterable of users nearby
idx = 5

for u in users:
    print(u.name)
    idx -= 1
    if idx < 1:
        break
