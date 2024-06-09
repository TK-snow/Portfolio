from PyQt6 import  uic
from PyQt6.QtWidgets import QApplication,QWidget,QMainWindow
from PyQt6.QtCore import QEvent,Qt



import sys
import hashlib



#import model
import Model.database as database 
#import controller
import Controller.ui_controller as ui

#import menu page
import page.menu as menu
import page.database_info as database_info

class loginPage(QMainWindow):
    user_login = "test"
    def __init__(self):
        super(loginPage, self).__init__()
        uic.loadUi('UI/login.ui', self)

        self.database_info = None
        self.login_btn.clicked.connect(self.login)
        self.change_database.triggered.connect(self.database_change)


        

        

        self.show()

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()


        password_hash = hashlib.new('sha256')
        password_hash.update(password.encode())
        password_hash = password_hash.hexdigest()

        admin = database.admin()
        admin.connect()

        get_data = admin.get_data_by_username(username)

        if not get_data:
            ui.message.alert(self,message="Invalid Username or Password")
            return 0
        else:
            find_data = get_data[0]
            admin_password = find_data[2]
            if admin_password != password_hash:
                ui.message.alert(self,message="Invalid Username or Password")
                return 0
            
            name = find_data[3]
            self.user_login = username
            ui.message.finish(self,message="Login Successful!")
            self.menu_page = menu.Menu(self.user_login,name)
            self.menu_page.show()
            self.close()
    
    def database_change(self):
        self.database_info = database_info.databaseInfo()
        self.database_info.show()

app = QApplication(sys.argv)
window = loginPage()
win = app.exec()



