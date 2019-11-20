"""
	Point class models a cell in the Pacman grid.
	It can be a WALL or EMPTY CELL / FOOD CELL.
"""
from math import log
import pdb


class Point:
	def __init__(self, x, y, is_wall):
		self.x = x
		self.y = y
		self.is_wall = is_wall
		self.morton_key = encode_coord(self.x, self.y)

	def __str__(self):
		return "Point: ({0}, {1}), isWall: {2}".format(self.x, self.y, self.is_wall)


"""
	Rectangle class models the boundaries of a QuadTree.
	One can check if a point is inside a rectangle or if it
	intersects with its boundaries.
"""


class Rectangle:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def __str__(self):
		return "Rectangle: ({0}, {1}, {2}, {3})".format(self.x, self.y, self.width, self.height)

	def contains(self, point):
		return (point.x >= self.x) and \
			   (point.x < self.x + self.width) and \
			   (point.y >= self.y) and \
			   (point.y < self.y + self.height)


"""
	A QuadTree is a data structure which holds 4 regions: NW, NE, SW, SE,
	a collection of Point and a Boundary.
"""


class QuadTree:

	def __init__(self, boundary, level):
		self.boundary = boundary
		self.points = []
		self.isDivided = False
		self.children = []
		self.level = level
		self.morton_key = 0

	def __str__(self):
		return "QuadTree: {0}, isDivided: {1}, Level: {2}, morton_key: {3}\nPoints: {4}". \
			format(self.boundary, self.isDivided, self.level, self.morton_key, self.points)

	def show(self):
		print self
		if self.isDivided:
			print "SW: "
			self.children[0].show()
			print "SE: "
			self.children[1].show()
			print "NW: "
			self.children[2].show()
			print "NE: "
			self.children[3].show()

	def update_morton_keys(self):
		if self.level < max_level:
			self.morton_key <<= 2 * (max_level - self.level)
		if self.isDivided:
			self.children[0].update_morton_keys()
			self.children[1].update_morton_keys()
			self.children[2].update_morton_keys()
			self.children[3].update_morton_keys()


	def subdivide(self):
		x = self.boundary.x
		y = self.boundary.y
		width = self.boundary.width
		height = self.boundary.height
		new_level = self.level + 1

		new_width = width / 2
		new_height = height / 2

		sw = QuadTree(Rectangle(x, y, new_width, new_height), new_level)
		se = QuadTree(Rectangle(x + new_width, y, new_width, new_height), new_level)
		nw = QuadTree(Rectangle(x, y + new_height, new_width, new_height), new_level)
		ne = QuadTree(Rectangle(x + new_width, y + new_height, new_width, new_height), new_level)

		sw.morton_key = (self.morton_key << 2)
		se.morton_key = (self.morton_key << 2) | 0x1
		nw.morton_key = (self.morton_key << 2) | 0x2
		ne.morton_key = (self.morton_key << 2) | 0x3

		self.children.append(sw)
		self.children.append(se)
		self.children.append(nw)
		self.children.append(ne)
		self.isDivided = True

	def insert(self, point):
		if not self.boundary.contains(point):
			return False

		if point.is_wall:
			if self.boundary.width * self.boundary.height == 1:  # a wall
				self.points.append(point)
				return True
			else:
				if not self.isDivided:
					self.subdivide()
				for i in range(0, 4):
					if self.children[i].insert(point):
						return True
		else:													# a path tile
			if self.isDivided:
				for i in range(0, 4):
					if self.children[i].insert(point):
						return True
			else:
				self.points.append(point)
				return True

	# Returns the QuadTree with the 'morton_key' equal to 'key'
	def search(self, key):
		if key >= (1 << (2 * max_level)):  # if out of bounds, return root
			return self
		significant_bit = bap(key, self.level + 1)
		while self.isDivided:
			self = self.children[significant_bit]
			if self.level < max_level:
				significant_bit = bap(key, self.level + 1)
			if key == self.morton_key and not self.isDivided:
				return self

		return self

	# Returns a list of quadtrees that are the leaves of the current quadtree
	def search_children(self, suffix):
		if not self.points[0].is_wall:
			if not self.isDivided and self not in res:
				res.append(self)
			else:
				self.children[suffix[0]].search_children(quadrant)
				self.children[suffix[1]].search_children(quadrant)

	def find_boundary_children(self):
		children_keys = []
		for i in range(0, self.boundary.width):
			children_keys.append(encode_coord(self.boundary.x + i, self.boundary.y))
			children_keys.append(encode_coord(self.boundary.x + i, self.boundary.y + self.boundary.height - 1))
		for j in range(0, self.boundary.height):
			children_keys.append(encode_coord(self.boundary.x, self.boundary.y + j))
			children_keys.append(encode_coord(self.boundary.x + self.boundary.width - 1, self.boundary.y + j))
		return set(children_keys)

	def find_neighbours(self, key):
		current = self.search(key)
		print "Current: ", current

		key_candidates = [left(current.morton_key), right(current.morton_key),
						  top(current.morton_key), bot(current.morton_key)]
		print "Key candidates: ", key_candidates

		for quadrant in range(0, 4):
			if key_candidates[quadrant] >= (1 << (2 * max_level)):
				continue

			tmp = self.search(key_candidates[quadrant])
			if current.level == tmp.level and tmp.isDivided:
				tmp.search_children(suffixes[quadrant])
			if not tmp.isDivided and not tmp.points[0].is_wall and tmp != current and tmp not in res:
				res.append(tmp)


