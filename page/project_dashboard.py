from PyQt6 import  uic
from PyQt6.QtWidgets import QMainWindow,QTableWidgetItem


#import model
import Model.database as database 
#import controller
import Controller.ui_controller as ui

#import page
import page.edit_project as edit




class Dashboard(QMainWindow):
    def __init__(self,username):
        super(Dashboard, self).__init__()
        uic.loadUi('UI/dashboard.ui', self)

        self.project_data_dashboard.cellDoubleClicked.connect(self.edit_data)
        self.project_data_dashboard.cellClicked.connect(self.select_cell)

        self.edit_btn.clicked.connect(self.edit_select)
        self.delete_btn.clicked.connect(self.delete_select)
        self.username = username

        project = database.project()
        project.connect()

        data = project.get_all()


        project.disconnect()

        for x in data:

            id = x[0]
            project_type = x[2]
            period = x[3]
            title = x[1]

            rowPosition = self.project_data_dashboard.rowCount()
            self.project_data_dashboard.insertRow(rowPosition)
            self.project_data_dashboard.setItem(rowPosition , 0,QTableWidgetItem(str(id)))
            self.project_data_dashboard.setItem(rowPosition , 1,QTableWidgetItem(str(project_type)))
            self.project_data_dashboard.setItem(rowPosition , 2,QTableWidgetItem(str(period)))
            self.project_data_dashboard.setItem(rowPosition , 3,QTableWidgetItem(str(title)))
            rowPosition = self.project_data_dashboard.rowCount()

        

    
    def edit_data(self,row, column):
        item = self.project_data_dashboard.item(row,0)
        ID = item.text()

        self.edit_page = edit.editProjectPage(ID,self.username)
        self.edit_page.show()

        self.close()

    def select_cell(self,row,column):
        item = self.project_data_dashboard.item(row,0)
        self.projectID = item.text()
        print(self.projectID)

    def edit_select(self):
        try :
            self.edit_page = edit.editProjectPage(self.projectID,self.username)
            self.edit_page.show()

            self.close()
        
        except Exception as ex :
            ui.message.alert(self,message="please select project you want to edit first1")

    def delete_select(self):
        project = database.project()

        project.connect()
        project.delete_project(self.projectID)
        data = project.get_all()
        project.disconnect()

        self.project_data_dashboard.setRowCount(0)
        for x in data:

            id = x[0]
            project_type = x[2]
            period = x[3]
            title = x[1]

            rowPosition = self.project_data_dashboard.rowCount()
            self.project_data_dashboard.insertRow(rowPosition)
            self.project_data_dashboard.setItem(rowPosition , 0,QTableWidgetItem(str(id)))
            self.project_data_dashboard.setItem(rowPosition , 1,QTableWidgetItem(str(project_type)))
            self.project_data_dashboard.setItem(rowPosition , 2,QTableWidgetItem(str(period)))
            self.project_data_dashboard.setItem(rowPosition , 3,QTableWidgetItem(str(title)))
            rowPosition = self.project_data_dashboard.rowCount()
        

    