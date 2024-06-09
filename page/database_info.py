from PyQt6 import  uic
from PyQt6.QtWidgets import QApplication,QMainWindow,QFileDialog
from PyQt6.QtCore import QDate
from PyQt6.QtGui import QPixmap




import dotenv
import os


#import model
import Model.database as database 
#import controller
import Controller.ui_controller as ui

class databaseInfo(QMainWindow):
    def __init__(self):
        super(databaseInfo, self).__init__()
        uic.loadUi('UI/database_info.ui', self)

        self.env_file = dotenv.find_dotenv()
        dotenv.load_dotenv(self.env_file,override=True)

        

        self.database_detail = {
                    "host": os.getenv("DB_HOST"),
                    "port": os.getenv("DB_PORT"),
                    "database_name": os.getenv("DB_DATABASE"),
                    "database_username": os.getenv("DB_USERNAME"),
                    "database_password": os.getenv("DB_PASSWORD"),
                    }

        self.host_edit.setText(self.database_detail["host"])
        self.port_edit.setText(self.database_detail["port"])
        self.database_name_edit.setText(self.database_detail["database_name"])
        self.username_edit.setText(self.database_detail["database_username"])
        self.password_edit.setText(self.database_detail["database_password"])

        self.default_btn.clicked.connect(self.set_default)
        self.confirm_btn.clicked.connect(self.confirm_database)

    def set_default(self):
        self.database_detail["host"] = "127.0.0.1"
        self.database_detail["port"] = "3305"
        self.database_detail["database_name"] = "portfolio"
        self.database_detail["database_username"] = "root"
        self.database_detail["database_password"] = ""

        dotenv.set_key(self.env_file,"DB_HOST",self.database_detail["host"])
        dotenv.set_key(self.env_file,"DB_PORT",self.database_detail["port"])
        dotenv.set_key(self.env_file,"DB_DATABASE",self.database_detail["database_name"])
        dotenv.set_key(self.env_file,"DB_USERNAME",self.database_detail["database_username"])
        dotenv.set_key(self.env_file,"DB_PASSWORD",self.database_detail["database_password"])

        self.host_edit.setText(self.database_detail["host"])
        self.port_edit.setText(self.database_detail["port"])
        self.database_name_edit.setText(self.database_detail["database_name"])
        self.username_edit.setText(self.database_detail["database_username"])
        self.password_edit.setText(self.database_detail["database_password"])

    def confirm_database(self):
        self.database_detail["host"] = self.host_edit.text()
        self.database_detail["port"] = self.port_edit.text()
        self.database_detail["database_name"] = self.database_name_edit.text()
        self.database_detail["database_username"] = self.username_edit.text()
        self.database_detail["database_password"] = self.password_edit.text()

        dotenv.set_key(self.env_file,"DB_HOST",self.database_detail["host"])
        dotenv.set_key(self.env_file,"DB_PORT",self.database_detail["port"])
        dotenv.set_key(self.env_file,"DB_DATABASE",self.database_detail["database_name"])
        dotenv.set_key(self.env_file,"DB_USERNAME",self.database_detail["database_username"])
        dotenv.set_key(self.env_file,"DB_PASSWORD",self.database_detail["database_password"])

        ui.message.finish(self,message="Database information change complete!")

    