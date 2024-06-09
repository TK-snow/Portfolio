from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

import numpy as np
import cv2 as cv
from io import BytesIO
import PIL.Image


class button_control :
    def save_image(self,img_data):
        fileName, _ = QFileDialog.getSaveFileName(
                            self, "Save Image",r"D:/" , "Images (*.png *.jpg *.jpeg)"
                            )

        if fileName:
            with open(fileName, "wb") as f:
                img_data.save(fileName)

class message:
    def alert(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("Alert!")
        msg.setText(message)
 
        x = msg.exec()

    def finish(self,message):
        msg = QMessageBox()
        msg.setWindowTitle("Operation Finsih!")
        msg.setText(message)
 
        x = msg.exec()

class image_frame :
    img_path = ""
    select = False


    def openCVtoPixmap(self,output):
        height, width = output.shape[:2]
        bytesPerLine = 3 * width
        output2 = np.require(output, np.uint8, 'C')
        output = QImage(output2, width, height,bytesPerLine,QImage.Format.Format_RGB888).rgbSwapped()
        img_data = QPixmap(QPixmap.fromImage(output))
        return img_data
     
    def databasetoPixmap(self,image):
        convert = BytesIO(image)
        img = PIL.Image.open(convert)
        img = np.array(img) 
        # Convert RGB to BGR 
        output = img[:, :, ::-1].copy()
        height, width = output.shape[:2]
        bytesPerLine = 3 * width
        output2 = np.require(output, np.uint8, 'C')
        output = QImage(output2, width, height,bytesPerLine,QImage.Format.Format_RGB888).rgbSwapped()
        img_data = QPixmap(QPixmap.fromImage(output))

        return img_data


    def image_resize(image, width = None, height = None, inter = cv.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]
        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image
        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized