import html

import pandas as pd
from doctor_trans import trans
import mysql.connector

# Sample data
data = pd.read_excel("F:\\Nirav\\Project_export_data\\dkforom\\dkforom_native_12_11_2024.xlsx")

trans(data, input_lang='DA', output_lang='en', download_file_name='F:\\Nirav\\Project_export_data\\dkforom\\dkforom_translated_new_01.xlsx')
