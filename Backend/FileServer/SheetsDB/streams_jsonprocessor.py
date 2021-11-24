from io import TextIOWrapper
import json
from datetime import datetime
from collections import Counter

class JSONProcessor():

	json_list_in: list
	streams_json_list: list


	def __init__(self, in_list, _out_file=False):
		'''
		default sets out_file to False, keep this unless you require only a file output.
		otherwise set to True
		'''
		self.json_list_in = in_list
		self.process_streams_JSON()

		if _out_file:
			timestamp = str(datetime.now())[:10]
			filename = f"streams_{timestamp}.json"
			self.to_json_file(filename)


	def process_streams_JSON(self) -> None:
		# load json into dict list
		streamsDictList = self.json_list_in

		# remove unused timecode field
		for x in streamsDictList: x.pop("endTime", None)
		
		# get frequencies:
		# count track name occurences
		streamsFreqDict = {x[0]:x[1] for x in Counter([jsonobject["trackName"] for jsonobject in streamsDictList]).most_common()}
		
		# reconstruct json dict with names, 
		# add 'numPlays field',
		# and remove json objects, ignoring names
		namedStreamsDict = {jsonobject["trackName"]:jsonobject for jsonobject in streamsDictList}
		for (key,value) in namedStreamsDict.items():
			namedStreamsDict[key]["numPlays"] = streamsFreqDict[key]		
		streamsDictListUsable = [x[1] for x in namedStreamsDict.items()]
		
		# set streams_dict attr when done
		self.streams_json_list = streamsDictListUsable


	def to_json_file(self, out_file: str) -> None:
		userStreamsJSON = json.dumps(self.streams_json_list)
		with open(out_file, "w") as writefile:
			writefile.writelines(userStreamsJSON)
		writefile.close()
		

def main():
	pass


if __name__ == '__main__':
	main()
