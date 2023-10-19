from PyQt6.QtWidgets import * 
from PyQt6 import QtCore, QtGui 
from PyQt6.QtGui import * 
from PyQt6.QtCore import * 
from tqdm import tqdm
import datetime as dt
import concurrent.futures
import qdarktheme
import threading
import shutil
import time
import json
import sys
import os

def get_path(which_path):
    try:
        with open(os.getcwd() + '/settings.json' ,'r+') as file:
            file_data = json.load(file)
            drive_mnt_loc = file_data['drive_mnt_loc']
            sd_mnt_loc = file_data['sd_mnt_loc']
            if which_path == 'drive_path' and os.path.exists(drive_mnt_loc):
                return drive_mnt_loc
            elif which_path == 'sd_path'and os.path.exists(sd_mnt_loc):
                return sd_mnt_loc
            else:
                print(f"settings.json[{which_path}]: Path not found.")
                return os.path.expanduser("~/")
    except FileNotFoundError:
        return os.path.expanduser("~/")

class SettingsGUI(QMainWindow):
    settings_closed = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Settings")
        self.setFixedSize(400, 200) 
        self.SettingsUI()
        
        save_txt = QLabel(self)
        save_txt.setText("Default SD Card Mount Path:")
        save_txt.setGeometry(50, 10, 210, 20) 
        
        save_to_txt = QLabel(self)
        save_to_txt.setText("Default Backup Drive Mount Path:")
        save_to_txt.setGeometry(50, 70, 210, 20)
        
    def SettingsUI(self): 
        self.save_button = QPushButton("Save", self) 
        self.save_button.setGeometry(100, 150, 75, 25) 
        self.save_button.clicked.connect(self.save_settings)
        self.save_button.setStyleSheet("background-color : green; color: white")
        
        self.cancel_button = QPushButton("Cancel", self) 
        self.cancel_button.setGeometry(225, 150, 75, 25) 
        self.cancel_button.clicked.connect(self.cancel)
        self.cancel_button.setStyleSheet("background-color : grey; color: white")
        
        self.save_path = QLineEdit(self)   
        self.save_path.setGeometry(50, 30, 275, 30)  
        self.save_path.setText(get_path('sd_path'))  
        
        self.select_sd = QPushButton("", self) 
        self.select_sd.setGeometry(325, 30, 25, 30) 
        self.select_sd.clicked.connect(self.select_sd_loc)
        self.select_sd.setStyleSheet("background-color : grey; color: white")
        self.select_sd.setIcon(QIcon(os.getcwd() + '/img/search.png'))
        
        self.save_to_path = QLineEdit(self)   
        self.save_to_path.setGeometry(50, 90, 275, 30)           
        self.save_to_path.setText(get_path('drive_path')) 
        
        self.select_drive = QPushButton("", self) 
        self.select_drive.setGeometry(325, 90, 25, 30) 
        self.select_drive.clicked.connect(self.select_drive_loc)
        self.select_drive.setStyleSheet("background-color : grey; color: white")
        self.select_drive.setIcon(QIcon(os.getcwd() + '/img/search.png'))
        
    def select_sd_loc(self):
        dialog = QFileDialog.getExistingDirectory(self, 'Select Directory', self.save_path.text()) + '/'
        self.save_path.setText(dialog)
        
    def select_drive_loc(self):
        dialog = QFileDialog.getExistingDirectory(self, 'Select Directory', self.save_to_path.text()) + '/'
        self.save_to_path.setText(dialog)
        
    def save_settings(self):
        if not os.path.exists(os.getcwd() + '/settings.json'):
            with open(os.getcwd() + '/settings.json' ,'w') as file:
                tmp = os.path.expanduser("~/")                
                json.dump({"drive_mnt_loc" : "{tmp}", "sd_mnt_loc" : "{tmp}"}, file) 
                print("settings.json created")
        with open(os.getcwd() + '/settings.json' ,'r+') as file:
            file_data = json.load(file)
            file_data['sd_mnt_loc'] = self.save_path.text()
            file_data['drive_mnt_loc'] = self.save_to_path.text()
        with open(os.getcwd() + '/settings.json' ,'w') as file:
            json.dump(file_data, file)
        self.hide()  
        self.settings_closed.emit()     
        
    def cancel(self):
        self.hide()
        
