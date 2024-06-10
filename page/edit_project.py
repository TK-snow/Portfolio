from PyQt6 import  uic
from PyQt6.QtWidgets import QMainWindow,QFileDialog
from PyQt6.QtCore import QDate



from pathlib import Path
import tempfile
import cv2 as cv


#import model
import Model.database as database 
#import controller
import Controller.ui_controller as ui

import page.project_dashboard as dashboard

class editProjectPage(QMainWindow):
    def __init__(self,id,username):
        super(editProjectPage, self).__init__()
        uic.loadUi('UI/edit_project.ui', self)

        self.back = None


        self.username = username
        self.Id = id
        project = database.project()
        project.connect()
        result = project.get_data_by_id(id)
        project.disconnect()
        data = result[0]

        self.project_data = {
            "id" : data[0],
            "title" : data[1],
            "type" : data[2],
            "period": data[3],
            "image_1" : data[4],
            "image_2" : data[5],
            "description" : data[6],
            "present_link" : data[7],
            "git_link" : data[8]
        }

        

        self.title_edit.setText(self.project_data["title"])
        self.project_data["period"] = QDate.fromString(str(self.project_data["period"]),"yyyy")
        self.year_edit.setDate(self.project_data["period"])
        index = self.project_type_box.findText(self.project_data["type"])
        self.project_type_box.setCurrentIndex(index) 
        self.description_box.setPlainText(self.project_data["description"])
        self.present_link_edit.setText(self.project_data["present_link"])
        self.git_link_edit.setText(self.project_data["git_link"])

        self.temp_file_1 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        self.temp_file_2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)

        img_data = ui.image_frame.databasetoPixmap(self,self.project_data["image_1"])
        self.picture_show_1.setPixmap(img_data)
        img_data = ui.image_frame.databasetoPixmap(self,self.project_data["image_2"])
        self.picture_show_2.setPixmap(img_data)

        self.upload_picture1_btn.clicked.connect(self.select_image_1)
        self.upload_picture2_btn.clicked.connect(self.select_image_2)
        self.edit_project_btn.clicked.connect(self.edit_data)
    
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
            image_1_blob = open(self.temp_file_1.name,'rb').read()

            self.project_data["image_1"] = image_1_blob

            
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

            image_2_blob = open(self.temp_file_2.name,'rb').read()
            self.project_data["image_2"] = image_2_blob

            self.img_data = ui.image_frame.openCVtoPixmap(self,self.image_2)
            self.picture_show_2.setPixmap(self.img_data)
            self.hasImage2 = True

    def edit_data(self):
        self.project_data["title"] = self.title_edit.text()
        self.project_data["period"] = self.year_edit.text()
        self.project_data["type"] = str(self.project_type_box.currentText())
        self.project_data["description"] = str(self.description_box.toPlainText())
        self.project_data["present_link"] = self.present_link_edit.text()
        self.project_data["git_link"] = self.git_link_edit.text()

        values = (self.project_data["title"],self.project_data["type"],self.project_data["period"],
                  self.project_data["image_1"],self.project_data["image_2"],
                  self.project_data["description"],self.project_data["present_link"],self.project_data["git_link"],self.Id
                  )


        project = database.project()
        project.connect()

        project.update_project(values)

        project.disconnect()

        self.back = dashboard.Dashboard(self.username)
        self.back.show()

        self.close()

        

        



        