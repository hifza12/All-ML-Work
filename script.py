import cv2
import pytesseract
import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt

img = cv2.imread('/home/hifza/Pictures/PassportOCR/static/uploads/passport.png',0)
img_copy = img.copy()
img_canny = cv2.Canny(img_copy, 50, 100, apertureSize = 3)
#plt.imshow(img)
#plt.imshow(img_canny)
img_hough = cv2.HoughLinesP(img_canny, 1, math.pi / 180, 100, minLineLength = 100, maxLineGap = 10)
(x, y, w, h) = (np.amin(img_hough, axis = 0)[0,0], np.amin(img_hough, axis = 0)[0,1], np.amax(img_hough, axis = 0)[0,0] - np.amin(img_hough, axis = 0)[0,0], np.amax(img_hough, axis = 0)[0,1] - np.amin(img_hough, axis = 0)[0,1])
img_roi = img_copy[y:y+h,x:x+w]
#plt.imshow(img_roi)

#img_roi = cv2.rotate(img_roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
(height, width) = img_roi.shape
img_roi_copy = img_roi.copy()
dim_mrz = (x, y, w, h) =(1, round(height*0.75), width-2, round(height-(height*0.75))-2)
img_roi_copy = cv2.rectangle(img_roi_copy, (x, y), (x + w ,y + h),(0,0,0),2)

img_mrz = img_roi[y:y+h, x:x+w]
img_mrz =cv2.GaussianBlur(img_mrz, (3,3), 0)
ret, img_mrz = cv2.threshold(img_mrz,127,255,cv2.THRESH_TOZERO)

#plt.imshow(img_mrz)

mrz = pytesseract.image_to_string(img_mrz, config = '--psm 12')
print(mrz)

#
# mrz = [line for line in mrz.split('\n') if len(line)>10]
# if mrz[0][0:2] == 'P<':
#   lastname = mrz[0].split('<')[1][3:]
# else:
#   lastname = mrz[0].split('<')[0][5:]
#   firstname = [i for i in mrz[0].split('<') if (i).isspace() == 0 and len(i) > 0][0]
#   pp_no = mrz[1][:9]

#mrz = "P<UTO<<SMITH<<JOHN<<<<<<<<<<<<<<<<<<<<<<<<<\nL898902C<3UTO6908061F9406236ZE184226B<<<<<10"

# Split the MRZ into lines
lines = mrz.split("\n")

# Extract the last name from the first line
last_name_line = lines[0]
if mrz[0][0:2] == 'P<':
    last_name_line = mrz[0].split('<')[1][3:]
# last_name_parts = last_name_line.split("<<")
# last_name = last_name_parts[0][1]

# Extract the first name from the first line
first_name_line = lines[0]
first_name_parts = first_name_line.split("<<")
first_name = first_name_parts[0][2]

# Extract the passport number from the second line
passport_number = lines[1][:9]

print(first_name)    # prints "JOHN"
print(last_name_line)     # prints "SMITH"
print(passport_number)  # prints "L898902C3"


# result = {"first name ": firstname,
#           "lastname": lastname,
#           "passport": pp_no}
#
# print(result)

