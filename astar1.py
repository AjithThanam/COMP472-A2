import copy
import random
from node import Node
from queue import PriorityQueue
from timer import Timer


def main():
	# val = input("Enter your value: ")
	#val = '((3; 2); (4; 1))'
	val = '((9; 2; 3); (4; 5; 6); (7; 8; 1))'
	#val = '((1; 2; 10; 7); (8; 3; 11; 14); (4; 9; 12; 5); (15; 13; 16; 6))'
	#val = '((25; 1; 2; 10; 17); (7; 8; 3; 11; 21); (5; 4; 9; 12; 20); (14; 15; 13; 16; 19); (6; 24; 23; 22; 18))'
	#val = '((25; 1; 2; 10; 17; 26); (7; 8; 3; 11; 21; 27); (5; 4; 9; 12; 20; 28); (14; 15; 13; 16; 19; 29); (6; 24; 23; 22; 18; 30); (32; 31; 33; 35; 34; 36))'
	#val = '((25; 1; 2; 10; 17; 26; 37); (7; 8; 3; 11; 21; 27; 38); (5; 4; 9; 12; 20; 28; 39); (14; 15; 13; 16; 19; 29; 40); (6; 24; 23; 22; 18; 30; 41); (32; 31; 33; 35; 34; 36; 42); (44; 43; 49; 48; 47; 46; 45))'
	
	input_list = get_list(parse_input(val))
	
	node = Node(input_list, [], 0, 12)
	start_a1(node)
	
def start_a1(start_node):
	# solution_node = [[1, 2], [3, 4]
	solution_node = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	#solution_node = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
	#solution_node = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
	#solution_node = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24], [25, 26, 27, 28, 29, 30], [31, 32, 33, 34, 35, 36]]
	#solution_node = [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14], [15, 16, 17, 18, 19, 20, 21], [22, 23, 24, 25, 26, 27, 28], [29, 30, 31, 32, 33, 34, 35], [36, 37, 38, 39, 40, 41, 42], [43, 44, 45, 46, 47, 48, 49]]
	open_queue = PriorityQueue()
	closed_stack = []
	max_depth = 10
	counter = 0
	t = Timer()
	t.start()

	open_queue.put((start_node.f_score, counter, start_node))
	counter += 1

	while(open_queue.not_empty):

		if t.getTime() >= 60:
			t.maxTime()
			return False, 0, 0, 0, 0

		if len(closed_stack) == 0:
			current_node = open_queue.get()[2]
			closed_stack.append(current_node)
		else:
			#print(current_node.state)
			closed_stack.append(current_node)
			current_node = open_queue.get()[2]

		if(current_node.state == solution_node):
			print("*************************************************")
			print("Solution State Reached: " + str(current_node.state))
			print("Parent State: " + str(current_node.parent.state))
			print("*************************************************")
			output_solution_path(current_node)
			output_search_path(closed_stack)
			elapsed_time = t.getTime()
			t.stop()
			return True, elapsed_time, len(closed_stack), current_node.depth+1, total_fscore(closed_stack)

		children = generateChildren(current_node)

		for node in children:
			if t.getTime() >= 60:
				t.maxTime()
				return False, 0, 0, 0, 0
			if current_node.depth == 0:
				open_queue.put((node.f_score, counter, node))
				counter += 1
			elif not is_in_stack(node.state, closed_stack):
				open_queue.put((node.f_score, counter, node))
				counter += 1
			
		closed_stack.append(current_node)


def output_solution_path(node):
	new_file = open("output_files/A1/solution_path.txt","w+")
	dimension = len(node.state)
	solution_path = node.get_solution_path()
	ctr = 0

	for state in solution_path:
		while(ctr < dimension):
			new_file.write(str(state.state[ctr]) + "\n")
			ctr +=1

		new_file.write("\n")
		ctr = 0

def output_search_path(closed_stack):
	new_file = open("output_files/A1/search_path.txt","w+")
	dimension = len(closed_stack[0].state)
	ctr = 0

	for i in reversed(closed_stack):
		while(ctr < dimension):
			new_file.write(str(i.state[ctr]) + "\n")
			ctr +=1

		new_file.write("\n")
		ctr = 0
			
def is_in_stack(state, stack):
	for i in range(len(stack)):
		if state == stack[i].state:
			return True
	return False

# convert input string to a tuple
def parse_input(inputStr):
	inputStr = eval(inputStr.replace(';', ','))
	return inputStr

# converts tuple to a list, since tuples are immutable
def get_list(tup):
	return list(map(get_list, tup)) if isinstance(tup, (list, tuple)) else tup

