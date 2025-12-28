import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

import db_config as db

# ======================= Google Drive Setup =======================
SERVICE_ACCOUNT_FILE = r'D:\Nirav Chauhan\code\gorkhnath_sir_amazon_ss\amazon_screnshot\amazon001-465605-f9434d007932.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = '1RKmxOHlRFRE0M6HBCO4icze7ahZmIDxn'  # Screenshot destination folder


# ======================= Create Date Folder on Drive =======================
def create_date_folder():
    today_drive = datetime.now().strftime('%Y_%m_%d')  # for drive folder name (e.g. 2025_04_16)
    # today_drive = "2025_05_15"  # for drive folder name (e.g. 2025_04_16)
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': today_drive,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [PARENT_FOLDER_ID]
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    folder_id = folder.get('id')

    permission = {'type': 'anyone', 'role': 'reader'}
    service.permissions().create(fileId=folder_id, body=permission).execute()

    return today_drive, folder_id


# ======================= Check if File Exists in Drive =======================
def file_exists_in_drive(filename, drive_folder_id, creds_path):
    creds = service_account.Credentials.from_service_account_file(creds_path,
                                                                  scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=creds)

    query = f"'{drive_folder_id}' in parents and name = '{filename}'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])
    return len(files) > 0


# ======================= Upload Single Screenshot (Thread Safe) =======================
def upload_single_image_thread_safe(filename, folder_id, screenshot_path, creds_path):
    try:
        # New service object for thread safety
        creds = service_account.Credentials.from_service_account_file(creds_path,
                                                                      scopes=['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=creds)

        # Check if file exists
        if file_exists_in_drive(filename, folder_id, creds_path):
            return filename, None, "Already exists"

        file_path = os.path.join(screenshot_path, filename)
        file_metadata = {'name': filename, 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='image/jpeg')
        uploaded = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = uploaded.get('id')
        file_link = f"https://drive.google.com/file/d/{file_id}/view"
        return filename, file_link, None

    except Exception as e:
        return filename, None, str(e)


# ======================= Main Logic for Code =======================
if __name__ == '__main__':
    today_drive, folder_id = create_date_folder()

    # Construct the base path using today's date (in YYYY-MM-DD format)
    base_path = db.screenshot_filepath
    screenshot_path = os.path.join(base_path)

    # ======================= ThreadPool Executor =======================
    if os.path.exists(screenshot_path):
        # List all image files in the directory
        image_list = [f for f in os.listdir(screenshot_path) if
                      f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'))]

        # Start the upload process using ThreadPoolExecutor
        uploaded_files = {}
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(upload_single_image_thread_safe, f, folder_id, screenshot_path, SERVICE_ACCOUNT_FILE): f
                for f in image_list
            }

            # Collect the results
            for future in futures:
                filename, file_link, error = future.result()
                if file_link:
                    uploaded_files[filename] = file_link
                    print(f"✅ Uploaded: {filename} (Link: {file_link})")
                elif error:
                    print(f"❌ Failed: {filename} — {error}")

        # Save the uploaded links to a JSON file
        output_links_file = os.path.join(screenshot_path, "uploaded_links.json")
        with open(output_links_file, "w") as json_file:
            json.dump(uploaded_files, json_file, indent=4)
        print(f"Uploaded file links saved to {output_links_file}")

    else:
        print(f"❌ Screenshot folder not found: {screenshot_path}")




#Todo: Google Drive Link --> https://drive.google.com/drive/folders/1T1lUe10FQLxultRfygiIo85F3WAOUVF0

# Todo: Google console Link --> https://console.cloud.google.com/welcome?inv=1&invt=Ab2cNA&project=nirav-458910