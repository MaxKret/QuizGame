import json, sys, os
import pandas as pd
import gspread, gspread.utils
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service_account.json'), scope)
# authorize the clientsheet 
client = gspread.authorize(creds)
# get the instance of the Spreadsheet
spreadsheet = client.open('DB 1.0')

sheet_instance = spreadsheet.get_worksheet(0)

cell = sheet_instance.find("", in_row=1)
idx = cell.address
print(f"{idx[0]}{int(idx[1])+1}:{idx[0]}")
