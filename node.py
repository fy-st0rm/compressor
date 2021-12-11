
class Node:
	def __init__(self, char, freq, left=None, right=None):
		self.char = char
		self.freq = freq
		self.huff = ""

		# Next nodes
		self.left = left
		self.right = right


def print_nodes(node, huff=""):
	new_huff = huff + str(node.huff)
	
	# if new node exists in the node then go in that node
	if (node.left):
		print_nodes(node.left, new_huff)
	if (node.right):
		print_nodes(node.right, new_huff)
	
	# if its the last node
	if (not node.left and not node.right):
		print(f"{node.char}: {new_huff}")


