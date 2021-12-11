import sys
from node import *


class Compressor:
	def __init__(self, file_name):
		self.file_name = file_name
		self.out_file_name = self.file_name + ".cmp"
		self.file_data = ""

		self.char_freq = {}
		self.nodes = []
		self.huffman_dict = {}

	def __open_file(self):
		with open(self.file_name, "rb") as input_file:
			file_data = input_file.read()
		return file_data

	def __generate_nodes(self):
		# Generates nodes for each unique character in a file

		self.file_data = self.__open_file()

		for ch in self.file_data:
			if ch not in self.char_freq:
				self.char_freq[ch] = 1;
			else:
				val = self.char_freq[ch];
				self.char_freq[ch] = val + 1;
		
		for i in self.char_freq:
			self.nodes.append(Node(i, self.char_freq[i]))
	
	def __generate_huffman(self, node, huff=""):
		# Generates huffman tree for all unique characters and stores it in a dictionary

		new_huff = huff + str(node.huff)
		
		# if new node exists in the node then go in that node
		if (node.left):
			self.__generate_huffman(node.left, new_huff)
		if (node.right):
			self.__generate_huffman(node.right, new_huff)
		
		# if its the last node
		if (not node.left and not node.right):
			self.huffman_dict.update({node.char: new_huff})
		
	def __calculate_huffman(self):
		# Calculates the huffman tree for all the nodes

		while (len(self.nodes) > 1):
			self.nodes = sorted(self.nodes, key = lambda x: x.freq)

			left = self.nodes[0]
			right = self.nodes[1]

			left.huff = 0
			right.huff = 1
			
			new_node = Node(left.char + right.char, left.freq + right.freq, left, right)
			self.nodes.remove(left)
			self.nodes.remove(right)
			self.nodes.append(new_node)

	def __generate_encoded_text(self):
		# Generating encoded text from the huffman tree

		encoded_text = ""
		for ch in self.file_data:
			encoded_text += self.huffman_dict[ch]
		return encoded_text

	def __padd_encoded_text(self, encoded_text):
		# Adding extra padding to create a perfect divisible of 8
		extra_padd = 8 - (len(encoded_text) % 8)
		for padd in range(extra_padd):
			encoded_text += "0"

		# Adding the binary rep of padding infront of the text
		padded_info = "{0:08b}".format(extra_padd)
		encoded_text = padded_info + encoded_text

		return encoded_text

	def __get_byte_array(self, encoded_text):
		b = bytearray()
		for i in range(0, len(encoded_text), 8):
			byte = encoded_text[i:i+8] # Splitting the text with 8 bite each
			b.append(int(byte, 2))
		return b

	def __save_table(self):
		table = "{"
		for ch in self.char_freq:
			table += f"{self.char_freq[ch]}{chr(ch)}"
		table += "}"

		with open(self.out_file_name, "wb") as out:
			out.write(table.encode())

	def run(self):
		self.__generate_nodes()
		self.__calculate_huffman()
		self.__generate_huffman(self.nodes[0])

		self.__save_table()

		encoded_text = self.__generate_encoded_text()
		encoded_text = self.__padd_encoded_text(encoded_text)
		byte_array = self.__get_byte_array(encoded_text)

		with open(self.out_file_name, "ab") as out:
			out.write(bytes(byte_array))
		

if __name__ == "__main__":
	if (len(sys.argv) <= 1):
		print("Usage: comp [filename]")
		exit()
		
	compressor = Compressor(sys.argv[1])
	compressor.run()

