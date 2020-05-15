import io
from src.projects import project1cs360s2020 as project1
from src.projects import project2cs360s2020 as project2
from src.projects import project3cs360s2020 as project3

"""
ProjectInterface - bridge class containing static methods to interface with
				   various projects from CSCI 360
"""
class ProjectInterface :

	@staticmethod
	def runSearch(body) :
		"""
		runSearch - handles project 1 searches following project 1 guidelines
			- vars below refer to following:
				n => matrix will be nxn
				d => # drones need to place
				p => total # packages
				alg => type of algorithm (allowed values dfs or astar)
				packages => array of string coordinates of packages

		:param dict body
		:return True if successful, False otherwise
		"""
		n, d, p, alg, packages = None, None, None, None, []
		try :
			f = io.StringIO(body)
			n = int((f.readline()).split('\n')[0])
			d = int((f.readline()).split('\n')[0])
			p = int((f.readline()).split('\n')[0])
			alg = (f.readline()).split('\n')[0]
			for line in f :
				coords = line.split('\n')[0]
				packageCoords = (int(coords.split(',')[0]), int(coords.split(',')[1]))
				packages.append(packageCoords)
			packages = project1.getPackageInfo(packages)
			packagesDict = packages[0]
			numPackages = packages[1]
		except :
			print('Error reading input')
			return None
		ASTAR = False
		if alg.lower() == 'astar' :
			ASTAR = True
		res = None
		if ASTAR :
			res = project1.searchASTAR(packagesDict, d, n, numPackages)
		else :
			res = project1.searchDFS(packagesDict, d, n, numPackages)
		try :
			return res
		except :
			print('Error writing output')
			return None

	@staticmethod
	def runMinimax(body) :
		"""
		runMinimax - runs minimax with or without ab pruning depending on body options

		:param dict request body
		:return string result
		"""
		line_number = 0
		alg_type = ''
		contestants = []
		try :
			f = io.StringIO(body)
			for line in f :
				line_number += 1
				if line_number == 1:
					continue
				if line_number == 2:
					alg_type = line
					continue
				data = line.strip().split(',')
				new_contestant = project2.Contestant(int(data[0]), float(data[1]), float(data[2]), float(data[3]), int(data[4]))
				contestants.append(new_contestant)
			input = [alg_type, contestants]
			all_contestants = project2.get_starting_contestants(input[1])
			res = None
			print(input)
			print(all_contestants)
			if 'minimax' in input[0]:
				res = project2.minimax(all_contestants[0], all_contestants[1], all_contestants[2], len(all_contestants[0]), True)
			else :
				res = project2.ab(all_contestants[0], all_contestants[1], all_contestants[2], len(all_contestants[0]), True)
			return str(res[1].id)
		except:
			print('error reading input')
			return None

	@staticmethod
	def runMdp(body) :
		grid_size = 0
		obstacles = []
		destination = []
		def parse_coords_line(inp) :
			coords = inp.split(',')
			return [int(coord) for coord in coords]

		with io.StringIO(body) as file :
			grid_size = int(file.readline())
			num_obstactles = int(file.readline())
			for i in range(0, num_obstactles) :
				obstacles.append(parse_coords_line(file.readline()))
			destination = parse_coords_line(file.readline())

		initial = project3.initialize_grid(grid_size, obstacles, destination)
		grid = project3.run_value_iteration(initial)
		policy = project3.compute_optimal_policy(grid)
		output_file = ''
		for row in policy :
			output_str = ''
			for col in row :
				output_str += col
			output_file += output_str + '\n'
		return output_file
