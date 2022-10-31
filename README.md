# EyeFollowingFace
Using Arduino and Oled Display to show an image of eye that follow face movement

I'm using eksternal webcam to capture the image and proccesing it in Python program on my Computer, then send the X&Y coordination to Arduino and display it on 0.96" OLED display

The X&Y coordinates is base on the center of face, then I map it to fit on the 0.96" display resolution (128x64 Pixel)

Simple Diagram:

![a](https://user-images.githubusercontent.com/105662575/199051556-91f63255-1d8a-456e-96d1-ceed8a75d34f.jpg)
