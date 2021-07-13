
# import necessary librairs 
# for application
import sys
from  PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic,QtGui
from PyQt5.QtCore import QCoreApplication, Qt

# for DB
import psycopg2   as pg
import informations_DB  as info # to change the DB config go to informations_DB.py



# class for login page 
class MainApp(QMainWindow):
    def __init__(self):
        # initialize MainWindow    
        super().__init__()
        uic.loadUi('MainWindow.ui',self)
        self.setupUi()
        self.buttons()
    

    def setupUi(self):
        self.setWindowTitle('   Login APP for any application')
        self.setFixedSize(405,230)
        self.setWindowIcon(QtGui.QIcon('icon.png'))

     
    def checkDbConnection(self):
             # connect to db
        try:
            pgconn = pg.connect(
                host = info.db_host,
                database = info.db_name,
                user = info.db_user,
                password = info.db_password
            )
        except :
            return False
        return True


    def check_user(self,user,pgconn):
        if self.lineEdit_username.text() == '' or self.lineEdit_password.text()=='':
            QMessageBox.warning(self,"Failed Connection","Please complete info")
        else:
            # open the cursor 
            cur = pgconn.cursor() 
            username,password = user.split(' ')
            try:
                cur.execute(f"SELECT username,Password FROM users WHERE username LIKE '{username}'")
                usernames = cur.fetchall()
            except :
                QMessageBox.warning(self,"Failed Connection","Error of searching")
            else:
                if len(usernames) == 0:
                    QMessageBox.information(self,"Failed Connection","User Not Found")  
                elif len(usernames) > 0: 
                    for user in usernames:
                        if username == user[0] and password == user[1]:
                            QMessageBox.information(self,"Login successfully",f"Welcome {username}")
                            self.lineEdit_username.setText("")
                            self.lineEdit_password.setText("")
                        else:
                            QMessageBox.warning(self,"Failed Connection","Wrong  Password")
            
        

    def buttons(self):
        if self.checkDbConnection() == True:
            try:
                pgconn = pg.connect(
                    host = info.db_host,
                    database = info.db_name,
                    user = info.db_user,
                    password = info.db_password
                )
                self.pushButton_login.clicked.connect(lambda: self.check_user(self.user(),pgconn))
            except :
                pass
        else:
            QMessageBox.warning(self,"Failed Connection","Failed Connect to database")
            self.close()
    

    def user(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()
        user = username + ' ' + password
        return user 






if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginApp = MainApp()
    loginApp.show()


    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('closing window...')

