# Last Updated:	4/30/13

Description:
I used OpenCV for all image operations, and Tesseract as my character recognizer. First an image is taken from my webcam. It is then blurred to remove noise, and run through a Sobel edge detection filter. This will draw colored lines on edges in the image, based on what the colors between the original edge were. Since Massachusetts has red characters on a white background, the edges will show up teal after being run through the Sobel filter, as you can see from the example image in the repo. The image is then thresholded for just this teal color to a binary image and we then find where the characters of the license plate are in the image. A circle is drawn in the center of the license plate, and a rectangle is draw at a specific size with the circle in it's center. The image inside this rectangle is then cropped from the image, converted to greyscale, and sent through the Tesseract Optical Character Recognition engine. Tesseract then attempts to read the characters on the license plate and outputs what it thinks to the command line. 

Although the character recognition is pretty inaccurate right now, I believe it can be improved greatly. Right now, my program draws a specific sized rectangle around where it thinks the license plate is instead of drawing one around just where the characters are. This is why it is very inaccurate at most distances. However, there is a small range of distances that the license plate can be away from the camera for it to work pretty well. If work is continued on this project, I would rewrite the locator module and use contour lines to find the specific size and orientation of the license plate. This way, when the image is cropped and sent through Tesseract, it should be much more accurate.

How to use:
1. Install the necessary libraries. (I used MacPorts to simplify this process, and this website gives detailed instructions on how to link the libraries together on Mac OS X 10.8.x: http://code.google.com/p/python-tesseract/wiki/HowToCompilePythonTesseractForMacMountainLion)
2. Navigate to the directory and simply type: "python LicensePlateRecognition.py"
3. A window should pop up with your laptop's web cam feed and being tracking Massachusetts license plates.

Libraries:
1. OpenCV with Python extensions: www.opencv.org
2. Tesseract-OCR: http://code.google.com/p/tesseract-ocr/
3. Python-Tesseract wrappers: http://code.google.com/p/python-tesseract/

Notes:
Newer versions of the OpenCV library may not be compatible with Tesseract and it's libraries. Since updating to newer versions of OpenCV, I have not been able to get it to run without weird errors with Tesseract and it's python wrappers, although I haven't tried updating all three to their latest versions, which may work. However, there is a demo video I made proving that the source code does in fact work.

More info can be found at the project webpage: http://cs.clarku.edu/~tboraski/cs201/project/
