import os
import sys
import paramiko
import requests
from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
import LoginWindow, ConnectWindow, ConnectedWindow
from PySide2.QtWidgets import QApplication, QLineEdit, QPushButton, QTabWidget, QWidget, QTextEdit

class DriverWindow(QtCore.QObject):
    def __init__(self, parent=None):
        super(DriverWindow, self).__init__(parent)
        self.active_window = LoginWindow.get_mainwindow(self)
        self.connected_windows = {}
        self.connected_window_count = 0
        self.ip = None
        self.port = None
        self.username = None
        self.password = None

    def LoginSignal(self):
        self.active_window.window.close()
        self.active_window = ConnectWindow.get_mainwindow(self)
        self.active_window.window.show()

    def ConnectSignal(self):
        self.connected_window_count += 1
        window_label = "window" + str(self.connected_window_count)
        self.connected_windows[window_label] = ConnectedWindow.get_mainwindow(self.ip, self.port, self.username, self.password, self.connected_window_count, self)
        self.connected_windows[window_label].window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    driver_window = DriverWindow()
    driver_window.active_window.window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()