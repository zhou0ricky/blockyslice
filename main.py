import pygame.gfxdraw
import math
import random
import copy


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

def calculateArea(points):
		pointsList = points + [points[0]]
		num1 = 0
		num2 = 0
		for i in range(len(points)):
			x1 = pointsList[i][0]
			y1 = pointsList[i+1][1]
			num1 += x1*y1
			y2 = pointsList[i][1]
			x2 = pointsList[i+1][0]
			num2 += x2*y2
		return abs(num1 - num2) / 2

class Polygon(object):
	def __init__(self, points, position, velocity, rotation, rotationRate, color):
		self.points = points
		self.position = position
		self.velocity = velocity
		self.rotation = rotation
		self.rotationRate = rotationRate
		self.color = color

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

	def slice(self, line, polygons):
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
			half2 = [intersectionPoints[1]]
			for i in range(intersectionEdgeNums[0] + 1, intersectionEdgeNums[1] + 1):
				half1.append(self.points[i])
			for i in range(intersectionEdgeNums[1] + 1, len(self.points) + intersectionEdgeNums[0] + 1):
				half2.append(self.points[i % len(self.points)])
			half1.append(intersectionPoints[1])
			half2.append(intersectionPoints[0])
			vel2 = copy.copy(self.velocity)
			#self.velocity[0] += 0.5
			#vel2[0] -= 0.5
			if calculateArea(half1) > calculateArea(half2):
				self.points = half1
				polygons.append(Polygon(half2, copy.copy(self.position), vel2, self.rotation, self.rotationRate, (100, 100, 100)))
			else:
				self.points = half2
				polygons.append(Polygon(half1, copy.copy(self.position), vel2, self.rotation, self.rotationRate, (100, 100, 100)))

	def move(self, time):
		self.position[0] += self.velocity[0] * time
		self.position[1] += self.velocity[1] * time
		self.velocity[1] += gravity * time
		self.rotation += self.rotationRate * time

def createPolygon(screenSize):
	points = [
		[-50, -50], [-50, 50],
		[50, 50], [50, -50]
	]

	posX = random.randint(0, screenSize[0])
	toTravel = screenSize[0] / 2 - posX
	posY = screenSize[1]
	velY = -10
	velX = toTravel / (-velY / gravity)

	position = [posX, posY]
	velocity = [velX, velY]
	rotation = 0.05
	rotationRate = random.randint(-10, 10) / 50
	return Polygon(points, position, velocity, rotation, rotationRate, (0, 0, 0))

def main():
	pygame.init()
	screenSize = [800, 600]

	screen = pygame.display.set_mode(screenSize)
	clock = pygame.time.Clock()

	pygame.display.set_caption("Blocky Slice")

	running = True

	time = 1

	polygon = createPolygon(screenSize)
	polygons = [polygon]

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
				polygon.slice([firstCut, secondCut], polygons);
		secondCut = pygame.mouse.get_pos()

		clock.tick(60)
		screen.fill([255, 255, 255])
		
		for poly in polygons:
			pygame.gfxdraw.filled_polygon(screen, transformPoints(poly.points, poly.position, poly.rotation), poly.color)
			poly.move(time)

		if cutting:
			pygame.gfxdraw.line(screen, firstCut[0], firstCut[1], 
								secondCut[0], secondCut[1], [0, 0 ,0])
			time = (0.1 + time) / 2
		else:
			time = (1 + time) / 2

		if polygon.position[1] > screenSize[1]:
			polygon = createPolygon(screenSize)
			polygons = [polygon]

		pygame.display.flip()

	pygame.quit()

main()
