#!/usr/bin/env fish

while true
    python screenshot.py
    python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=/tmp/tinder_screenshot.png > /tmp/tinder_scores.txt
    python uglyparse.py /tmp/tinder_scores.txt
    # sometimes randomly sleep
    if random 0 1 | grep 1 > /dev/null
        sleep random 0 3
    end
end
