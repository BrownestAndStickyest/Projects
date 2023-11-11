# necessary packages
import pygame

class Particle:

	# constructor
	def __init__(self,screen,colour,radius,inflRad,pos,vel,dt):
		self.radius = radius
		self.inflRad = inflRad
		self.pos = pos
		self.screen = screen
		self.colour = colour
		self.vel = vel
		self.dt = dt

	# draw the particle
	def illustrate(self):
		pygame.draw.circle(self.screen,self.colour,self.pos,self.radius)

	# show the influences of each particle as well
	def illustrateInfl(self):
		pygame.draw.circle(self.screen,pygame.Color(255,0,0,a = 10),self.pos,self.inflRad)

	### the following methods get values of a particle
	# returns the size of the particle
	def getSize(self):
		return self.size

	# returns the position of the particle
	def getPos(self):
		return self.pos

	# returns the position of the particle
	def getVel(self):
		return self.vel

	# returns the thought new position of the particle
	def getNewPos(self):
		v = pygame.Vector2(self.vel.x,self.vel.y)
		temp = self.pos + self.dt*v

		if(temp.x < 0 or temp.x > self.screen.get_width()):
			v.x = -0.9*v.x
		if(temp.y < 0 or temp.y > self.screen.get_height()):
			v.y = -0.9*v.y

		return self.pos + self.dt*v

	# returns the colour of the particle
	def getColour(self):
		return self.colour

	### the following methods sets the particles attributes directly 
	# set the size of the particle
	def setSize(self,size):
		self.size = size

	# set the position of the particle
	def setPos(self,pos):
		self.pos = pos

	# set the velocity of the particle
	def setVel(self,vel):
		self.vel = vel

	# set the colour of the particle
	def setColour(self,colour):
		self.colour = colour 

	### the next are related to the physics and the appearence
	# moves a particles according to its current velocity, considers bouncing against walls
	def updatePos(self):

		# rectangular geometry:
		temp = self.pos + self.dt*self.vel

		if(temp.x < 0 or temp.x > self.screen.get_width()):
			self.vel.x = -0.6*self.vel.x
		if(temp.y < 0 or temp.y > self.screen.get_height()):
			self.vel.y = -0.6*self.vel.y

		# circular geometry:

		self.pos = self.pos + self.dt*self.vel

	# updates a particles velocity according to a force
	def updateVel(self,force):
		self.vel = self.vel + self.dt*force

	# rescales in case the particle is too quick
	def fixVel(self,m):
		if(self.vel.length() > m):
			self.vel = (m/self.vel.length())*self.vel