class GUI(QMainWindow):   
    def __init__(self): 
        super().__init__() 
  
        self.setWindowTitle("copycat")   
        self.setFixedSize(500, 320)    
        self.MainUI()   

        self.cat_img = QLabel(self)
        pixmap = QPixmap(os.getcwd() + '/img/center.png')
        self.cat_img.move(400, 180)
        self.cat_img.setPixmap(pixmap)
        self.cat_img.resize(pixmap.width(), pixmap.height())
        
        self.cat_left = QLabel(self)
        pixmap_cl = QPixmap(os.getcwd() + '/img/left.png')
        self.cat_left.move(400, 180)
        self.cat_left.setPixmap(pixmap_cl)
        self.cat_left.resize(pixmap_cl.width(), pixmap_cl.height())
        self.cat_left.setHidden(True)
        
        self.cat_right = QLabel(self)
        pixmap_cr = QPixmap(os.getcwd() + '/img/right.png')
        self.cat_right.move(400, 180)
        self.cat_right.setPixmap(pixmap_cr)
        self.cat_right.resize(pixmap_cr.width(), pixmap_cr.height())
        self.cat_right.setHidden(True)
        
        title = QLabel(self)
        title.setText("copycat")
        title.setFont(QFont('Arial', 16))
        title.resize(200, 50)
        
        save_txt = QLabel(self)
        save_txt.setText("Select SD Card:")
        save_txt.setGeometry(130, 35, 150, 20) 
        
        save_to_txt = QLabel(self)
        save_to_txt.setText("Select Backup Drive:")
        save_to_txt.setGeometry(130, 95, 150, 20)
        
        album_tag_txt = QLabel(self)
        album_tag_txt.setText("Album Tag:")
        album_tag_txt.setGeometry(175, 155, 100, 20)
        
        self.show() 
  
    def MainUI(self): 
        self.save = QComboBox(self)   
        self.save.setGeometry(130, 55, 240, 30)  
        self.sd_folder_path = os.listdir(get_path('sd_path'))
        self.save.addItems(self.sd_folder_path)  
        
        self.save_to = QComboBox(self)   
        self.save_to.setGeometry(130, 115, 240, 30)
        self.attached_drive_list = os.listdir(get_path('drive_path'))
        self.save_to.addItems(self.attached_drive_list)  

        self.album_tag = QLineEdit(self)
        self.album_tag.setGeometry(175, 175, 150, 30) 
        
        self.start = QPushButton("START", self) 
        self.start.setGeometry(200, 230, 100, 50) 
        self.start.clicked.connect(self.press_handler)
        self.start.setStyleSheet("background-color : green; color: white")
        
        self.pbar = QProgressBar(self)   
        self.pbar.setGeometry(50, 240, 400, 30)   
        self.pbar.setHidden(True)
        self.pbar.setStyleSheet("QProgressBar::chunk ""{" "background-color : purple;""}")
        
        self.settings = QPushButton("", self) 
        self.settings.setGeometry(455, 10, 30, 30) 
        self.settings.clicked.connect(self.open_settings)
        self.settings.setIcon(QIcon(os.getcwd() + '/img/settings.png'))
        
    def open_settings(self):
        self.settings_w = SettingsGUI()
        self.settings_w.settings_closed.connect(self.refresh_paths)
        self.settings_w.show()
        
    def refresh_paths(self):
        self.save.clear() 
        self.save_to.clear()
        self.save.addItems(os.listdir(get_path('sd_path')))
        self.save_to.addItems(os.listdir(get_path('drive_path')))
        
    def cat_dance(self):
        self.dance = True
        self.cat_img.setHidden(True)
        while self.dance:
            self.cat_right.setHidden(False)
            time.sleep(.2)
            self.cat_right.setHidden(True)
            self.cat_left.setHidden(False)
            if self.dance:
                time.sleep(.2)    
                self.cat_left.setHidden(True) 
        self.cat_right.setHidden(True)
        self.cat_left.setHidden(True)
        self.cat_img.setHidden(False)
    
    def press_handler(self): 
        self.pbar.setHidden(False)
        self.start.setEnabled(False)
        self.start.setHidden(True)
        self.settings.setEnabled(False)
        self.save.setEnabled(False)
        self.save_to.setEnabled(False)
        self.album_tag.setEnabled(False)
        self.thread = threading.Thread(target=self.backup, args=(self.album_tag.text(), get_path('sd_path'), get_path('drive_path'),), daemon=True)
        self.thread.start()
        self.catdance = threading.Thread(target=self.cat_dance, daemon=True)
        self.catdance.start()
        
    def reset_ui(self):  
        self.dance = False  
        self.pbar.setHidden(True)
        self.pbar.setValue(0)
        self.settings.setEnabled(True)
        self.save.setEnabled(True)
        self.save_to.setEnabled(True)
        self.album_tag.setEnabled(True)
        self.start.setEnabled(True)
        self.start.setHidden(False)
        self.album_tag.setText("")        
                
    def backup(self, title, sd_loc, drive_loc):
        self.start.setEnabled(False)
        if title == '':
            title = 'New_Album'
        backup_folder_path = os.path.join(drive_loc + self.save_to.currentText(), title)

        if os.path.isdir(backup_folder_path):
            backup_folder_path = backup_folder_path + '_' + str(time.time())
        try:
            os.mkdir(backup_folder_path)
        except:
            print('I dont work... idk')
        
        print(f"Folder {title} was created at {backup_folder_path}")        

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            pre_date = os.path.getctime(sd_loc + self.save.currentText())
            date = dt.datetime.utcfromtimestamp(pre_date).strftime("%Y-%m-%d")
    
            executor.map(self.copy_files(title, backup_folder_path, sd_loc + self.save.currentText(), date))        
        
        self.reset_ui() 
        
    def copy_files(self, title, backup_folder_path, sd_folder_path, date):  
        i = 1           
        for file_name in tqdm(os.listdir(sd_folder_path), mininterval=2, desc="Photo backup is in progress"):
            try:
                file_path = os.path.join(sd_folder_path, file_name)
                new_file_name = title + "_" + date + "_RAW_" + file_name
                shutil.copy(file_path, os.path.join(backup_folder_path, new_file_name))
                self.pbar.setValue(int(((i/len([entry for entry in os.listdir(sd_folder_path) if os.path.isfile(os.path.join(sd_folder_path, entry))]))*100))) 
                i += 1
            except(IndexError) as e:
                print("Nuhuh u don't")
          
        print(f'Files on {sd_folder_path} have completed copying')
        
if __name__ == "main":    
    App = QApplication(sys.argv)
    qdarktheme.setup_theme()   
    gui = GUI()  
    sys.exit(App.exec())
