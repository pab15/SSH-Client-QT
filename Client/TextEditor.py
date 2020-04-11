import os
import sys
import paramiko
import File as fl 
import Folder as fld 
import Filesystem as fs
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *

class TextEditor(QtCore.QObject):
    def __init__(self, ui_file, client, file_name_path, file_name, file_system, password, driver_window, parent=None):
        super(TextEditor, self).__init__(parent)
        self.driver_window = driver_window

        ui_file = QtCore.QFile(ui_file)
        ui_file.open(QtCore.QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        
        ui_file.close()

        self.client = client
        self.name = file_name
        self.file_name = file_name_path
        self.password = password

        self.text_area = self.window.findChild(QPlainTextEdit, 'text_editor')
        command = "cat {}".format(file_name_path)
        command = "sudo -S -p '' %s" % command
        stdin, stdout, stderr = self.client.exec_command(command)
        stdin.write(self.password + '\n')
        stdin.flush()
        text = ''
        for line in stdout:
            text = text + line
        self.text_area.setPlainText(text)

        delete_action = self.window.findChild(QAction, 'actionDelete_File')
        delete_action.triggered.connect(self.delete_action_triggered)
        
        close_action = self.window.findChild(QAction, 'actionClose')
        close_action.triggered.connect(self.close_action_triggered)

        self.save_host_button = self.window.findChild(QPushButton, 'save_host')
        self.save_host_button.clicked.connect(lambda: self.save_host_button_clicked(self.client, self.password, self.file_name))

        self.save_client_button = self.window.findChild(QPushButton, 'save_client')
        self.save_client_button.clicked.connect(lambda: self.save_client_button_clicked(self.client, self.password, self.file_name))

        self.window.show()
        
    def save_host_button_clicked(self, client, password, file_name):
      contents = self.text_area.toPlainText()
      with open('Saved-Files/' + self.name, 'w') as file:
        file.write(contents)
      self.window.statusBar().showMessage('Success!')

    def save_client_button_clicked(self, client, password, file_name):
      contents = self.text_area.toPlainText()
      command = "echo '{}' | sudo -S -p '' tee {}".format(contents, self.file_name)
      command = "sudo -S -p '' %s" % command
      stdin, stdout, stderr = self.client.exec_command(command)
      stdin.write(self.password + '\n' + self.password + '\n')
      stdin.flush()
      self.window.statusBar().showMessage('Success!')
      
    def close_action_triggered(self):
        self.window.close()

    def delete_action_triggered(self):
      command = "rm {}".format(self.file_name)
      command = "sudo -S -p '' %s" % command
      stdin, stdout, stderr = self.client.exec_command(command)
      stdin.write(self.password + '\n')
      stdin.flush()
      folder_buttons = self.driver_window.file_scroll_layout.findChildren(QWidget)
      file_buttons = self.driver_window.file_scroll_layout.findChildren(QWidget)
      for button in folder_buttons:
          button.deleteLater()
      for button in file_buttons:
          button.deleteLater()
      for folder in self.driver_window.file_system.current_dir.contents['Sub-Folders']:
          self.driver_window.add_folder_widget(folder.folder_name)
      count = 0
      for file in self.driver_window.file_system.current_dir.contents['Files']:
        if file.file_name == self.name:
          del self.driver_window.file_system.current_dir.contents['Files'][count]
          count += 1
        else:
          self.driver_window.add_file_widget(file.file_name)
          count += 1
      self.window.close()

def get_mainwindow(client, file_name_path, file_name, file_system, password, driver_window):
    widget = QWidget()
    editor_window = TextEditor('texteditor.ui', client, file_name_path, file_name, file_system, password, driver_window)
    return editor_window

def main():
  os.system('python Driver.py')

if __name__ == '__main__':
  main()