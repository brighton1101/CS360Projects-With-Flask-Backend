"""
Brighton Balfrey
balfrey@usc.edu
CS360 - Intro to AI
Assignment 1

Use Python3 to run this exclusively.

Note that design was not taken into account here. There could be a lot done to clean up
the code below.
"""
import copy
import sys
import heapq

"""
:class State

Node representing the current state within the search
"""
class State:

	"""
	constructor - initializes all class values
				- note that some of these could have been globals and the code would have been cleaner
	"""
	def __init__(self, remainingPackages, numDrones, drones, gridSize, currNumPackages, ASTAR, remainingNumPackages) :
		"""
		:param remainingPackages dictionary - maps tuple of (row, col) => number of packages at location
		:param numDrones int - number of drones that still need to be placed
		:param drones set - locations of current drones
		:param gridSize int - the matrix is (gridSize x gridSize)
		:param currNumPackages int - the current number of packages that have been collected up to this state
		:param ASTAR bool - whether or not search is ASTAR
		:param remainintNumPackages int - remaining number of packages that could potentially be picked up 
		"""
		self.remainingPackages = remainingPackages
		self.numDrones = numDrones
		self.drones = drones
		self.gridSize = gridSize
		self.currNumPackages = currNumPackages
		self.ASTAR = ASTAR
		self.remainingNumPackages = remainingNumPackages

	"""
	removeIntersection - given a location tuple/array (row, col), get remainingPackages that would
						 still work with the given action
	"""
	def removeIntersection(self, location) :
		"""
		:param location array/tuple - (row, col) where the drone is going to be placed
		:return list - remainingPackages dict listing out possible packages, remainingNumPackages int count of
					   possible remaining packages
		"""
		remainingPackages = {}
		packageKeys = self.remainingPackages.keys()
		remainingNumPackages = 0
		# Remove initial intersecting drones based on location
		for package in packageKeys :
			if location[0] == package[0] :
				continue
			if location[1] == package[1] :
				continue
			if abs((package[0]-location[0]) / (package[1]-location[1])) == 1 :
				continue
			remainingNumPackages += self.remainingPackages[package]
			remainingPackages[package] = self.remainingPackages[package]
		return [remainingPackages, remainingNumPackages]


	"""
	getChildren - gets possible children of state
	"""
	def getChildren(self) :
		"""
		:return children array - array of child states
		"""
		if self.numDrones < 1 :
			return []
		if len(self.remainingPackages) < 1 :
			return self.placeRemainingDrones()
		children = []

		# Add a "blank" child - you won't place on packages this time, and next iteration
		# you will just try to place all the drones in valid locations and return
		if len(self.drones) > 0 :
			newDrones = (copy.deepcopy(self.drones))
		else :
			newDrones = set()
		children.append(createState({}, self.numDrones, newDrones, self.gridSize, self.currNumPackages, self.ASTAR, 0))
		
		# iterate through remaining packages, and create state with drone at each location
		packageKeys = self.remainingPackages.keys()
		for package in packageKeys :
			newValidPackages = self.removeIntersection(package)
			newValidPackageDict = newValidPackages[0]
			totalNewValidPackages = newValidPackages[1]
			if len(self.drones) > 0 :
				newDrones = (copy.deepcopy(self.drones))
				newDrones.add((package[0], package[1]))
			else :
				newDrones = set()
				newDrones.add((package[0], package[1]))
			children.append(createState(newValidPackageDict, self.numDrones - 1, newDrones, self.gridSize, self.currNumPackages+self.remainingPackages[(package[0], package[1])], self.ASTAR, totalNewValidPackages))
		return children

	"""
	isValidRow - checks to see if given row is still valid
	"""
	def isValidRow(self, row) :
		"""
		:param row int - row to check to see if drone exists at
		:return True if valid, False otherwise
		"""
		for drone in self.drones :
			if row == drone[0] :
				return False
		return True

	"""
	isValidDiagCol - checks to see if diagonals/cols are valid
	"""
	def isValidDiagCol(self, i, j) :
		"""
		:param i int - the row to check
		:param j int - the col to check
		:return bool - True if valid, False otherwise
		"""
		for drone in self.drones :
			if j == drone[1] :
				return False
			if abs((drone[0] - i)/(drone[1] - j)) == 1 :
				return False
		return True

	"""
	placeRemainingDrones - place remaining drones given no more valid remaining packages
	"""
	def placeRemainingDrones(self) :
		"""
		:return array - possible children states
		"""
		children = []
		if self.numDrones == 0 :
			return []
		for i in range(0, self.gridSize) :
			if not self.isValidRow(i) :
				continue
			for j in range(0, self.gridSize) :
				if not self.isValidDiagCol(i, j) :
					continue
				if len(self.drones) > 0 :
					newDrones = (copy.deepcopy(self.drones))
					newDrones.add((i, j))
				else :
					newDrones = set()
					newDrones.add((i, j))
				children.append(createState({}, self.numDrones - 1, newDrones, self.gridSize, self.currNumPackages, self.ASTAR, 0))
		return children

	"""
	comparison - used for astar, overestimates amount of potential packages
	"""
	def __lt__(self, other) :
		"""
		:return bool
		"""
		return (15*self.currNumPackages + 20*self.remainingNumPackages) > (15*other.currNumPackages + 20*other.remainingNumPackages)


