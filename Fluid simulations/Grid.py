import pygame
import sys

class Grid:

	# constructor 
	def __init__(self,width,height,R):
		self.width = width
		self.height = height
		self.W = int(width/R) + 1
		self.H = int(height/R) + 1
		self.R = R
		self.boxes = {}

	# add an index to the relevant boxes given a spacial coordinate
	def add(self,vec,ind):
		x = int(vec.x/self.R)
		y = int(vec.y/self.R)
		xVar = [x-1,x,x+1]
		if(x == 0):
			xVar = [0,1]
		elif(x == self.W-1):
			xVar = [self.W-2,self.W-1]
		yVar = [y-1,y,y+1]
		if(y == 0):
			xVar = [0,1]
		elif(y == self.H-1):
			xVar = [self.H-2,self.H-1]

		for a in xVar:
			for b in yVar:
				key = a*self.H + b
				if(key in self.boxes.keys()):
					self.boxes[key] = self.boxes[key] + [ind]
				else:
					self.boxes[key] = [ind]

	# get the relevant indices given a coordinate:
	def candidates(self,vec):
		x = int(vec.x/self.R)
		y = int(vec.y/self.R)
		key = x*self.H + y
		if(key in self.boxes.keys()):
			return self.boxes[key]
		else:
			return []

	def reset(self):
		self.boxes = {}
