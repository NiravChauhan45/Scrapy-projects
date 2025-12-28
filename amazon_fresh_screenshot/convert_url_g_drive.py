from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import db_config as db
# ======================= Google Drive Setup =======================
SERVICE_ACCOUNT_FILE = r'D:\Nirav Chauhan\code\amazon_fresh_screenshot\testingproject-436810-397c59f4c027.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build('drive', 'v3', credentials=creds)

# ======================= File and Folder =======================
folder_id = '17hYnzu7G_csl3tO9ZB-cGnFgWprmAt3p'
file_name_input = fr"{db.filepath}\{db.amazon_filename}.xlsx"
output_filename = fr"{db.filepath}\Updated_{db.amazon_filename}.xlsx"


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
    df.to_excel(output_filename, index=False)



# Todo: https://drive.google.com/drive/folders/1T1lUe10FQLxultRfygiIo85F3WAOUVF0