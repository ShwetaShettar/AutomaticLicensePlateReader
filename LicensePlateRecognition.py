# /opt/local/bin/python2
# MacPorts Python 2.7.3
##################################################
# Name:			Tyler Boraski
# Date:			12/11/12
# Class:		CS201
# Assignment:	Final Project - License Plate Recognition
##################################################

# Import libraries
import time
import sys
import copy
import ctypes
import os
import re

# Import OpenCV
import cv

# Import Tesseract
import tesseract

# OpenCV variables
cv.NamedWindow("CS201 - Tyler Boraski - Final Project", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)

    
##################################################
# Name:         colorEdgeDetector()
# Description:  Finds a license plate template based
#               on edge color.
##################################################
def colorEdgeDetector():
    # Declare as globals since we are assigning to them now
    global capture
    global capture_index
    
    # Declare tesseract variables
    api = tesseract.TessBaseAPI()
    api.Init(".","eng",tesseract.OEM_DEFAULT)
    api.SetPageSegMode(tesseract.PSM_SINGLE_LINE)
    
    # Variable to control size of peeking window
    xDiff = 120.0
    yDiff = 40.0
    rectArea = int(xDiff*2) * int(yDiff*2)
    
    # Capture current frame
    frame = cv.QueryFrame(capture)
    
    # Declare other variables used to manipulate the frame
    threshold_frame = cv.CreateImage(cv.GetSize(frame), 8, 1)
    hsv_frame = cv.CreateImage(cv.GetSize(frame), 8, 3)
    
    while True:
        # Copy the original frame to display later
        original_frame = cv.CloneImage(frame)
        
        # Use Sobel filter to detect edges
        cv.Smooth(frame, frame, cv.CV_BLUR, 3, 3)
        cv.Sobel(frame, frame, 2, 0, 5)
        cv.Smooth(frame, frame, cv.CV_BLUR, 3, 3)
        
        # Convert frame to HSV
        cv.CvtColor(frame, hsv_frame, cv.CV_BGR2HSV)
        
        # Remove all pixels that aren't a teal color: RGB(0, 180, 170) HSV(170, 75, 100)
        cv.InRangeS(hsv_frame, (70, 150, 150), (100, 255, 255), threshold_frame)
        
        
        # Get moments to see if what was found is a license plate or not
        moments = cv.Moments(cv.GetMat(threshold_frame, 1), 0) 
        area = cv.GetCentralMoment(moments, 0, 0)     
        if(area > 60000): 
            # Determine the x and y coordinates of the center of the object 
            x = cv.GetSpatialMoment(moments, 1, 0)/area 
            y = cv.GetSpatialMoment(moments, 0, 1)/area 
            
            # Retrieve candidate license plate and test it's characters
            if int(x-xDiff) > 0 and int(y-yDiff) > 0 and (int(x-xDiff) + int(xDiff*2)) < 640 and (int(y-yDiff) + int(yDiff*2)) < 480:
                candidate = cv.GetSubRect(original_frame, (int(x-xDiff), int(y-yDiff), int(xDiff*2), int(yDiff*2)))
                candidateImg = cv.CreateImage(cv.GetSize(candidate), 8, 3)
                cv.Convert(candidate, candidateImg)
                candidateGrey = cv.CreateImage(cv.GetSize(candidate), 8, 1)  
                cv.CvtColor(candidateImg, candidateGrey, cv.CV_RGB2GRAY)
                tesseract.SetCvImage(candidateImg, api)
                text = api.GetUTF8Text()
                print "License Plate Characters:",text
                
                """
                # Regex and this don't seem to work
                if text.isalnum(): 
                    print "License Plate Characters:",text
                """
            
            # Draw circle on center of object
            cv.Circle(original_frame, (int(x), int(y)), 2, (255, 255, 255), 10)
            
            # Rectangle
            cv.Rectangle(original_frame, (int(x-xDiff),int(y-yDiff)), (int(x+xDiff),int(y+yDiff)), cv.CV_RGB(0,0,255), 1)
        
        # Display image
        cv.ShowImage("CS201 - Tyler Boraski - Final Project", original_frame)
        
        # Capture new frame
        frame = cv.QueryFrame(capture)
        
        # If wrong camera index is initialized, press "n" to cycle through camera indexes.
        c = cv.WaitKey(10)
        if c == "n": 						
            camera_index += 1 				# Try the next camera index
            capture = cv.CaptureFromCAM(camera_index)
            if not capture: 				# If the next camera index didn't work, reset to 0.
                camera_index = 0
                capture = cv.CaptureFromCAM(camera_index)
        
        # If "esc" is pressed the program will end
        esc = cv.WaitKey(7) % 0x100
        if esc == 27:
            quit()

##################################################
# Main functions of the program. It's just a wrapper 
# for colorEdgeDetector().
##################################################    
if  __name__ =='__main__':
    # Connected Components
    colorEdgeDetector()