# File: terrainLabStarterCode.py
# Purpose: To display terrain data read from a ArcGIS file
# and allow the user to navigate through it

import viz
import vizshape
import vizcam
import random
import math

class Terrain(viz.EventClass):

	# Constructor reads in terrain data and creates
	# triangular mesh that models it
	def __init__(self):
		# must call constructor of EventClass first!!
		viz.EventClass.__init__(self)
		self.x = 20
		self.z =20
		self.y = 0
		self.theta = 0
		self.angl = 0
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.avatar = viz.add('vcc_female.cfg')
		self.avatar.disable(viz.INTERSECTION)
		
		print "Reading file greysriver.asc..." 
		f = open('greysriver.asc', 'r')
		# first two lines are number of cols and rows
		cols = int(str.split(f.readline())[1])
		rows = int(str.split(f.readline())[1])
		
		# discard next 4 lines in file
		f.readline(), f.readline(), f.readline(), f.readline()
		
		# create 2D array of empty lists, one empty list for each row of data
		self.elevation = [ [] for x in range(0,rows)]
		maxElevation = -50000
		minElevation = 50000
		# read in elevation data and keep track of max and min elevations
		for r in range( 0, rows):
			for n in str.split(f.readline()):
				self.elevation[r].append(float(n))
				if ( float(n) > maxElevation ):
					maxElevation = float(n)
				if ( float(n) < minElevation):
					minElevation = float(n)
		
		# create triangle mesh
		viz.startLayer(viz.TRIANGLES)
		for r in range(rows-1):
			for c in range(cols-1):
				# create first triangle
				color = self.getColor( self.elevation[r][c], maxElevation, minElevation)
				viz.vertexColor( color )
				viz.vertex(c,self.elevation[r][c],r)
				viz.vertex(c+1,self.elevation[r+1][c+1],r+1)
				viz.vertex(c,self.elevation[r+1][c],r+1)
				
				# create second triangle
				color = self.getColor( self.elevation[r][c+1], maxElevation, minElevation)
				viz.vertexColor( color )
				viz.vertex(c,self.elevation[r][c],r)
				viz.vertex(c+1,self.elevation[r][c+1],r)
				viz.vertex(c+1,self.elevation[r+1][c+1],r+1)
		self.t = viz.endLayer()
		self.y = self.elevation[20][20]+1
		self.transform()
	# Returns a color [R,G,B] based on elevation 
	def getColor(self, elevation, maxElevation, minElevation):
		# river bed triangles are blue
		if ( elevation < 1895 ):
			return [0,0,.5]
		# other triangles are colored based on elevation
		# higher elevations lighter, lower elevations darker
		else:
			color = 1-((maxElevation-elevation)
			           /(maxElevation - minElevation))
			return [color,color,color]
		
	# controls the view of the scene
	def transform(self):
			if self.angl == 1:
				view = viz.MainView
				mat = viz.Matrix()
				mat.postAxisAngle(0,1,0,self.theta)
				mat.postTrans(self.x,self.y+1.45,self.z+0.15)
				view.setMatrix(mat)
			intersect = viz.intersect([self.x, 4000, self.z], [self.x, 0, self.z])
			self.y = intersect.point[1]
			mat = viz.Matrix()
			mat.postAxisAngle(0,1,0,self.theta)
			mat.postScale(2,2,2)
			mat.postTrans(self.x, self.y, self.z)
			self.avatar.setMatrix(mat)
		
	# Key pressed down event code.
	def onKeyDown(self,key):
		if (key == viz.KEY_LEFT):
			self.theta = self.theta - 5	
		if (key == viz.KEY_RIGHT):
			self.theta = self.theta + 5	
		if (key == viz.KEY_UP):
			ang = math.radians(self.theta)
			self.x = self.x + (math.sin(ang)/3)
			self.z = self.z+(math.cos(ang)/3)
		if (key == viz.KEY_DOWN):
			ang = math.radians(self.theta)
			self.x = (self.x - math.sin(ang)/3)
			self.z = (self.z - math.cos(ang)/3)
		if key == 'u':
			self.y += 5
		if key == 'd':
			self.y -= 5
			#self.y = self.elevation[self.x][self.z] + 1
		if (key == "1"):
			self.angl = 1
			view = viz.MainView
			mat = viz.Matrix()
			mat.postAxisAngle(0,1,0,self.theta)
			mat.postTrans(self.x,self.y+1.45,self.z+0.15)
			view.setMatrix(mat)
		self.transform()	
	
