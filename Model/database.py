import mysql.connector as mysql
from mysql.connector import errorcode
import os
import dotenv


import Controller.ui_controller as ui

class database_call :
    #default database information
    database_detail = {
                    "type": "database type",
                    "host": "database host",
                    "port": "database port",
                    "database_name": "database name",
                    "database_username": "database username",
                    "database_password": "database password",
                    }
    
    database_connect = False
    
        
    def __init__(self):
        dotenv.load_dotenv(override=True)

        self.database_detail["type"] = os.getenv("DB_CONNECTION")
        self.database_detail["host"] = os.getenv("DB_HOST")
        self.database_detail["port"] = os.getenv("DB_PORT")
        self.database_detail["database_name"] = os.getenv("DB_DATABASE")
        self.database_detail["database_username"] = os.getenv("DB_USERNAME")
        self.database_detail["database_password"] = os.getenv("DB_PASSWORD")

    def connect(self):
        try:
            self.connection = mysql.connect(
                        host=self.database_detail["host"],
                        user=self.database_detail["database_username"],
                        password=self.database_detail["database_password"],
                        database=self.database_detail["database_name"],
                        port=self.database_detail["port"]
                        )
            
            self.database_connect = True
            
            return self.connection
            
        except Exception as e:
            code = e.errno
            print(code)
            if(code == 2005):
                ui.message.alert(self,message="can't access to database server!")
            elif(code == 1045):
                ui.message.alert(self,message="Invalid Username or password")
            else:
                ui.message.alert(self,e.msg)
            return False

    def get_host(self):
        return self.database_detail["host"]

    def get_name(self):
        return self.database_detail["database_name"]
    
    def database_status(self):
        if not self.database_connect:
            return "disconnect"
        else:
            return "connect"
    
    def disconnect(self):
        self.connection.close()
        self.database_connect = False

    
    

class admin(database_call):
    def get_all(self):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)
        SQL = "SELECT * FROM admin"
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL)
            result = database_cursor.fetchall()
            database_cursor.close()
            return result
        except Exception as e:
            ui.message.alert(self,e.msg)

    def get_data_by_username(self,username):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)
        SQL = "SELECT * FROM admin WHERE username = %s"
        value = (username,)
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,value)
            result = database_cursor.fetchall()
            database_cursor.close()
            return result
        except Exception as e:
            ui.message.alert(self,e.msg)

    def new_admin(self,data):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)
        SQL = "INSERT INTO admin VALUES (%s,%s,%s,%s,%s);"
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,data)
            self.connection.commit()
            ui.message.finish(self,message="Insert data into database complete!")
            return True
        except Exception as e:
            if(e.errno == 1062):
                ui.message.alert(self,message="This username already taken!")
            return False
    
    def edit_data(self,username,field,data):
        SQL = "UPDATE admin SET " + field + " = %s WHERE username = %s"
        value = (data,username)
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,value)
            self.connection.commit()

            if(database_cursor.rowcount == 0):
                ui.message.alert(self,message="Update Data fail! No this username in database!")
                return False
            else:
                ui.message.finish(self,message="Update data from database sucessful!")
                return True
        except Exception as e :
            print(e)
            ui.message.alert(self,e.msg)
            return False
        
    def delete_data(self,username):
        SQL = "DELETE FROM admin WHERE username = %s"
        data = (username,)
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,data)
            self.connection.commit()

            if(database_cursor.rowcount == 0):
                ui.message.alert(self,message="No this data found in this database")
                return False
            else:
                ui.message.finish(self,message="Delete data from database sucessful!")
                return True
        except Exception as e :
            ui.message.alert(self,e.msg)
            return False

class project(database_call):
    def get_all(self):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)
        SQL = "SELECT * FROM project"
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL)
            result = database_cursor.fetchall()
            database_cursor.close()
            return result
        except Exception as e:
            ui.message.alert(self,e.msg)
    
    def get_data_by_id(self,id):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)
        SQL = "SELECT * FROM project WHERE ID = %s"
        value = (id,)
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,value)
            result = database_cursor.fetchall()
            database_cursor.close()
            return result
        except Exception as e:
            ui.message.alert(self,e.msg)
    
    def add_project(self,data):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)
        SQL = "INSERT INTO project VALUES ('',%s,%s,%s,%s,%s,%s,%s,%s);"
        print("to this part")
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,data)
            self.connection.commit()
            ui.message.finish(self,message="Insert data into database complete!")
            return True
        except Exception as e:
            if(e.errno == 1062):
                ui.message.alert(self,message="Already have data in database!")
            return False
        
    def update_project(self,data):
        database_cursor = self.connection.cursor()
        database_cursor = self.connection.cursor(buffered=True , dictionary=True)

        SQL = """UPDATE project SET title = %s, type = %s, 
        period = %s, project_image_1 = %s, project_image_2 = %s, detail = %s, link = %s, github = %s WHERE id = %s;"""
        
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,data)
            self.connection.commit()
            ui.message.finish(self,message="Upadate data complete!")
            return True
        except Exception as e:
            if(e.errno == 1062):
                ui.message.alert(self,message="Already have data in database!")
            ui.message.alert(self,e.msg)
            return False
        
    def delete_project(self,id):
        SQL = "DELETE FROM project WHERE id = %s"
        data = (id,)
        try:
            database_cursor = self.connection.cursor()
            database_cursor.execute(SQL,data)
            self.connection.commit()

            if(database_cursor.rowcount == 0):
                ui.message.alert(self,message="No this data found in this database")
                return False
            else:
                ui.message.finish(self,message="Delete data from database sucessful!")
                return True
        except Exception as e :
            ui.message.alert(self,e.msg)
            return False