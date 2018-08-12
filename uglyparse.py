import sys

# Change this for the computer's preference
preference = "sunflowers"

out_f = sys.argv[1]
# keys: class names values: scores
scores = {}
with open(out_f, "r") as f:
    for l in f:
        if "score" in l:
            s = float(l.split("=")[1][:-2])
            c = l.split("=")[0].split(" ")[0]
            scores[c] = s

pref_score = scores[preference]
for c, s in scores.items():
    if c == preference:
        continue
    if s > pref_score:
        print("Swipe left!")
        exit(0)
print("Swipe right!")
        
        
        

    
