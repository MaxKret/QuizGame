# importing the required libraries
import json, sys
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
sys.path.append(".")
from streams_jsonprocessor import JSONProcessor


class DBHandler:

	current_record: list


	def __init__(self):
		# define the scope
		scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
		# add credentials to the account
		creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
		# authorize the clientsheet 
		self.client = gspread.authorize(creds)
		# get the instance of the Spreadsheet
		self.sheet = self.client.open('DB 1.0')

		self.current_record = []


	def choose_sheet(self, id):
		self.sheet_instance = self.sheet.get_worksheet(id)


	def add_record(self):
		pass

	def delete_record(self):
		pass

	def find_record(self):
		pass

	def update_record(self):
		pass


	def import_json_record(self, in_file):
		JSON_Processor = JSONProcessor(in_file=in_file)
		if((json_list := JSON_Processor.streams_json_list) is not self.current_record):
			self.current_record = json_list
			print(f"New Record selected")
		else:
			print("Record already selected")

	def export_json_record(self):
		pass



def main():
	pass

if __name__ == '__main__':
	main()