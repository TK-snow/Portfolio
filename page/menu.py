from PyQt6 import  uic
from PyQt6.QtWidgets import QApplication,QMainWindow,QWidget



import sys
from dotenv import load_dotenv
import hashlib
import os

#import model
import Model.database as database 
#import controller
import Controller.ui_controller as ui

#import page
import page.add_project as add_page
import page.project_dashboard as dashboard




class Menu(QMainWindow):
    def __init__(self,username,name):
        super(Menu, self).__init__()
        uic.loadUi('UI/menu.ui', self)
        self.addPage = None
        self.dashboard = None
        self.user = username
        self.name = name
        
        
        self.name_surname.setText(name)
        self.add_pj_btn.clicked.connect(self.open_add_page)
        self.dashboard_btn.clicked.connect(self.open_dashboard)
        self.exit_btn.clicked.connect(self.close_app)


        

        
    def open_add_page(self):
        self.addPage = add_page.addProjectPage(self.user,self.name,self)
        self.addPage.show()

        
    def open_dashboard(self):
        self.addPage = dashboard.Dashboard(self.user)
        self.addPage.show() 

    def close_app(self):
        self.close()

    
    


            
    
