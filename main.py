import os, shutil
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
  camera_brands = ["Sony","Nikon","Canon","Polaroid"]
  camera_menu = SelectionMenu(camera_brands)
  camera_menu.show(); cma = camera_menu.selected_option + 1
  
  if cma == 1:
    sd_folder_path = os.listdir(f"/Volumes/Untitled/DCIM/")
  elif cma == 2:
    sd_folder_path = os.listdir(f"/Volumes/Untitled/DCIM/")
  elif cma == 3:
    sd_folder_path = os.listdir(f"/Volumes/Untitled/DCIM/100CANON/")
  elif cma == 4:
    #sd_folder_path = os.listdir(f"/Volumes/Untitled/DCIM/???N/")
    print("try again")

  drives_list = ["Sabrent",
                "Backup Plus",
                "My Passport For Mac",
                "My Passport For Mac Two"]
  
  selection_menu = SelectionMenu(drives_list)
  selection_menu.show()
  
  attached_drive_path = "/Volumes/"+drives_list[selection_menu.selected_option]
  backup_folder_path = os.path.join(attached_drive_path, title)
  os.mkdir(backup_folder_path)
  print(f"Folder {title} was created at {backup_folder_path}")

  with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    pre_date = os.path.getctime("/Volumes/Untitled/DCIM/")
    date = dt.datetime.utcfromtimestamp(pre_date).strftime("%Y-%m-%d")
    
    executor.map(copy_files(title, 
                            backup_folder_path, 
                            sd_folder_path, 
                            date), 
                 sd_folder_path)

if __name__ == "__main__":
  backup()
