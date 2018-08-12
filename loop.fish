#!/usr/bin/env fish

while true
    python screenshot.py
    python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=/tmp/tinder_screenshot.png > /tmp/tinder_scores.txt
    python uglyparse.py /tmp/tinder_scores.txt
end
