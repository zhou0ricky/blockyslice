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

	def move(self):
		self.position[0] += self.velocity[0]
		self.position[1] += self.velocity[1]
		self.velocity[1] += gravity
		self.rotation += 0.1

def main():
	pygame.init()
	screenSize = [800, 600]

	screen = pygame.display.set_mode(screenSize)
	clock = pygame.time.Clock()

	pygame.display.set_caption("Blocky Slice")

	running = True

	polygon = Polygon(screenSize)

	while(running):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False

		clock.tick(60)
		screen.fill([255, 255, 255])

		pygame.gfxdraw.filled_polygon(screen, polygon.transformPoints(), [0, 0, 0])

		polygon.move()

		if polygon.position[1] > screenSize[1]:
			polygon = Polygon(screenSize)

		pygame.display.flip()

		#print(clock.get_fps())

	pygame.quit()

main()
