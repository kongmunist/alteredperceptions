#!/bin/bash
echo Starting to compile into ./app...

g++ -std=c++11 -Wall -I/usr/lib/opencv simple_camera.cpp -L/usr/lib -lopencv_core -lopencv_highgui -lopencv_videoio -o app

echo Done! Executing

./app

