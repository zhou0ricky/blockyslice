import pygame.gfxdraw
import math
import random

gravity = 0.1

def intersect(line1, line2):
	xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
	ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

	def det(a, b):
		return a[0] * b[1] - a[1] * b[0]

	div = det(xdiff, ydiff)
	if div == 0:
	   return None

	d = (det(*line1), det(*line2))
	x = det(d, xdiff) / div
	y = det(d, ydiff) / div
	if (x >= min(line1[0][0], line1[1][0]) and
		x >= min(line2[0][0], line2[1][0]) and
		x <= max(line1[0][0], line1[1][0]) and
		x <= max(line2[0][0], line2[1][0]) and
		y >= min(line1[0][1], line1[1][1]) and
		y >= min(line2[0][1], line2[1][1]) and
		y <= max(line1[0][1], line1[1][1]) and
		y <= max(line2[0][1], line2[1][1])):
		return [x, y]

def transformPoints(points, position, rotation):
	newPoints = []
	c = math.cos(rotation)
	s = math.sin(rotation)
	for point in points:
		x = point[0]
		y = point[1]
		rx = x * c - y * s
		ry = y * c + x * s
		px = rx + position[0]
		py = ry + position[1]
		newPoints.append([px, py])
	return newPoints

def invertPoints(points, position, rotation):
	newPoints = []
	c = math.cos(-rotation)
	s = math.sin(-rotation)
	for point in points:
		x = point[0]
		y = point[1]
		px = x - position[0]
		py = y - position[1]
		rx = px * c - py * s
		ry = py * c + px * s
		newPoints.append([rx, ry])
	return newPoints


class Polygon(object):
	def __init__(self, screenSize):
		self.points = [
			[-50, -50], [-50, 50],
			[50, 50], [50, -50]
		]

		posX = random.randint(0, screenSize[0])
		toTravel = screenSize[0] / 2 - posX
		posY = screenSize[1]
		velY = -10
		velX = toTravel / (-velY / gravity)

		self.position = [posX, posY]
		self.velocity = [velX, velY]
		self.rotationRate = random.randint(-10, 10) / 50
		self.rotation = 0

	def recenter(self):
		center = [0, 0]
		for point in self.points:
			center[0] += point[0]
			center[1] += point[1]
		center[0] /= len(self.points)
		center[1] /= len(self.points)
		for point in self.points:
			point[0] -= center[0]
			point[1] -= center[1]
		self.position[0] -= center[0]
		self.position[1] -= center[1]

	def slice(self, line):
		newPoints = transformPoints(self.points, self.position, self.rotation)
		intersectionPoints = []
		intersectionEdgeNums = []
		for edgeNum in range(0, len(newPoints)):
			edge = [newPoints[edgeNum], newPoints[(edgeNum + 1) % len(newPoints)]]
			inter = intersect(edge, line)
			if inter != None:
				intersectionPoints.append(inter)
				intersectionEdgeNums.append(edgeNum)
		if len(intersectionPoints) == 2:
			intersectionPoints = invertPoints(intersectionPoints, self.position, self.rotation)
			half1 = [intersectionPoints[0]]
			for i in range(min(intersectionEdgeNums[0], intersectionEdgeNums[1]) + 1,
						max(intersectionEdgeNums[0], intersectionEdgeNums[1]) + 1):
				half1.append(self.points[i])
			half1.append(intersectionPoints[1])
			self.points = half1
			self.recenter()


	def move(self, time):
		self.position[0] += self.velocity[0] * time
		self.position[1] += self.velocity[1] * time
		self.velocity[1] += gravity * time
		self.rotation += self.rotationRate * time

def main():
	pygame.init()
	screenSize = [800, 600]

	screen = pygame.display.set_mode(screenSize)
	clock = pygame.time.Clock()

	pygame.display.set_caption("Blocky Slice")

	running = True

	time = 1

	polygon = Polygon(screenSize)

	cutting = False
	firstCut = []
	secondCut = []

	while(running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				firstCut = pygame.mouse.get_pos()
				cutting = True
			elif event.type == pygame.MOUSEBUTTONUP:
				cutting = False
				polygon.slice([firstCut, secondCut]);
		secondCut = pygame.mouse.get_pos()

		clock.tick(60)
		screen.fill([255, 255, 255])

		pygame.gfxdraw.filled_polygon(screen, transformPoints(polygon.points, polygon.position, polygon.rotation), [0, 0, 0])
		
		if cutting:
			pygame.gfxdraw.line(screen, firstCut[0], firstCut[1], 
								secondCut[0], secondCut[1], [0, 0 ,0])
			time = (0.1 + time) / 2
		else:
			time = (1 + time) / 2


		polygon.move(time)

		if polygon.position[1] > screenSize[1]:
			polygon = Polygon(screenSize)

		pygame.display.flip()

		#print(clock.get_fps())

	pygame.quit()

main()