# importing the required libraries
import json, sys, os
from flask.json.tag import PassDict
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
sys.path.append(".")
from streams_jsonprocessor import JSONProcessor


class DBHandler:

	current_record: dict
	list_file_json = None


	def __init__(self):
		# define the scope
		scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
		# add credentials to the account
		creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service_account.json'), scope)
		# authorize the clientsheet 
		self.client = gspread.authorize(creds)
		# get the instance of the Spreadsheet
		self.spreadsheet = self.client.open('DB 1.0')

		self.current_record = []


	def choose_sheet(self, id):
		self.sheet_instance = self.spreadsheet.get_worksheet(id)


	def add_record(self, record: dict):
		# convert the json to dataframe
		record_df = pd.DataFrame.from_dict(record)
		# update cell 1 with header, and cells 2+ with stream json objects
		self.sheet_instance.update_acell("C1", str(record_df.columns.values.tolist()[0]))
		self.sheet_instance.update('C2:C', [[str(y) for y in x] for x in record_df.values.tolist()])
		print()

	def delete_record(self, record: dict):
		pass

	def find_record(self, record: dict):
		pass

	def update_record(self, record: dict):
		pass


	def find_file(self, filename) -> bool:
		if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)):
			print("File Found DBHandler.py")
			with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)) as openfile:
				self.list_file_json = json.load(openfile)
			return True
		else:
			return False

	def import_json_record(self, user_email):
		JSON_Processor = JSONProcessor(in_list=self.list_file_json)
		streams_list = JSON_Processor.streams_json_list
		streams_record = {user_email:streams_list}
		if( streams_record is not self.current_record):
			self.current_record = streams_record
			print("New Record selected")
			self.add_record(self.current_record)
		else:
			print("Record already selected")

	def export_json_record(self):
		pass

def main():
	pass

if __name__ == '__main__':
	main()