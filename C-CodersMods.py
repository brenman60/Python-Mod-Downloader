import os
import json
import requests
import shutil
import zipfile
from urllib.parse import urlparse

def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to download JSON from the URL.")
        return None

def parse_json_to_dict(json_content):
    try:
        data = json.loads(json_content)
        if isinstance(data, dict):
            return data
        else:
            print("JSON data is not a dictionary.")
            return None
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON data: {e}")
        print("Raw JSON content:")
        print(json_content.decode("utf-8"))
        return None
    
def download_latest_version(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed getting latest version")
        return None

current_version_file = os.getenv('APPDATA') + "/.minecraft/mods/modsDownloaderVersion/c-codermodsprogramversion.txt"
latest_version_url = "https://drive.google.com/uc?export=download&id=1raR1WTdIA8YnNN8uB2l2oS5Bmbv3YwXO"
latest_version = download_latest_version(latest_version_url)

if os.path.exists(current_version_file):
    current_version_text = ""
    with open(current_version_file, "r") as txt_file:
        current_version_text = txt_file.read()

    if latest_version != current_version_text:
        # Download new version
        response = requests.get(f"https://www.googleapis.com/drive/v3/files/1nfM7x7MoD6lNi0ntpzr_yiYfS1bCfi6x?alt=media&key={os.getenv('GOOGLE_API_KEY')}") # This is the link for the direct download of the most up-to-date version
        if response.status_code == 200:
            # Downloaded correctly
            print("Downloaded updated version successfully")
            filename = os.path.join(os.getcwd(), os.path.basename("Zipped_C-CodersMods.py_" + current_version_text))
            with open(filename, 'wb') as file:
                written_zip_file = file.write(response.content)

            with zipfile.ZipFile(written_zip_file, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(os.getcwd()))
        else:
            # Quit the program or something
            print("Failed downloading latest program version")
            input("Please try again. Press enter to exit...")
            exit()

        # Update version text
        with open(current_version_file, 'wb') as file:
            file.write(latest_version)

        # Remove this version and startup new version
else:
    # Download new version text file
    os.makedirs(os.getenv('APPDATA') + "/.minecraft/mods/modsDownloaderVersion/")
    with open(current_version_file, 'wb') as file:
        file.write(latest_version)

    # Download new version and abort this program
    

target_folder = os.getenv('APPDATA') + "/.minecraft/mods"

delete_old_mods = "none"
while delete_old_mods != "y" and delete_old_mods != "n":
    delete_old_mods = input("Delete already existing mods? (y/n)").lower()

if delete_old_mods == "n":
    print("Checking old mods folders...")
    new_folder_base = "OLD_MODS_ARCHIVE "
    folder_number = 0
    while os.path.exists(os.path.join(target_folder, f"{new_folder_base} {folder_number}")):
        folder_number += 1

if delete_old_mods == "n":
    print("Putting old mods away...")
    new_folder = os.path.join(target_folder, f"{new_folder_base} {folder_number}")
    os.makedirs(new_folder, exist_ok=True)
else:
    print("Deleting old mods...")
    for item in os.listdir(target_folder):
        item_path = os.path.join(target_folder, item)
        if os.path.isfile(item_path):
            os.remove(item_path)

for item in os.listdir(target_folder):
    item_path = os.path.join(target_folder, item)
    if os.path.isfile(item_path):
        shutil.move(item_path, os.path.join(new_folder, item))

print("Downloading new mods list...")
json_url = "https://drive.google.com/uc?export=download&id=1NWTY-Koaf3feyL09GJqGt1dverIGsADV"
json_content  = download_json(json_url)

if json_content:
    print("Downloading mods...")
    data_dict = parse_json_to_dict(json_content)
    if data_dict:
        for key, file_url in data_dict.items():
            try:
                response = requests.get(file_url)
                if response.status_code == 200:
                    filename = os.path.join(target_folder, os.path.basename(file_url))
                    with open(filename, 'wb') as file:
                        file.write(response.content)
                        print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download file from {file_url}: " + response.reason)
            except Exception as e:
                print(f"Error downloading file: {str(e)}")

input("Press Enter to exit...")