import datetime
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# from email.mime.text import MIMEText
import pandas as pd
# from email.mime.multipart import MIMEMultipart
import smtplib
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import nykaa.db_file as db

# email_sender = 'prakashkumar.bhatiya@actowiz.co.in'
email_sender = 'nirav.chauhan@actowiz.co.in'
email_password = 'eVH(EfGz{Y'

# email_reciever = 'jaiminp.actowiz@gmail.com'
email_reciever = 'niravc.actowiz@gmail.com'

# cc = ['mehula.actowiz@gmail.com','deeps.actowiz@gmail.com','rheab.actowiz@gmail.com','kunal@actowiz.com']
cc = [
    'niravc.actowiz@gmail.com',
    # 'abhishekp.actowiz@gmail.com',
    # 'jaiminp.actowiz@gmail.com',
    # 'divya.actowiz@gmail.com',
    # 'rahul.mishra@actowizsolutions.com',  # Rahul sir
    # 'sagar.sonawane@actowiz.co.in',  # Sagar sir
    # 'kunal@actowiz.com',  # kunal sir
]

# pandas
# TODO - change only this Previous_file path
Previous_file = pd.read_excel(r'F:\Nirav\Project_export_data\nykaa\nykaa_23_03_2025.xlsx')
Current_file = pd.read_excel(fr'F:\Nirav\Project_export_data\nykaa\nykaa_26_03_2025.xlsx')

Pre_week_date = '23032025'
Cur_week_date = '26032025'


# try:
#     Previous_file.drop(columns=['type'], inplace=True)
#     Current_file.drop(columns=['type'], inplace=True)
# except:
#     pass
#
# try:
#     Previous_file.drop(columns=['scrape_date'], inplace=True)
#     Current_file.drop(columns=['scrape_date'], inplace=True)
# except:
#     pass
#
# try:
#     Previous_file.drop(columns=['id'], inplace=True)
#     Current_file.drop(columns=['id'], inplace=True)
# except:
#     pass


def percent_change(old, new):
    if old == 0:  # Avoid division by zero
        return "N/A"
    pc = round(((new - old) / new) * 100, 2)
    return pc


# week format
today = datetime.date.today()
tuesday = today + datetime.timedelta((1 - today.weekday()) % 7)
Tuesday = datetime.datetime.strftime(tuesday, '%d-%m-%Y')
previous_tuesday = tuesday - datetime.timedelta(days=7)
formated_tuesday = datetime.datetime.strftime(previous_tuesday, '%d-%m-%Y')

# Pre_week = formated_tuesday


prev_df_columns = list(Previous_file.columns)
cur_df_columns = list(Current_file.columns)

cur_count_dict = {}
prev_count_dict = {}

for col in cur_df_columns:
    df_count = Current_file[col].count()
    cur_count_dict[col] = df_count
cur_html_table = PrettyTable(["DataFields", f"{Cur_week_date}"])

for col in prev_df_columns:
    df_count = Previous_file[col].count()
    prev_count_dict[col] = df_count
prev_html_table = PrettyTable(["DataFields", f"{Pre_week_date}"])

for field, counts in cur_count_dict.items():
    cur_html_table.add_row([field, counts])

for field, counts in prev_count_dict.items():
    prev_html_table.add_row([field, counts])

merge_html_table = PrettyTable(["DataField", f"{Pre_week_date}", f"{Cur_week_date}", "Difference"])
for field in cur_count_dict.keys():
    cur_count = cur_count_dict.get(field)
    prev_count = prev_count_dict.get(field)
    diff_percent = percent_change(prev_count, cur_count)
    merge_html_table.add_row([field, prev_count, cur_count, diff_percent])

# output_html = merge_html_table.get_html_string(border=1).replace('<table>', '<table border="1">')
html_output = merge_html_table.get_html_string(attributes={"border": "1", "cellpadding": "5", "cellspacing": "0"})
html_output = html_output.replace("<table>", "<table style='border-collapse: collapse;'>")
highlighted_html_output = ""

soup = BeautifulSoup(html_output, "html.parser")
rows = soup.find_all("tr")

for row in rows[1:]:  # Skip the header row
    cells = row.find_all("td")
    try:
        diff_value = float(cells[-1].text.strip())  # Get the "Difference (%)" cell value
        if abs(diff_value) >= 20:
            row.attrs["style"] = "background-color: green;"
        elif diff_value < -20:
            row.attrs["style"] = "background-color: red;"
    except ValueError:
        # Skip rows where the last cell value is not a float
        pass

highlighted_html_output = str(soup)

bcc = []
# Create email message
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciever
em['CC'] = ', '.join(cc)
em['Subject'] = "Nykaa twice week file count"
em['BCC'] = ",".join(bcc)
em.set_content(highlighted_html_output, subtype='html')

# Combine recipients
# recipients = [email_reciever] + cc

# Secure SMTP connection
context = ssl.create_default_context()
s = smtplib.SMTP('mail.actowiz.co.in', 587)
s.starttls()
s.login(email_sender, email_password)
recipients = [email_reciever] + cc + bcc
s.sendmail(email_sender, recipients, em.as_string())
s.quit()
print('Mail Sent!')
