import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import db_config as db

# ======================= Google Drive Setup =======================
# SERVICE_ACCOUNT_FILE = r'D:\Nirav Chauhan\amazon_screnshot\inspired-alcove-458605-k2-a25c7bc42433.json'
SERVICE_ACCOUNT_FILE = r'D:\Nirav Chauhan\code\big_basket_screenshot\big_basket_screenshot\comm-465612-6eafe74c6d09.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('drive', 'v3', credentials=creds)

# ======================= File and Folder =======================
folder_id = '1CmfutOeK1fx8_doH47jRj9JapwDBkbxm'
os.makedirs(fr"D:\Nirav Chauhan\Data\Big_Basket_Screenshot\{db.current_date}", exist_ok=True)
file_name_input = fr"D:\Nirav Chauhan\Data\Big_Basket_Screenshot\{db.current_date}\Big_Basket_data_{db.current_date}.xlsx"
output_filename = fr"D:\Nirav Chauhan\Data\Big_Basket_Screenshot\{db.current_date}\Big_Basket_data_{db.current_date}_updated.xlsx"

query = f"'{folder_id}' in parents and trashed = false"
results = service.files().list(q=query, pageSize=1000, fields="files(id, name, mimeType)").execute()
items = results.get('files', [])

df = pd.read_excel(file_name_input)

if not items:
    print("No files found.")
else:
    for item in items:
        name = item['name']
        packshot_url = f"https://drive.google.com/file/d/{item['id']}/view"

        # Match by filename in 'SKU Packshot'
        mask = df['SKU Packshot'].astype(str) == name
        df.loc[mask, 'SKU Packshot'] = packshot_url if name != 'N/A' else 'N/A'

    df.fillna('N/A', inplace=True)
    df['Sr.No'] = range(1, len(df) + 1)
    df.to_excel(output_filename, index=False)

# Todo: https://drive.google.com/drive/folders/1T1lUe10FQLxultRfygiIo85F3WAOUVF0
