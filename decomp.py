import sys
from node import *


class Decompressor:
	def __init__(self, file_name):
		self.file_name = file_name
		self.out_file_name = self.file_name.split(".cmp")

		self.file_data = ""

	def __open_file(self):
		with open(self.file_name, "rb") as input_file:
			self.file_data = input_file.read()

	def run(self):
		pass

if __name__ == "__main__":
	if (len(sys.argv) <= 1):
		print("Usage: decomp [filename]")
		exit()
	
	decompressor = Decompressor(sys.argv[1])
	decompressor.run()