# returns index of a number in a nested list as a list of size 2
def get_index(input_list, num):
	for sub_list in input_list:
		if num in sub_list:
			return (input_list.index(sub_list), sub_list.index(num))
	raise ValueError("'{num}' is not in list".format(num=num))

# -----------------------SWAPING METHODS-----------------------
def swap_left(input_list, current_index):
	list_copy = copy.deepcopy(input_list)
	num_temp = list_copy[current_index[0]][current_index[1]+1]
	list_copy[current_index[0]][current_index[1] +
								1] = list_copy[current_index[0]][current_index[1]]
	list_copy[current_index[0]][current_index[1]] = num_temp
	return list_copy


def swap_right(input_list, current_index):
	list_copy = copy.deepcopy(input_list)
	num_temp = list_copy[current_index[0]][current_index[1]-1]
	list_copy[current_index[0]][current_index[1] -
								1] = list_copy[current_index[0]][current_index[1]]
	list_copy[current_index[0]][current_index[1]] = num_temp
	return list_copy

def swap_up(input_list, current_index):
	list_copy = copy.deepcopy(input_list)
	num_temp = list_copy[current_index[0]-1][current_index[1]]
	list_copy[current_index[0]-1][current_index[1]
								  ] = list_copy[current_index[0]][current_index[1]]
	list_copy[current_index[0]][current_index[1]] = num_temp
	return list_copy


def swap_down(input_list, current_index):
	list_copy = copy.deepcopy(input_list)
	num_temp = list_copy[current_index[0]+1][current_index[1]]
	list_copy[current_index[0]+1][current_index[1]
								  ] = list_copy[current_index[0]][current_index[1]]
	list_copy[current_index[0]][current_index[1]] = num_temp
	return list_copy

# -------------SWAP CHECKING METHODS-------------

def can_swap_left(current_index, dimension):
	if(current_index[1] == dimension - 1):
		return False
	else:
		return True


def can_swap_right(current_index):
	if(current_index[1] == 0):
		return False
	else:
		return True

def can_swap_up(current_index):
	if(current_index[0] == 0):
		return False
	else:
		return True

def can_swap_down(current_index, dimension):
	if(current_index[0] == dimension - 1):
		return False
	else:
		return True

# Generate all 12 child nodes for given parent node

def generateChildren(parent_node):
	input_list = parent_node.state
	possible_moves = []
	dimension = len(input_list)
	for row in input_list:
		for j in row:
			index = get_index(input_list, j)
			if(can_swap_left(index, dimension)):
				move = swap_left(input_list, index)
				if move not in possible_moves:
					possible_moves.append(move)
			if(can_swap_right(index)):
				move = swap_right(input_list, index)
				if move not in possible_moves:
					possible_moves.append(move)
			if(can_swap_up(index)):
				move = swap_up(input_list, index)
				if move not in possible_moves:
					possible_moves.append(move)
			if(can_swap_down(index, dimension)):
				move = swap_down(input_list, index)
				if move not in possible_moves:
					possible_moves.append(move)

	nodes = create_nodes(possible_moves, parent_node)
	random.shuffle(nodes)
	return nodes


def total_fscore(closed_stack):
	total = 0
	for node in closed_stack:
		total += node.f_score

	return total

def create_nodes(states_list, parent_node):
	nodes = []
	for state in states_list:
		f_value = manhattan_distance(state) + parent_node.depth+1
		node = Node(state, parent_node, parent_node.depth+1, f_value)
		nodes.append(node)

	return nodes

def manhattan_distance(state):
	count = 0
	for row in state:
		for value in row:
			count = count + get_distance(state, value)

	return count

def get_distance(state, num):
	solution_state = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
	#solution_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
	#solution_state = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15], [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]]
	#solution_state = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24], [25, 26, 27, 28, 29, 30], [31, 32, 33, 34, 35, 36]]
	#solution_state = [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14], [15, 16, 17, 18, 19, 20, 21], [22, 23, 24, 25, 26, 27, 28], [29, 30, 31, 32, 33, 34, 35], [36, 37, 38, 39, 40, 41, 42], [43, 44, 45, 46, 47, 48, 49]]
	solution_index = get_index(solution_state, num)
	num_index = get_index(state, num)
	temp1 = abs(solution_index[0] - num_index[0])
	temp2 = abs(solution_index[1] - num_index[1])
	# solution_value = solution_index[0] + solution_index[1]
	# num_value = num_index[0] + num_index[1]

	return temp1 + temp2


if __name__ == '__main__':
	main()
