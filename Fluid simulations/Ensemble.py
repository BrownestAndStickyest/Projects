# necessary packages
import pygame
import math
import random
import sys
from Particle import Particle
from Grid import Grid

class Ensemble:

	# constructor for the ensemble
	def __init__(self,size,screen,radius,inflRad,maxVel,dt,g,press,smooth,mus):

		# our initial variables
		self.size = size
		self.screen = screen
		self.radius = radius
		self.inflRad = inflRad
		self.maxVel = maxVel
		self.particles = []
		self.dt = dt
		self.g = g
		self.press = press
		self.smooth = smooth
		self.mus = mus
		self.musfactor = 0

		# a grid that will carry what neighbous need to be checked. 
		self.grid = Grid(self.screen.get_width(),self.screen.get_height(),self.inflRad)

		# creates the initial positions in a sort of square
		N = int(math.sqrt(self.size)+1)-1
		vectors = []
		f = 1.5
		temp = pygame.Vector2(0,0)
		hor = pygame.Vector2(self.radius*f,0)
		ver = pygame.Vector2(0,self.radius*f)
		s = pygame.Vector2(0,0)
		for i in range(1,size + 1):
			vectors = vectors + [pygame.Vector2(temp.x,temp.y)]
			s = s + vectors[-1]
			if(i % N == 0):
				temp.y = 0
				temp = temp + hor 
			else:
				temp = temp + ver

		shift = pygame.Vector2(screen.get_width()/2,screen.get_height()/2) - s*(1/self.size)

		# creates the particles in the ensemble and adds their position and index to tree
		for i in range(0,self.size):
			new = Particle(self.screen,"black",self.radius,self.inflRad,shift + vectors[i],pygame.Vector2(0,0),self.dt)
			self.particles = self.particles + [new]
			self.grid.add(shift + vectors[i],i)

	# change how the mouse behaves
	def changeMus(self):
		if(self.musfactor == 0):
			self.musfactor = 1
		elif(self.musfactor == 1):
			self.musfactor = -1
		elif(self.musfactor == -1):
			self.musfactor = 0

	# draw the ensemble
	def illustrate(self):

		for i in range(0,self.size):
			v = self.particles[i].getVel().length()
			r = int(255*v/(0.00001 + self.maxVel))
			self.particles[i].setColour(pygame.Color(r,0,255-r))
			self.particles[i].illustrate()

	# the function for the influence function
	def influenceKer(self,X):
		if(X.length() > self.inflRad):
			return 0
		else:
			return (1 - X.length()/self.inflRad)**2

	# the gradient of the influence function
	def influenceKerGrad(self,X):
		if(X.length() > self.inflRad):
			return pygame.Vector2(0,0)
		else:
			return -2*(1 - X.length()/self.inflRad)*X.normalize()/self.inflRad

	# the function for the smooth influence function
	def influenceSmoothKer(self,X):
		if(X.length() > self.inflRad):
			return 0
		else:
			return (1 - (X.length()/self.inflRad)**2)**2

	# the gradient of the smooth influence function
	def influenceSmoothKerGrad(self,X):
		if(X.length() > self.inflRad):
			return pygame.Vector2(0,0)
		else:
			return -2*(1 - (X.length()/self.inflRad)**2)*X

	# calculating density at a particle p
	def density(self,p):
		volume = math.pi*self.inflRad**4/6
		res = 0
		candidates = self.cand(p)
		for i in candidates:
			res = res + self.influenceKer(self.particles[i].getPos() - p.getPos())
		return res/volume

	# update the ensemble
	def update(self):

		# the changes to the velocities:	
		Forces = []
		for i in range(0,self.size):
			Forces = Forces + [pygame.Vector2(0,0)]

		# first according to gravity and the mouse:
		grav = pygame.Vector2(0,self.g)
		for i in range(0,self.size):
			Forces[i] = Forces[i] + grav
			diff = pygame.mouse.get_pos() - self.particles[i].getNewPos()
			mF = 2
			Forces[i] = Forces[i] + self.musfactor*self.mus*self.influenceSmoothKerGrad(diff/mF)

		# next there is a repelling force, one calculates according to the density method:
		# A(x) = sum_p A(x(p))*W(|x - x(p)|)*m(p)/rho(p),
		# rho(x) = sum_p W(|x - x(p)|)*m(p)

		# first we make a dictionary with all the densities
		densities = []
		for i in range(0,self.size):
			densities = densities + [self.density(self.particles[i])]

		for i in range(0,self.size):
			candidates = self.cand(self.particles[i])
			for j in candidates:
				if(i != j):
					# incompressibility
					force = self.press*self.influenceKerGrad(self.particles[j].getNewPos() - self.particles[i].getNewPos())*densities[i]/2
					Forces[i] = Forces[i] + force
					Forces[j] = Forces[j] - force

					# viscosity
					diff = self.particles[i].getVel() + self.dt*Forces[i] - self.particles[j].getVel() - self.dt*Forces[j]
					force = self.smooth*diff*densities[i]/2
					Forces[i] = Forces[i] - force
					Forces[j] = Forces[j] + force

		# update the velocities:
		for i in range(0,self.size):
			self.particles[i].updateVel(Forces[i])
			self.particles[i].fixVel(self.maxVel)

		# move each particle:
		for i in range(self.size):
			self.particles[i].updatePos()

		# update the tree
		self.grid.reset()
		for i in range(0,self.size):
			self.grid.add(self.particles[i].getPos(),i)
			
	# finds the candidates given a particles grid index
	def cand(self,p):
		return self.grid.candidates(p.getPos())





