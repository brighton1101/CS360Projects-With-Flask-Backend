"""
Brighton Balfrey
Project 3
CS360
balfrey@usc.edu	
3228236754
"""

import sys

global epsilon
epsilon = 0.01

global gamma
gamma = 0.9

global goal
goal = []

global obstacles
obstacles = set()

def parse_input(file_location) :
	grid_size = 0
	obstacles = []
	destination = []

	def parse_coords_line(inp) :
		coords = inp.split(',')
		return [int(coord) for coord in coords]

	with open(file_location, 'r') as file :
		grid_size = int(file.readline())
		num_obstactles = int(file.readline())
		for i in range(0, num_obstactles) :
			obstacles.append(parse_coords_line(file.readline()))
		destination = parse_coords_line(file.readline())
	return [grid_size, obstacles, destination]

def output(file_location, policy) :
	with open(file_location, 'w') as file :
		for row in policy :
			output_str = ''
			for col in row :
				output_str += col
			file.write(output_str + '\n')

def initialize_grid(grid_size, obs, dest) :
	initial = [[0 for x in range(grid_size)] for i in range(grid_size)]
	global obstacles
	obstacles = set()
	for obstacle in obs :
		initial[obstacle[1]][obstacle[0]] = -100
		obstacles.add((obstacle[1], obstacle[0]))
	global goal
	goal = [dest[1], dest[0]]
	initial[dest[1]][dest[0]] = 100
	return initial

def calculate_utilities(grid, point) :
	x, y = point
	curr_north = curr_south = curr_east = curr_west = 0
	# Calculate current val at north
	if y - 1 < 0 :
		curr_north = grid[x][y]
	else :
		curr_north = grid[x][y-1]
	# Current val at south
	if y + 1 >= len(grid) :
		curr_south = grid[x][y]
	else :
		curr_south = grid[x][y+1]
	# Current val at east
	if x + 1 >= len(grid) :
		curr_east = grid[x][y]
	else :
		curr_east = grid[x+1][y]
	# Current val at west
	if x - 1 < 0 :
		curr_west = grid[x][y]
	else :
		curr_west = grid[x-1][y]

	# Now calculate the value for each of the moves w probability
	north = south = east = west = 0

	# Closure helper
	def calculate_val(main, others) :
		return_val = 0.7*main
		for other in others :
			return_val += 0.1*other
		return return_val

	north = calculate_val(curr_north, [curr_south, curr_east, curr_west])
	south = calculate_val(curr_south, [curr_north, curr_east, curr_west])
	east = calculate_val(curr_east, [curr_north, curr_south, curr_west])
	west = calculate_val(curr_west, [curr_north, curr_south, curr_east])
	return [north, south, east, west]



def bellman(grid, point) :
	reward = 0
	x, y = point
	if (x, y) in obstacles :
		reward = -101
	elif [x, y] == goal :
		reward = 99
	else :
		reward = -1
	north, south, east, west = calculate_utilities(grid, point)
	return reward + (gamma * max(north, south, east, west))


def run_value_iteration(grid) :
	while True :
		maxChange = -(sys.maxsize)
		for row in range(len(grid)) :
			for col in range(len(grid)) :
				if [row, col] == goal :
					continue
				before = grid[row][col]
				after = bellman(grid, [row, col])
				grid[row][col] = after
				if (abs(after - before) > maxChange) :
					maxChange = abs(after - before)
		if maxChange < epsilon * (1 - gamma) / gamma :
			return grid

def compute_optimal_policy(grid) :
	policy = [['' for x in range(len(grid))] for y in range(len(grid))]
	for row in range(len(grid)) :
		for col in range(len(grid)) :
			if (row, col) in obstacles :
				policy[row][col] = 'o'
			elif [row, col] == goal :
				policy[row][col] = '.'
			else :
				north, south, east, west = calculate_utilities(grid, [row, col])
				max_move = '^'
				max_val = west
				if east > max_val :
					max_move = 'v'
					max_val = east
				if south > max_val :
					max_move = '>'
					max_val = south
				if north > max_val :
					max_move = '<'
					max_val = north
				policy[row][col] = max_move
	return policy

if __name__ == "__main__" :
	grid_size, obstacles, destination = parse_input('./input.txt')
	initial = initialize_grid(grid_size, obstacles, destination)
	grid = run_value_iteration(initial)
	policy = compute_optimal_policy(grid)
	output('./output.txt', policy)
