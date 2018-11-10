import pygame.gfxdraw
import math
import random

gravity = 0.1

class Polygon(object):
	def __init__(self, screenSize):
		self.points = [
			[-30, -30], [-30, 30],
			[30, 30], [30, -30]
		]

		posX = random.randint(0, screenSize[0])
		toTravel = screenSize[0] / 2 - posX
		posY = screenSize[1]
		velY = -10
		velX = toTravel / (-velY / gravity)

		self.position = [posX, posY]
		self.velocity = [velX, velY]
		self.rotation = 0

	def transformPoints(self):
		newPoints = []
		c = math.cos(self.rotation)
		s = math.sin(self.rotation)
		for point in self.points:
			x = point[0]
			y = point[1]
			nx = x * c - y * s
			ny = y * c + x * s
			newPoints.append([nx + self.position[0],
							ny + self.position[1]])
		return newPoints

	def move(self, time):
		self.position[0] += self.velocity[0] * time
		self.position[1] += self.velocity[1] * time
		self.velocity[1] += gravity * time
		self.rotation += 0.1 * time

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
		secondCut = pygame.mouse.get_pos()

		clock.tick(60)
		screen.fill([255, 255, 255])

		pygame.gfxdraw.filled_polygon(screen, polygon.transformPoints(), [0, 0, 0])
		
		if cutting:
			pygame.gfxdraw.line(screen, firstCut[0], firstCut[1], 
								secondCut[0], secondCut[1], [0, 0 ,0])
			time = (0.1 * 4 + time) / 5
		else:
			time = (4 + time) / 5


		polygon.move(time)

		if polygon.position[1] > screenSize[1]:
			polygon = Polygon(screenSize)

		pygame.display.flip()

		#print(clock.get_fps())

	pygame.quit()

main()
