from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import pytesseract
import pandas as pd
import numpy as np
import math
import  logging

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        f=file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_path=os.path.join('static/uploads', secure_filename(filename))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
      #  return render_template('index.html', filename=filename)
    # else:
    #     flash('Allowed image types are - png, jpg, jpeg, gif')
        #return redirect(request.url)
        # import pdb
        # pdb.set_trace()
        img = cv2.imread(file_path)
        #img_copy = img.copy()
        #img_copy = img.copy()
        img_canny = cv2.Canny(img, 50, 100, apertureSize=3)
        # plt.imshow(img)
        # plt.imshow(img_canny)
        img_hough = cv2.HoughLinesP(img_canny, 1, math.pi / 180, 100, minLineLength=100, maxLineGap=10)
        (x, y, w, h) = (np.amin(img_hough, axis=0)[0, 0], np.amin(img_hough, axis=0)[0, 1],
                        np.amax(img_hough, axis=0)[0, 0] - np.amin(img_hough, axis=0)[0, 0],
                        np.amax(img_hough, axis=0)[0, 1] - np.amin(img_hough, axis=0)[0, 1])
        img_roi = img[y:y + h, x:x + w]
        # plt.imshow(img_roi)

        #img_roi = cv2.rotate(img_roi, cv2.ROTATE_90_COUNTERCLOCKWISE)
        (height, width,_) = img_roi.shape
        #(height, width) = img_roi.shape
        img_roi_copy = img_roi.copy()
        dim_mrz = (x, y, w, h) = (1, round(height * 0.75), width - 2, round(height - (height * 0.75)) - 2)
        img_roi_copy = cv2.rectangle(img_roi_copy, (x, y), (x + w, y + h), (0, 0, 0), 2)

        img_mrz = img_roi[y:y + h, x:x + w]
        img_mrz = cv2.GaussianBlur(img_mrz, (3, 3), 0)
        ret, img_mrz = cv2.threshold(img_mrz, 127, 255, cv2.THRESH_TOZERO)

        # plt.imshow(img_mrz)

        mrz = pytesseract.image_to_string(img_mrz, config='--psm 12')
        print(mrz)
       #  import  pdb
       # #  pdb.set_trace()

    mrz = [line for line in mrz.split('\n') if len(line) > 10]
    if mrz[0][0:2] == 'P<':
        lastname = mrz[0].split('<')[1][3:]
    else:
        lastname = mrz[0].split('<')[0][5:]
    f= mrz[0].split('<')[1][1:12]
    f2=f.replace(" ","")
    firstname=f2.replace("C", " ")
    #firstname = [i for i in mrz[0].split('<') if (i).isspace() == 0 and len(i) > 0][1]
    pp_no = mrz[1][:11]
    passport=pp_no.replace(" ","")
    p=passport.replace("1.","L")

    result = " first name =  " + firstname + "  , " + " last name = " + lastname + " , " + " passport = "+ p


    


    return render_template('index.html', filename=filename,result=result)
    # else:
    #     flash('Allowed image types are - png, jpg, jpeg, gif')
    #     return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(debug=True)