"""
createState - wrapper for creating a state
"""
def createState(remainingPackages, numDrones, drones, gridSize, currNumPackages, ASTAR, totalNewValidPackages) :
	"""
	:see State constructor as it matches these params exactly
	:return State - new state
	"""
	return State(remainingPackages, numDrones, drones, gridSize, currNumPackages, ASTAR, totalNewValidPackages)

"""
getPackageInfo - gets package dict and total packages
"""
def getPackageInfo(packages) :
	"""
	:param array - list of packages
	"""
	totalPackages = 0
	packageDict = {}
	for package in packages :
		if (package[0], package[1]) in packageDict :
			packageDict[(package[0], package[1])] += 1
		else :
			packageDict[(package[0], package[1])] = 1
		totalPackages += 1
	return [packageDict, totalPackages]

"""
getSolnScore - gets score of given drones/package combo
"""
def getSolnScore(soln, packageDict) :
	"""
	:param soln set - set of drones to check
	:param packageDict dictionary - package dict maps (row, col) to total num packages
	:return int total number of packages covered
	"""
	currNumPackages = 0
	for drone in soln :
		if drone in packageDict :
			currNumPackages += packageDict[drone]
	return currNumPackages

"""
searchASTAR - performs astar search
"""
def searchASTAR(packages, numDrones, gridSize, numPackages) :
	"""
	:param packages dictionary - dictionary mapping (row, col) to number of packages
	:param numDrones int - total number of drones that need to be placed
	:param gridSize int - size of grid (gridSize x gridSize)
	:param numPackages int - total number of packages
	:return int - max number of packages that can be covered by drones
	"""
	seenDroneStates = set()
	solutionDict = copy.deepcopy(packages) if len(packages) > 0 else {}
	initialState = createState(packages, numDrones, set(), gridSize, 0, True, numPackages)
	frontier = []
	heapq.heappush(frontier, initialState)
	solutions = []
	currMaxSolnScore = -sys.maxsize
	currMaxSoln = None
	while len(frontier) > 0 :
		curr = heapq.heappop(frontier)
		children = curr.getChildren()
		if children == None :
			continue
		if len(children) < 1 and len(curr.drones) == numDrones:
			currSolnScore = getSolnScore(curr.drones, solutionDict)
			return currSolnScore
		for child in children :
			childDrones = frozenset(child.drones)
			if (childDrones, child.remainingNumPackages) in seenDroneStates :
				continue
			seenDroneStates.add((childDrones, child.remainingNumPackages))
			heapq.heappush(frontier, child)
	return currMaxSolnScore

"""
searchDFS - performs dfs search
"""
def searchDFS(packages, numDrones, gridSize, numPackages) :
	"""
	:param packages dictionary - dictionary mapping (row, col) to number of packages
	:param numDrones int - total number of drones that need to be placed
	:param gridSize int - size of grid (gridSize x gridSize)
	:param numPackages int - total number of packages
	:return int - max number of packages that can be covered by drones
	"""
	seenDroneStates = set()
	solutionDict = copy.deepcopy(packages) if len(packages) > 0 else {}
	initialState = createState(packages, numDrones, set(), gridSize, 0, False, numPackages)
	frontier = []
	frontier.append(initialState)
	currMaxSolnScore = -sys.maxsize
	currMaxSoln = None
	while len(frontier) > 0 :
		curr = frontier.pop()
		children = curr.getChildren()
		if children == None :
			continue
		if len(children) < 1 and len(curr.drones) == numDrones:
			currSolnScore = getSolnScore(curr.drones, solutionDict)
			if currSolnScore > currMaxSolnScore :
				currMaxSoln = curr
				currMaxSolnScore = currSolnScore
		for child in children :
			childDrones = frozenset(child.drones)
			if (childDrones, child.remainingNumPackages) in seenDroneStates :
				continue
			seenDroneStates.add((childDrones, child.remainingNumPackages))
			childScore = getSolnScore(child.drones, solutionDict)
			if child.remainingNumPackages <= (currMaxSolnScore - childScore) :
				continue
			frontier.append(child)
	return currMaxSolnScore


"""
run: method to process input, run search, and write output
"""
def run() :
		""" 	
		vars below refer to following:
			n => matrix will be nxn
			d => # drones need to place
			p => total # packages
			alg => type of algorithm (allowed values dfs or astar)
			packages => array of string coordinates of packages

		:return True if successful, False otherwise
		"""
		n, d, p, alg, packages = None, None, None, None, []
		try :
			f = open("./input.txt", "r")
			n = int((f.readline()).split('\n')[0])
			d = int((f.readline()).split('\n')[0])
			p = int((f.readline()).split('\n')[0])
			alg = (f.readline()).split('\n')[0]
			for line in f :
				coords = line.split('\n')[0]
				packageCoords = (int(coords.split(',')[0]), int(coords.split(',')[1]))
				packages.append(packageCoords)
			packages = getPackageInfo(packages)
			packagesDict = packages[0]
			numPackages = packages[1]
		except :
			print('Error reading input')
			return
		ASTAR = False
		if alg.lower() == 'astar' :
			ASTAR = True
		res = None
		if ASTAR :
			res = searchASTAR(packagesDict, d, n, numPackages)
		else :
			res = searchDFS(packagesDict, d, n, numPackages)
		try :
			f = open("./output.txt", "w+")
			f.write(str(res))
			f.close()
			return True
		except :
			print('Error writing output')
			return False

if __name__ == "__main__" :
	run()