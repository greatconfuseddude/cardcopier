import os, shutil, glob
import datetime as dt
import concurrent.futures
from tqdm import tqdm
from consolemenu import *
from consolemenu.items import *

def copy_files(title, backup_folder_path, sd_folder_path, date):
  for item in sd_folder_path:
    sd_card_path = "/Volumes/Untitled/DCIM/" + item
    n = len(os.listdir(sd_card_path))
    print(f"{n} photos are available to copy on {sd_card_path}")

    for file_name in tqdm(os.listdir(sd_card_path),
        mininterval=2,
        desc="Photo backup is in progress"):
      try:
        file_path = os.path.join(sd_card_path, file_name)
        new_file_name = title + "_" + date + "_RAW_" + file_name
        shutil.copy(file_path, os.path.join(backup_folder_path, new_file_name))
      except(IndexError) as e:
        print("Nuhuh u don't")
          
    print(f'Files on {sd_card_path} have completed copying')

def backup():
  title = input("Enter the event title for your archival folder: ")
  camera_brands = ["Sony","Nikon","Polaroid"]
  camera_menu = SelectionMenu(camera_brands); camera_menu.show()

  if camera_brands[camera_menu.selected_option] == 0 or 1:
    sd_folder_path = os.listdir(f"/Volumes/Untitled/DCIM/")
  elif camera_brands[camera_menu.selected_option] == 2:
    #sd_folder_path = os.listdir(f"/Volumes/Untitled/????????")
    print("gud luk wit that")

  drives_list = ["Sabrent",
                "Backup Plus",
                "My Passport For Mac",
                "My Passport For Mac Two"]
  
  selection_menu = SelectionMenu(drives_list)
  selection_menu.show()
  
  attached_drive_path = "/Volumes/"+drives_list[selection_menu.selected_option]
  backup_folder_path = os.path.join(attached_drive_path, title)
  os.mkdir(backup_folder_path)
  
  print(f"Folder was created at {backup_folder_path}")

  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    fdate = os.path.getctime("/Volumes/Untitled/DCIM/")
    date = dt.datetime.utcfromtimestamp(fdate).strftime("%Y-%m-%d")
    
    executor.map(copy_files(title, 
                            backup_folder_path, 
                            sd_folder_path, 
                            date), 
                 sd_folder_path)

if __name__ == "__main__":
  backup()
