import pygame.gfxdraw
import math
import random
import copy


gravity = 0.1
triangle = [
	[-50, 50], [0, -35], [50, 50]
]
rectangle = [
	[-25, 50], [-25, -50], [25, -50], [25, 50]
]
rightTriangle = [
	[-50, 50], [-50, -50], [50, 50]
]
hexagon = [
	[-50, 0], [-30, -50], [30, -50], [50, 0], [30, 50], [-30, 50]
]
shape1 = [
	[-50, 50], [-50, -50], [0, -50], [50, 50]
]
shape2 = [
	[-50, -50], [-25, -50], [50, 25], [50, 50], [25, 50], [-50, -25]
]
shape3 = [
	[-50, 50], [-50, 0], [0, -50], [50, -50], [50, 50]
]

shapes = [triangle, rectangle, rightTriangle, hexagon, shape1, shape2, shape3]

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
			velocity = [random.randint(-10, 10) / 0.25, random.randint(-10, 10) / 0.25]
			if calculateArea(half1) > calculateArea(half2):
				self.points = half1
				polygons.append(Polygon(half2, copy.copy(self.position), velocity, self.rotation, self.rotationRate, (155, 100, 100)))
			else:
				self.points = half2
				polygons.append(Polygon(half1, copy.copy(self.position), velocity, self.rotation, self.rotationRate, (155, 100, 100)))
			self.recenter()
			return True
		return False

	def move(self, time):
		self.position[0] += self.velocity[0] * time
		self.position[1] += self.velocity[1] * time
		self.velocity[1] += gravity * time
		self.rotation += self.rotationRate * time

def createTarget(screenSize):
	points = shapes[random.randint(0, len(shapes) - 1)]
	position = [screenSize[0] - 70, 55]
	return Polygon(points, position, [0, 0], 0, 0, (215, 0, 0))

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
	return Polygon(points, position, velocity, rotation, rotationRate, (215, 0, 0))


import numpy as np

# outputs list of angles based on points given
def findAngles(points):
	angleList = []
	for index in range(len(points)):
		a = np.array(points[index - 1])
		b = np.array(points[index])
		c = np.array(points[(index + 1) % len(points)])

		ba = a - b
		bc = c - b
		
		cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
		angle = np.arccos(cosine_angle)
		angleList.append(angle)

	return angleList

def findLengths(points):
	lengthList = []
	for index in range(len(points)):
		a = np.array(points[index])
		b = np.array(points[(index + 1) % len(points)])
		length = np.linalg.norm(a-b)
		lengthList.append(length)
	return lengthList

# compares 2 list of angles and scores based on differences
def angleScore(angleList1, angleList2):
	if len(angleList1) > len(angleList2):
		(big, small) = (angleList1, angleList2)
	else:
		(big, small) = (angleList2, angleList1)
	scoreList = []

	for i in range(len(big)):
		add = 0
		for j in range(len(small)):
			add += abs(small[j] - big[j])
		scoreList.append(add)
		big.insert(0, big.pop())
	return int(min(scoreList) * 100 / len(angleList2))

def lengthScore(lengthList1, lengthList2):
	if len(lengthList1) > len(lengthList2):
		(big, small) = (lengthList1, lengthList2)
	else:
		(big, small) = (lengthList2, lengthList1)
	scoreList = []
	if sum(big) > sum(small):
		scale = sum(big) / sum(small)
	else:
		scale = sum(small) / sum(big)
	for i in range(len(big)):
		add = 0
		for j in range(len(small)):
			add += abs(small[j] - big[j])
		scoreList.append(add)
		big.insert(0, big.pop())
	return int(min(scoreList) / (scale * len(lengthList2)))

def comparison(alist1, alist2, llist1, llist2):
	return (angleScore(alist1, alist2) + lengthScore(llist1, llist2))

def createParticle(polygons, position, color):
	points = [
		[-3, -3], [-3, 3],
		[3, 3], [3, -3]
	]
	velocity = [random.randint(-10, 10) / 5, random.randint(-10, 10) / 5]
	polygons.append(Polygon(points, position, velocity, 0, 0.1, color))

pygame.init()
screenSize = [1080, 760]

screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
font = pygame.font.Font("eggroll.ttf", 64)

pygame.display.set_caption("Blocky Slice")

running = True
mode = 0
nextMode = 0

time = 1

polygon = createPolygon(screenSize)
polygons = []

focus = 0.5

