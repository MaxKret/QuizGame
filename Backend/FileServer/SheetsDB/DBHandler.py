'''
Max's DBHandler
'''
# importing the required libraries
import json, sys, os, ast
import pandas as pd
import gspread, gspread.utils
from oauth2client.service_account import ServiceAccountCredentials
sys.path.append(".")
from streams_jsonprocessor import JSONProcessor


class DBHandler:
	'''
	class for handling Sheets DB
	'''

	current_record: dict
	list_file_json = None


	def __init__(self) -> None:
		'''
		creates self.spreadsheet to manipulate DB sheet
		'''
		creds = self.get_creds(scopes=['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'], )

		# authorize the clientsheet 
		self.client = gspread.authorize(creds)
		# get the instance of the Spreadsheet
		self.spreadsheet = self.client.open('DB 1.0')
		
		self.current_record = []


	def get_creds(self, scopes):
		# define the scope
		scope = scopes
		# add credentials to the account
		return ServiceAccountCredentials.from_json_keyfile_name(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'service_account.json'), scope)
		

	def choose_sheet(self, id: int) -> None:
		'''
		ID: int, starting at 0
		0: Main Sheet
		1: nothing yet!
		'''
		self.sheet_instance = self.spreadsheet.get_worksheet(id)


	def insert_record(self, record: dict) -> None:
		foundcell = self.sheet_instance.find(list(record.keys())[0], in_row=1)
		if foundcell : # record exists in table
			idx = foundcell.address
			print("RECORD FOUND AT", idx, ". UPDATING...")
			self.update_record(record, idx)
		else: # record not in table
			first_blank = self.sheet_instance.find("", in_row=1)
			if first_blank:
				idx = first_blank.address
				print("ADDING NEW RECORD AT", idx)
				self.add_record(record, idx)
			else:
				print("NO AVAILABLE SLOTS FOUND")

	def add_record(self, record: dict, idx: str) -> None:
		# convert the json to dataframe
		record_df = pd.DataFrame.from_dict(record)
		# update cell 1 with header, and cells 2+ with stream json objects
		self.sheet_instance.update_acell(idx, str(record_df.columns.values.tolist()[0]))
		self.sheet_instance.update(f"{idx[0]}{int(idx[1])+1}:{idx[0]}", [[str(y) for y in x] for x in record_df.values.tolist()])

	def update_record(self, record: dict, idx: str) -> None:
		self.delete_record(record, idx)
		record_df = pd.DataFrame.from_dict(record)
		data_only_idx = f"{idx[0]}{int(idx[1])+1}:{idx[0]}"
		self.sheet_instance.update(data_only_idx, [[str(y) for y in x] for x in record_df.values.tolist()])
		print("RECORD AT",idx,"UPDATED")


	def delete_record(self, record: dict, idx: str) -> None:
		data_only_idx = f"{idx[0]}{int(idx[1])+1}:{idx[0]}"
		self.sheet_instance.update(data_only_idx, [["" for y in x] for x in pd.DataFrame.from_dict(record).values.tolist()])
		print("RECORD AT",idx,"DELETED")
	
	
	def find_record_by_email(self, email: str) -> dict:
		#TODO add else branch for no record found
		found_record = self.sheet_instance.find(email, in_row=1)
		if found_record:
			idx = found_record.address
			data_only_idx = f"{idx[0]}{int(idx[1])+1}:{idx[0]}"
			return {email:[ast.literal_eval(x[0]) for x in self.sheet_instance.get_values(data_only_idx)]}

	def find_record_by_idx(self, idx: str) -> dict:
		#TODO add else branch for no record found
		email = self.sheet_instance.get(idx)
		if email:
			data_only_idx = f"{idx[0]}{int(idx[1])+1}:{idx[0]}"
			return {email:[ast.literal_eval(x[0]) for x in self.sheet_instance.get_values(data_only_idx)]}
	


	def find_file(self, filename) -> bool:
		if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)):
			print("FILE",filename,"FOUND")
			with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), encoding="utf8") as openfile:
				self.list_file_json = json.load(openfile)
			os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename))
			return True
		else:
			return False

	def import_json_record(self, user_email) -> None:
		JSON_Processor = JSONProcessor(in_list=self.list_file_json)
		streams_list = JSON_Processor.streams_json_list
		streams_record = {user_email:streams_list}
		if( streams_record is not self.current_record):
			self.current_record = streams_record
			print("ATTEMPTING TO ADD NEW RECORD")
			self.insert_record(self.current_record)
		else:
			print("RECORD ALREADY SELECTED")

	def export_json_record(self) -> None:
		pass

def main():
	pass

if __name__ == '__main__':
	main()