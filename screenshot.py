import pyscreenshot as ImageGrab

im=ImageGrab.grab(bbox=(10,10,510,510)) # X1,Y1,X2,Y2
# save in folder "tmp"
im.save("/tmp/tinder_screenshot.png")

