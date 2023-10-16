import datetime as dt
import concurrent.futures
from tqdm import tqdm
from consolemenu import *
from consolemenu.items import *

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import qdarktheme
import threading
import shutil
import time
import json
import os, sys


with open(os.getcwd() + '/settings.json' ,'r+') as file:
    file_data = json.load(file)
    drive_loc = file_data['drive_mnt_loc']
    sd_loc = file_data['sd_mnt_loc']

  
class GUI(QMainWindow):   
    def __init__(self): 
        super().__init__() 
  
        self.setWindowTitle("CopyCAT!")   
        self.setFixedSize(500, 320)  
        #self.setStyleSheet("background-color: #0f1112;")  
        self.UiComponents()   

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
        title.setText("CopyCAT!")
        title.setFont(QFont('Arial', 16))
        title.resize(200, 50)
        
        save_txt = QLabel(self)
        save_txt.setText("Save Me:")
        save_txt.setGeometry(150, 30, 100, 20) 
        
        save_to_txt = QLabel(self)
        save_to_txt.setText("Save Me To:")
        save_to_txt.setGeometry(150, 90, 100, 20)
        
        album_tag_txt = QLabel(self)
        album_tag_txt.setText("Album Tag:")
        album_tag_txt.setGeometry(175, 150, 100, 20)
        
        self.show() 
  
    def UiComponents(self): 
        self.save = QComboBox(self)   
        self.save.setGeometry(150, 55, 200, 30)  
        sd_folder_path = os.listdir(sd_loc)
        self.save.addItems(sd_folder_path)  
        
        self.save_to = QComboBox(self)   
        self.save_to.setGeometry(150, 115, 200, 30)           
        attached_drive_list = os.listdir(drive_loc)
        self.save_to.addItems(attached_drive_list)  

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
        self.thread = threading.Thread(target=self.backup, args=(self.album_tag.text(),), daemon=True)
        self.thread.start()
        self.catdance = threading.Thread(target=self.cat_dance, daemon=True)
        self.catdance.start()
        
    def reset_ui(self):  
        self.dance = False  
        self.pbar.setHidden(True)
        self.pbar.setValue(0)
        self.start.setEnabled(True)
        self.start.setHidden(False)
        self.album_tag.setText("")        
                
    def backup(self, title):
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
        

if __name__ == "__main__":    
    App = QApplication(sys.argv)
    qdarktheme.setup_theme()   
    gui = GUI()  
    sys.exit(App.exec()) 
