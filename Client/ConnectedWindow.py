import os
import sys
import paramiko
import File as fl 
import Folder as fld 
import Filesystem as fs
import TextEditor
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

class ConnectedWindow(QtCore.QObject):
    def __init__(self, ui_file, ip, port, username, password, active_connection_count, driver_window, parent=None):
        super(ConnectedWindow, self).__init__(parent)
        self.driver_window = driver_window
        self.window_number = active_connection_count

        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()

        self.window = loader.load(ui_file)
        self.open_editor = None

        ui_file.close()

        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.file_system = None

        self.folder_layout = QVBoxLayout()
        self.folder_scroll_layout = QWidget()
        self.folder_scroll_layout.setLayout(self.folder_layout)
        self.file_layout = QVBoxLayout()
        self.file_scroll_layout = QWidget()
        self.file_scroll_layout.setLayout(self.file_layout)

        self.folder_scroll_area = self.window.findChild(QScrollArea, 'folder_area')
        self.folder_scroll_area.setWidget(self.folder_scroll_layout)
        self.file_scroll_area = self.window.findChild(QScrollArea, 'file_area')
        self.file_scroll_area.setWidget(self.file_scroll_layout)

        self.back_button = self.window.findChild(QPushButton, 'back_button')
        self.back_button.clicked.connect(self.back_button_clicked)

        disconnect_action = self.window.findChild(QAction, 'actionDisconnect')
        disconnect_action.triggered.connect(self.disconnect_action_triggered)

        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.ip, port=self.port, username=self.username, timeout=1, password=self.password)
        except:
            self.window.statusBar().showMessage('Could Not Connect To Host')
        finally:
            self.window.statusBar().showMessage('Status: Up at {}.{}'.format(self.username, self.ip))
            self.build_fs()

        self.window.show()

    def add_folder_widget(self, name_text):
        self.folder_layout.addWidget(FolderButton(name_text, self.client, self.file_system, self))

    def add_file_widget(self, name_text):
        self.file_layout.addWidget(FileButton(name_text, self.client, self.password, self, self.file_system))

    def pull_files(self):
        pass

    def build_fs(self):
        root_folder = fld.Folder('/', None)
        self.file_system = fs.FileSystem(root_folder)
        stdin, stdout, stderr = self.client.exec_command('cd / && ls')
        for line in stdout:
            line = line.replace('\n', '')
            if '.' in line:
                new_file = fl.File(line, self.file_system.current_dir)
                self.file_system.current_dir.add_file(new_file)
            else:
                new_folder = fld.Folder(line, self.file_system.current_dir)
                self.file_system.current_dir.add_folder(new_folder)
        for folder in self.file_system.root_dir.contents['Sub-Folders']:
            self.add_folder_widget(folder.folder_name)
        for file in self.file_system.root_dir.contents['Files']:
            self.add_file_widget(file.file_name)
        self.file_system.current_dir.added = True
        self.window.show()      

    def back_button_clicked(self):
        if self.file_system != None and self.file_system != self.file_system.root_dir:
            self.file_system.move_up()
            folder_buttons = self.folder_scroll_layout.findChildren(QWidget)
            file_buttons = self.file_scroll_layout.findChildren(QWidget)
            for button in folder_buttons:
                button.deleteLater()
            for button in file_buttons:
                button.deleteLater()
            for folder in self.file_system.current_dir.contents['Sub-Folders']:
                self.add_folder_widget(folder.folder_name)
            for file in self.file_system.current_dir.contents['Files']:
                self.add_file_widget(file.file_name)
            self.window.show() 

    # def new_file_triggered(self, new_file_name):
    #     command = "touch {}".format(new_file_name)
    #     command = "sudo -S -p '' %s" % command
    #     stdin, stdout, stderr = self.client.exec_command(command)
    #     stdin.write(self.password + '\n')
    #     stdin.flush()

    def disconnect_action_triggered(self):
        self.client.close()
        self.window.close()

class FolderButton(QWidget):
    def __init__(self, folder_name, client, file_system, window, parent = None):
        super(FolderButton, self).__init__(parent)
        self.folder_name = folder_name
        self.client = client
        self.window = window
        self.folder_button = QPushButton(folder_name)
        self.folder_button.clicked.connect(lambda : self.folder_button_clicked(file_system))
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.folder_button)
        self.setLayout(self.layout)
        
    def folder_button_clicked(self, file_system):
        file_system.move_down(self.folder_name)
        folder_buttons = self.parent().findChildren(QWidget)
        file_buttons = self.window.file_scroll_layout.findChildren(QWidget)
        for button in folder_buttons:
            button.deleteLater()
        for button in file_buttons:
            button.deleteLater()
        if file_system.current_dir.added == False:
            stdin, stdout, stderr = self.client.exec_command('ls {}'.format(file_system.current_path))
            for line in stdout:
                line = line.replace('\n', '')
                if '.' in line:
                    new_file = fl.File(line, file_system.current_dir)
                    file_system.current_dir.add_file(new_file)
                    self.window.add_file_widget(new_file.file_name)
                else:
                    new_folder = fld.Folder(line, file_system.current_dir)
                    file_system.current_dir.add_folder(new_folder)
                    self.window.add_folder_widget(new_folder.folder_name)
            file_system.current_dir.added = True
        else:
            file_system.move_down(self.folder_name)
            folder_buttons = self.parent().findChildren(QWidget)
            file_buttons = self.window.file_scroll_layout.findChildren(QWidget)
            for button in folder_buttons:
                button.deleteLater()
            for button in file_buttons:
                button.deleteLater()
            for folder in self.window.file_system.current_dir.contents['Sub-Folders']:
                self.window.add_folder_widget(folder.folder_name)
            for file in self.window.file_system.current_dir.contents['Files']:
                self.window.add_file_widget(file.file_name)
        

class FileButton(QWidget):
    def __init__(self, file_name, client, password, window, file_system, parent = None):
        super(FileButton, self).__init__(parent)
        self.window = window

        self.file_name = file_name
        self.client = client
        self.file_button = QPushButton(file_name)
        self.file_button.clicked.connect(lambda: self.file_button_clicked(file_system, password))

        layout = QHBoxLayout()
        layout.addWidget(self.file_button)
        self.setLayout(layout)

    def file_button_clicked(self, file_system, password):
        file_name_path = file_system.current_path + self.file_name
        self.window.open_editor = TextEditor.get_mainwindow(self.client, file_name_path, self.file_name, file_system, password, self.window)
        self.window.open_editor.window.show()

def get_mainwindow(ip, port, username, password, window_count, driver_window):
    widget = QWidget()
    connected_window = ConnectedWindow('connectedinterface.ui', ip, port, username, password, window_count, driver_window)
    return connected_window

def main():
    os.system('python Driver.py')

if __name__ == '__main__':
    main()