import cv2 #Import openCV
import numpy as np
import time
import sys #import Sys. Sys will be used for reading from the command line. We give Image name parameter with extension when we will run python script

#Read the image. The first Command line argument is the image
image = cv2.imread(sys.argv[1]) #The function to read from an image into OpenCv is imread()
rows,cols,ch = image.shape
for i in range(50):
    cv2.waitKey(200)
    pts1 = np.float32([[6.5+i/10,50],[110+i/10,25],[60+i/10,125]])
    pts2 = np.float32([[5,50],[100,25],[50,125]])
    M = cv2.getAffineTransform(pts1,pts2)
    dst = cv2.warpAffine(image,M,(cols,rows))
    #imshow() is the function that displays the image on the screen.
    #The first value is the title of the window, the second is the image file we have previously read.
    cv2.imshow("OpenCV Image Reading", dst)


cv2.destroyAllWindows()
