import os
import sys
import requests
import ConnectWindow, ConnectedWindow, Driver
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLineEdit, QPushButton, QTabWidget, QWidget

class LoginWindow(QtCore.QObject):
    def __init__(self, ui_file, driver_window, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.driver_window = driver_window

        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)

        ui_file.close()

        self.tab_controller = self.window.findChild(QTabWidget)

        cancel_button = self.tab_controller.findChild(QPushButton, 'cancel_button')
        cancel_button.clicked.connect(self.cancel_button_clicked)
        cancel_button_su = self.tab_controller.findChild(QPushButton, 'cancel_button_su')
        cancel_button_su.clicked.connect(self.cancel_button_clicked)

        login_button = self.tab_controller.findChild(QPushButton, 'login_button')
        login_button.clicked.connect(self.login_button_clicked)

        sign_up_button = self.tab_controller.findChild(QPushButton, 'sign_up_button')
        sign_up_button.clicked.connect(self.sign_up_button_clicked)

        self.window.show()

    def login_button_clicked(self):
        login_button = self.tab_controller.findChild(QPushButton, 'login_button')
        login_button.setEnabled(False)
        username = self.tab_controller.findChild(QLineEdit, 'username_field')
        password = self.tab_controller.findChild(QLineEdit, 'password_field')
        url = 'http://127.0.0.1:5000/login'
        data = {
                'username' : username.text(),
                'password' : password.text()
                }
        result = requests.post(url = url, data = data)
        if (result.text == 'Invalid Password' or result.text == 'Username Does Not Exist'):
            self.window.statusBar().showMessage(result.text)
            login_button.setEnabled(True)
        else:
            self.window.statusBar().showMessage(result.text)
            self.driver_window.LoginSignal()
            
    def sign_up_button_clicked(self):
        sign_up_button = self.tab_controller.findChild(QPushButton, 'sign_up_button')
        sign_up_button.setEnabled(False)
        username = self.tab_controller.findChild(QLineEdit, 'username_input_su')
        email = self.tab_controller.findChild(QLineEdit, 'email_input_su')
        password = self.tab_controller.findChild(QLineEdit, 'password_input_su')
        password_conf = self.tab_controller.findChild(QLineEdit, 'confirm_password_su')
        url = 'http://127.0.0.1:5000/signup'
        data = {
                'username' : username.text(),
                'email' : email.text(),
                'password' : password.text(),
                'password_conf' : password_conf.text()
                }
        result = requests.post(url = url, data = data)
        if (result.text == 'A User Already Exists With That Email Address' or 
                result.text == 'A User Already Exists With That Username' or
                result.text == 'One or More Fields Were Left Blank'):
            self.window.statusBar().showMessage(result.text)
            sign_up_button.setEnabled(True)
        else:
            self.window.statusBar().showMessage(result.text)

    def cancel_button_clicked(self):
        self.window.close()

def get_mainwindow(driver_window):
    window = LoginWindow('secureshellinterface.ui', driver_window)
    return window

if __name__ == '__main__':
    os.system('python Driver.py')