cutting = False
firstCut = []
secondCut = []

#graphics
particlePos = -1
background = pygame.image.load("background.png")
go = pygame.image.load("GO!.png")
splashTitle = pygame.image.load("Splash title (Textcraft).png")
focusBarOuterRect = [(0, screenSize[1] / 16),
				(screenSize[0] / 16, screenSize[1] / 16), 
				(screenSize[0] / 16, screenSize[1] - screenSize[1] / 16),
				(0, screenSize[1] - screenSize[1] / 16)]
focusBarInnerRect = [[screenSize[0] / 80, screenSize[1] / 12],
				[screenSize[0] / 20, screenSize[1] / 12], 
				[screenSize[0] / 20, screenSize[1] - screenSize[1] / 12],
				[screenSize[0] / 80, screenSize[1] - screenSize[1] / 12]]
targetText = font.render("Target: ", True, (75, 75, 75))
targetTextRect = targetText.get_rect().move(750, 30)
target = createTarget(screenSize)

buttonBox = [-150, 50], [-150, -50], [150, -50], [150, 50]
creativeBox = Polygon(buttonBox, [150, 300], [0, 0], 0, 0.3, (215, 0, 0))
creativeBoxText = font.render("Creative", True, (75, 75, 75))
creativeBoxTextRect = creativeBoxText.get_rect().move(75, 265)
survivalBox = Polygon(buttonBox, [150, 500], [0, 0], 0, 0.3, (215, 0, 0))
survivalBoxText = font.render("Survival", True, (75, 75, 75))
survivalBoxTextRect = survivalBoxText.get_rect().move(75, 465)
polygons = [creativeBox, survivalBox]

#sound
gameSong = pygame.mixer.Sound("Speed Round Loop.wav")
slashUp = pygame.mixer.Sound("UpSlash.wav")
slashDown = pygame.mixer.Sound("Short Down Slash.wav")
tutorialMusic = pygame.mixer.Sound("Creative-Tutorial.wav")
senseiTalking = pygame.mixer.Sound("senseiTalking.wav")
survivalIntro = pygame.mixer.Sound("Speed Round Intro.wav")
survivalTheme = pygame.mixer.Sound("Speed Round Loop.wav")
splashIntro = pygame.mixer.Sound("Splash Music Intro.wav")
splashLoop = pygame.mixer.Sound("Splash Music LOOP.wav")
creativeTheme = pygame.mixer.Sound("Tutorial.wav")

# class Music(object):
music = pygame.mixer.Channel(0)

