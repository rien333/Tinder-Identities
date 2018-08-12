#!/usr/bin/env fish

while true
    python screenshot.py
    python -m scripts.label_image --graph=tf_files/retrained_graph.pb --image=/tmp/tinder_screenshot.png
end
