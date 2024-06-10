from PyQt6 import  uic
from PyQt6.QtWidgets import QMainWindow,QFileDialog



from pathlib import Path
import cv2 as cv
import tempfile


#import model
import Model.database as database 
#import controller
import Controller.ui_controller as ui

import page.menu as menu

class addProjectPage(QMainWindow):
    def __init__(self,username,name,menu_page):
        super(addProjectPage, self).__init__()
        uic.loadUi('UI/add_project.ui', self)
        self.user = username
        self.name = name
        self.menu = menu_page
        self.hasImage1 = False
        self.hasImage2 = False
        self.temp_file_1 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.temp_file_2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

        self.upload_picture1_btn.clicked.connect(self.select_image_1)
        self.upload_picture2_btn.clicked.connect(self.select_image_2)
        self.add_project_btn.clicked.connect(self.summit_data)


    def select_image_1(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            path = Path(filename)

            self.image_1 = cv.imread(str(path))
            width,height = self.image_1.shape[:2]
            if(width > height):
                if(width > 500):
                    self.image_1 = ui.image_frame.image_resize(self.image_1,width=500)
            elif(width < height):
                if(height > 400):
                    self.image_1 = ui.image_frame.image_resize(self.image_1,height=400)

            cv.imwrite(self.temp_file_1.name,self.image_1)

            
            self.img_data = ui.image_frame.openCVtoPixmap(self,self.image_1)
            self.picture_show_1.setPixmap(self.img_data)
            self.hasImage1 = True
        
    def select_image_2(self):
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File", 
            r"D:/", 
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            path = Path(filename)

            self.image_2 = cv.imread(str(path))
            width,height = self.image_2.shape[:2]
            if(width > height):
                if(width > 500):
                    self.image_2 = ui.image_frame.image_resize(self.image_2,width=500)
            elif(width < height):
                if(height > 400):
                    self.image_2 = ui.image_frame.image_resize(self.image_2,height=400)

            cv.imwrite(self.temp_file_2.name,self.image_2)
            self.img_data = ui.image_frame.openCVtoPixmap(self,self.image_2)
            self.picture_show_2.setPixmap(self.img_data)
            self.hasImage2 = True

    def summit_data(self):
        title = self.title_edit.text()
        year = self.year_edit.text()
        type = str(self.project_type_box.currentText())
        description = str(self.description_box.toPlainText())
        present = self.present_link_edit.text()
        git = self.git_link_edit.text()
        year = int(year)
        if(title == ""):
            ui.message.alert(self,message="please enter title of project before summit")
        elif not self.hasImage1:
            ui.message.alert(self,message="please choose 2 of image of example before summit")
        elif not self.hasImage2:
            ui.message.alert(self,message="please choose 2 of image of example before summit")
        elif(description == ""):
            ui.message.alert(self,message="please enter description of project before summit")
        else:
            image_1_blob = open(self.temp_file_1.name,'rb').read()
            image_2_blob = open(self.temp_file_2.name,'rb').read()

            value = (title,type,year,image_1_blob,image_2_blob,description,present,git)

            project = database.project()
            project.connect()

            project.add_project(value)

            project.disconnect()


            self.title_edit.clear()
            self.picture_show_1.clear()
            self.picture_show_1.setText("Project Picture 1")
            self.picture_show_2.clear()
            self.picture_show_2.setText("Project Picture 2")
            self.description_box.clear()
            self.present_link_edit.clear()
            self.git_link_edit.clear()
            self.project_type_box.setCurrentIndex(0) 