while(running):
	clock.tick(60)

	####################################################################################################
	#Splash Screen
	####################################################################################################
	if mode == 0:
		if not pygame.mixer.get_busy():
			music.play(splashIntro)	
			music.queue(splashLoop)
		if music.get_sound() == splashLoop:
			music.queue(splashLoop)

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
				cbs = creativeBox.slice([firstCut, secondCut], polygons)
				sbs = survivalBox.slice([firstCut, secondCut], polygons)
				if cbs or sbs:
					creativeBox.rotationRate = -0.3
					survivalBox.rotationRate = -0.3
					for poly in polygons:
						poly.velocity = [-25, -0.4]
					creativeBox.velocity = [25, -0.4]
					survivalBox.velocity = [20, -0.8]
					if cbs:
						nextMode = 3
					else:
						nextMode = 4
					mode = 2
				particlePos = 0
				if secondCut[1] > firstCut[1]:
					slashDown.play()
				else:
					slashUp.play()
		secondCut = pygame.mouse.get_pos()

		screen.blit(background, [0, 0, screenSize[0], screenSize[1]])

		for i in range(len(polygons) - 1, -1, -1):
			poly = polygons[i]
			pygame.gfxdraw.filled_polygon(screen, transformPoints(poly.points, poly.position, poly.rotation), poly.color)

		screen.blit(creativeBoxText, creativeBoxTextRect)
		screen.blit(survivalBoxText, survivalBoxTextRect)
		screen.blit(splashTitle, [200, 50, screenSize[0], screenSize[1]])

		if cutting:
			pygame.gfxdraw.line(screen, firstCut[0], firstCut[1], secondCut[0], secondCut[1], [155, 0 ,0])

	####################################################################################################
	#Tutorial Mode
	####################################################################################################
	elif mode == 1:
		pass

	####################################################################################################
	#Buffer Mode
	####################################################################################################
	elif mode == 2:
		music.stop()

			# pygame.mixer.music.queue(survivalTheme)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
		secondCut = pygame.mouse.get_pos()
		screen.blit(background, [0, 0, screenSize[0], screenSize[1]])

		if particlePos != -1:
			for i in range(particlePos, particlePos + 25):
				posX = firstCut[0] * (50 - i) / 50 + secondCut[0] * i / 50
				posY = firstCut[1] * (50 - i) / 50 + secondCut[1] * i / 50
				createParticle(polygons, [posX, posY], (155, 100, 100))
			particlePos += 25
			if particlePos > 50: particlePos = -1

		if len(polygons) == 0:
			mode = nextMode
			polygons.append(polygon)

		for i in range(len(polygons) - 1, -1, -1):
			poly = polygons[i]
			pygame.gfxdraw.filled_polygon(screen, transformPoints(poly.points, poly.position, poly.rotation), poly.color)
			poly.move(time)
			if poly.position[1] > screenSize[1] * 1.25:
				polygons.pop(i)


	####################################################################################################
	#Creative Mode
	####################################################################################################
	elif mode == 3:
		if not pygame.mixer.get_busy():
			music.play(creativeTheme)
		if music.get_sound() == creativeTheme:
			music.queue(creativeTheme)


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
				polygon.slice([firstCut, secondCut], polygons)
				particlePos = 0
				if secondCut[1] > firstCut[1]:
					slashDown.play()
				else:
					slashUp.play()
		secondCut = pygame.mouse.get_pos()

		screen.blit(background, [0, 0, screenSize[0], screenSize[1]])
		
		focusBarTargetInnerHeight = focus * (screenSize[1] / 12) + (1 - focus) * (screenSize[1] - screenSize[1] / 12)
		focusBarInnerHeight = (focusBarTargetInnerHeight + focusBarInnerRect[0][1] * 7) / 8
		focusBarInnerRect[0][1] = focusBarInnerHeight
		focusBarInnerRect[1][1] = focusBarInnerHeight
		pygame.gfxdraw.filled_polygon(screen, focusBarOuterRect, (0, 0, 0, 155))
		pygame.gfxdraw.filled_polygon(screen, focusBarInnerRect, (150, 150, 215))
		
		if particlePos != -1:
			for i in range(particlePos, particlePos + 25):
				posX = firstCut[0] * (50 - i) / 50 + secondCut[0] * i / 50
				posY = firstCut[1] * (50 - i) / 50 + secondCut[1] * i / 50
				createParticle(polygons, [posX, posY], (155, 100, 100))
			particlePos += 25
			if particlePos > 50: particlePos = -1

		for i in range(len(polygons) - 1, -1, -1):
			poly = polygons[i]
			pygame.gfxdraw.filled_polygon(screen, transformPoints(poly.points, poly.position, poly.rotation), poly.color)
			poly.move(time)
			if poly.position[1] > screenSize[1] * 1.25:
				
				polygons.pop(i)

		if cutting:
			pygame.gfxdraw.line(screen, firstCut[0], firstCut[1], secondCut[0], secondCut[1], [155, 0 ,0])
			time = (0.1 + time) / 2
			focus -= 0.002
			createParticle(polygons, [random.randint(int(screenSize[0] / 80), int(screenSize[0] / 20)), focusBarInnerHeight], (150, 150, 215))
		else:
			time = (1 + time) / 2

		if polygon.position[1] > screenSize[1] * 1.25:
			angles1 = findAngles(poly.points)
			angles2 = findAngles(target.points)
			length1 = findLengths(poly.points)
			length2 = findLengths(target.points)
			score = (comparison(angles1, angles2, length1, length2))
			if score < 30:
				focus += 0.3
			elif score < 40:
				focus += 0
			else:
				focus -= 0.1
			polygon = createPolygon(screenSize)
			polygons = [polygon] + polygons
			target = createTarget(screenSize)


		screen.blit(targetText, targetTextRect)
		pygame.gfxdraw.filled_polygon(screen, transformPoints(target.points, target.position, target.rotation), target.color)

	####################################################################################################
	#Survival Mode
	####################################################################################################
	elif mode == 3:
		if not pygame.mixer.get_busy():
			music.play(survivalIntro)
			music.queue(survivalTheme)
		if music.get_sound() == survivalTheme:
			music.queue(survivalTheme)

	pygame.display.flip()

print(clock.get_fps())
pygame.quit()
