import sys
from pynput import keyboard
from pynput.keyboard import Key, Controller
keyboard=Controller()

# Change this for the computer's preference
# Swipe right when one of these preferences is met
preferences = ["sunflowers", "roses", "daisy"]

out_f = sys.argv[1]
# keys: class names values: scores
scores = {}
with open(out_f, "r") as f:
    for l in f:
        if "score" in l:
            s = float(l.split("=")[1][:-2])
            c = l.split("=")[0].split(" ")[0]
            scores[c] = s

pref_scores = [scores[pref] for pref in preferences]
for c, s in scores.items():
    if c in preferences:
        continue # skip
    # check wether a non prefered class scores higher than any of the prefered classes
    if all(s > s1 for s1 in pref_scores):
        print("Swipe left!")
        keyboard.press(Key.left)
        keyboard.release(Key.left)
        exit(0)
print("Swipe right!")
keyboard.press(Key.right)
keyboard.release(Key.right)