# search, find_neighbours, bits at position,
# search_children, array append, decode, encode,
B = [0x5555, 0x3333, 0x0f0f]
S = [1, 2, 4]
suffixes = [[1, 3], [0, 2], [2, 3], [0, 1]]

def split_binary(x):
	x = (x | (x << S[2])) & B[2]
	x = (x | (x << S[1])) & B[1]
	x = (x | (x << S[0])) & B[0]
	return x


def x_coord_from_morton(key):
	x = key & B[0]
	x = (x ^ (x >> S[0])) & B[1]
	x = (x ^ (x >> S[1])) & B[2]
	x = (x ^ (x >> S[2]))
	return x


def y_coord_from_morton(key):
	y = key >> 1
	y = y & B[0]
	y = (y ^ (y >> S[0])) & B[1]
	y = (y ^ (y >> S[1])) & B[2]
	y = (y ^ (y >> S[2]))
	return y


def decode_morton(key):
	return [x_coord_from_morton(key), y_coord_from_morton(key)]


def encode_coord(x, y):
	return split_binary(x) | (split_binary(y) << 1)


def left(key):
	return (((key & 0x5555) - 1) & 0x5555) | (key & 0xAAAA)


def right(key):
	return (((key | 0xAAAA) + 1) & 0x5555) | (key & 0xAAAA)


def top(key):
	return (((key & 0xAAAA) - 1) & 0xAAAA) | (key & 0x5555)


def bot(key):
	return (((key | 0x5555) + 1) & 0xAAAA) | (key & 0x5555)


def bap(key, level):
	return (key >> 2 * (max_level - level)) & 0x03


res = []
max_level = 3

def main():
	walls = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
	boundary = Rectangle(0, 0, 8, 8)
	qtree = QuadTree(boundary, 0)

	for (x, y) in walls:
		p = Point(x, y, True)
		qtree.insert(p)

	for x in range(0, qtree.boundary.width):
		for y in range(0, qtree.boundary.height):
			if (x, y) not in walls:
				p = Point(x, y, False)
				qtree.insert(p)

	qtree.update_morton_keys()
	# qtree.show()

	point = (6, 6)
	morton_key = encode_coord(point[0], point[1])
	qt = qtree.search(morton_key)
	print "QuadTree with morton_key = ({0}, {1}) is {2}".format(point[0], point[1], morton_key)
	# qt.show()

	qtree.find_neighbours(morton_key)
	print "\nres: ", res
	for each in res:
		each.show()

if __name__ == "__main__":
	main()
