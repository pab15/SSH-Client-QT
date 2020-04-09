import os
import sys
import paramiko
import ConnectedWindow, Driver
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QLineEdit, QPushButton, QTabWidget, QWidget

class ConnectWindow(QtCore.QObject):
    def __init__(self, ui_file, driver_window, parent=None):
        super(ConnectWindow, self).__init__(parent)
        self.driver_window = driver_window

        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        
        ui_file.close()

        connect_button = self.window.findChild(QPushButton, 'connect_button')
        connect_button.clicked.connect(self.connect_button_clicked)

        self.window.show()

    def connect_button_clicked(self):
        ip = self.window.findChild(QLineEdit, 'ip_field').text()
        port = int(self.window.findChild(QLineEdit, 'port_field').text())
        username = self.window.findChild(QLineEdit, 'username_field').text()
        password = self.window.findChild(QLineEdit, 'password_field').text()
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, port=port, username=username, timeout=1, password=password)
        except:
            self.window.statusBar().showMessage('Could Not Connect To Host')
        else:
            client.close()
            self.driver_window.ip = ip
            self.driver_window.port = port
            self.driver_window.username = username
            self.driver_window.password = password
            self.driver_window.ConnectSignal()
            self.window.statusBar().showMessage('Success')

def get_mainwindow(driver_window):
    widget = QWidget()
    connect_window = ConnectWindow('connectinterface.ui', driver_window)
    return connect_window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = ConnectWindow('connectinterface.ui')
    sys.exit(app.exec_())