# importing the required libraries
import json, sys, os
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
		self.sheet = self.client.open('DB 1.0')

		self.current_record = []


	def choose_sheet(self, id):
		self.sheet_instance = self.sheet.get_worksheet(id)


	def add_record(self, record: list):
		pass

	def delete_record(self, record: list):
		pass

	def find_record(self, record: list):
		pass

	def update_record(self, record: list):
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

def import_json(email, file_name):
   from DBHandler import DBHandler
   db_handler = DBHandler()
   db_handler.choose_sheet(0)
   if db_handler.find_file(file_name):
      db_handler.import_json_record(user_email=email)
      print("File Found fileserver.py")

def main():
	import_json(email="maxwellkret@gmail.com", file_name="DBHandler.json")

if __name__ == '__main__':
	main()