# maze.py starter Code

import viz
import vizshape
import vizcam
import math
from Model import *
import vizact
# An instance of this class adds a maze to the scene along with 
# an avatar that can be navigated through it.
class Maze(viz.EventClass):

	# Constructor 
	def __init__(self):
		self.mylight = viz.addLight()
		self.mylight.position(9,500,-25)
		self.mylight.color(.3,.3,.3)
		# base class constructor 
		self.boolean = False
		viz.EventClass.__init__(self)
		self.callback(viz.TIMER_EVENT,self.onTimer)
		self.starttimer(1,1/5.0,viz.FOREVER)
		self.cyl1hei = 0
		self.bZ = 0
		self.startbZ= 0
		self.ang=10
		self.tower = 1
		self.score = 0
		self.life = 5
		self.t = viz.addText("Score:" + "" + `self.score` , viz.SCREEN, pos = [0,0,0])
		self.t.fontSize(100)
		self.t.font('Chiller')
		self.t1 = viz.addText("Lives:" + "" + `self.life` , viz.SCREEN, pos = [0.8,0,0])
		self.t1.fontSize(100)
		self.t1.font('Chiller')
		self.bullet = None
		self.mode = 2
		
		
		# Load texture 
		pic = viz.addTexture('start.jpg') 
		# Create surface to wrap the texture on 
		self.start = viz.addTexQuad() 
		mat = viz.Matrix()
		mat.postScale(1.995,1.448,1.5)
		self.start.setMatrix( mat )
		self.start.setPosition([0, 0, 0]) #put quad in view 
		# Wrap texture on quad 
		self.start.texture(pic)
		self.t1.remove()
		self.t.remove()
		
		#snow
		self.bigSnowman = Model('snowman\\model.dae')
		self.snowman = Model('snowman\\model.dae')
		self.glacier = Model('glacier\\model.dae')
		self.bigGlacier = Model('glacier\\model.dae')
		self.bigSnowman.setOrientation(8,.1,5,.5,-50)
		self.snowman.setOrientation(3.1,.1,.7,.2,75)
		self.glacier.setOrientation(7,.1,2,.2,-90)
		self.bigGlacier.setOrientation(2.7,.1,4.5,.32,0)
		
		#desert
		self.bigPyr = Model('pyramidsmooth\\model.dae')
		self.pyr = Model('pyramidsmooth\\model.dae')
		self.sphinx = Model('sphinx\\model.dae')
		self.bigSphinx = Model('sphinx\\model.dae')
		self.bigPyr.setOrientation(7.3,-0.2,12,.7,-50)
		self.pyr.setOrientation(8,-0.2,17,.4,75)
		self.sphinx.setOrientation(5.5,0.2,15.1,.6,0)
		self.bigSphinx.setOrientation(2.9,0.1,10,2,-90)
		
		#city
		self.city = Model('city\\model.dae')
		self.sCity = Model('city\\model.dae')
		self.empstbu = Model('empire\\model.dae')
		self.skyskr = Model('skyskraper\\model.dae')
		self.towe = Model('tower\\model.dae')
		self.city.setOrientation(14,0.2,9.8,.0087,0)
		self.sCity.setOrientation(13,0.2,13.4,.006,180)
		self.empstbu.setOrientation(14.8,-0.1,15.17,.0082,0)
		self.skyskr.setOrientation(11.8,0.2,9.7,.006,0)
		self.towe.setOrientation(11.5,0.2,15.5,.03,0)

		#forest
		self.fores = Model('forest\\model.dae')
		self.fores1 = Model('forest\\model.dae')
		self.garde = Model('garden\\model.dae')
		self.fores.setOrientation(18.4,0.1,.3,0.07,0)
		self.fores1.setOrientation(18.4,0.1,9,0.04,-90)
		self.garde.setzScale(0.8)
		
		#spaceship
		self.ship = Model('ship\\model.dae')
		self.ship.setOrientation(4.5,.7,4,0.06,180)
		self.bZ = self.ship.getZ() + 0.05
		self.startbZ = self.ship.getZ()
		# set up keyboard and timer callback methods
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.COLLIDE_BEGIN_EVENT,self.onCollideBegin)
		
				
		#avatar's postion and rotation angle
		self.x = 4.5
		self.y = 0.85
		self.z = 2
		self.theta = 0
		
		# The 2D array below stores the representation of a maze.
		# Array entries containing a 2 represent 1 x 2 x 1 wall blocks.
		# Array entries containing a 0 represent 1 x 0.1 x 1 floor blocks.
		self.maze = []
		self.maze = [[11,11,11,11,11,11,11,11,11,11, 12,12,12,12,12,12,12,12,12,12]] + self.maze # row 17
		self.maze = [[11,0,0,0,0,0,0,0,0,0, 4,4,4,4,4,4,4,4,4,12]] + self.maze # row 17
		self.maze = [[11,0,0,0,0,0,0,0,0,0, 4,4,4,4,4,4,4,4,4,12]] + self.maze # row 16
		self.maze = [[11,0,0,0,0,0,0,0,0,0, 4,4,4,4,4,4,4,4,4,12]] + self.maze # row 15
		self.maze = [[11,0,0,0,1,1,1,1,1,1, 1,1,1,1,4,4,4,4,4,12]] + self.maze # row 14
		self.maze = [[11,0,0,0,1,0,0,0,0,0, 4,4,4,1,4,4,4,4,4,12]] + self.maze # row 13
		self.maze = [[11,0,0,0,8,0,0,0,0,0, 4,4,4,7,4,4,4,4,4,12]] + self.maze # row 12
		self.maze = [[11,0,0,0,1,0,0,0,0,0, 4,4,4,1,4,4,4,4,4,12]] + self.maze # row 11
		self.maze = [[11,0,0,0,10,0,0,0,0,0,4,4,4,10,4,4,4,4,4,12]] + self.maze # row 10
		self.maze = [[11,0,0,0,1,0,0,0,0,0, 4,4,4,1,4,4,4,4,4,12]] + self.maze # row 9
		
		self.maze = [[13,3,3,3,1,3,3,3,3,3, 6,6,6,1,5,5,5,5,5,14]] + self.maze # row 8
		self.maze = [[13,3,3,3,1,3,3,3,3,3, 6,6,6,1,5,5,5,5,5,14]] + self.maze # row 7
		self.maze = [[13,3,3,3,1,3,3,3,3,3, 6,6,6,1,5,5,5,5,5,14]] + self.maze # row 6
		self.maze = [[13,3,3,3,2,3,3,3,3,3, 6,6,6,9,5,5,5,5,5,14]] + self.maze # row 5
		self.maze = [[13,3,3,3,1,3,3,3,3,3, 6,6,6,1,5,5,5,5,5,14]] + self.maze # row 4
		self.maze = [[13,3,3,3,10,1,1,1,1,1,1,1,1,10,5,5,5,5,5,14]] + self.maze # row 3
		self.maze = [[13,3,3,3,3,3,3,3,3,3, 5,5,5,5,5,5,5,5,5,14]] + self.maze # row 2
		self.maze = [[13,3,3,3,3,3,3,3,3,3, 5,5,5,5,5,5,5,5,5,14]] + self.maze # row 1
		self.maze = [[13,3,3,3,3,3,3,3,3,3, 5,5,5,5,5,5,5,5,5,14]] + self.maze # row 0
		
		# Code to create blocks forming the maze goes here
		for r in range(0,len(self.maze)):
			for c in range(0, len(self.maze[0])):
				self.cVal = c
				self.rVal = r
				
				#Desert floor
				if (self.maze[r][c] == 0):
					box = vizshape.addCube( size=1, color=[.92,.90,.68] )
					mat = viz.Matrix()
					mat.postScale(1,.1,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
				elif (self.maze[r][c] == 11):
					box = vizshape.addCube( size=1, color=[.92,.90,.68] )
					mat = viz.Matrix()
					mat.postScale(1,10,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
				
				#Snow tower
				elif (self.maze[r][c] == 2):
					self.tower1 = vizshape.addCube( size=1, color=[1,.98,.98] )
					mat = viz.Matrix()
					mat.postScale(1,0.5,1)
					mat.postTrans(c+.5,0.25,r+.5)
					self.tower1.setMatrix( mat )
					y = 0.4
					self.cyl1 = vizshape.addCylinder( height=15.2, radius = 0.375, color=[1,1,1], alpha=0 )
					
					for i in range(19):
						water = vizshape.addCylinder( height = 0.2, radius = 0.375, slices = 20, stacks = 20, color=[0.13,.53,.85])
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						water.setMatrix( mat )
						y += 0.2
						snow = vizshape.addCube( size=0.6, color=[0.76,.87,1] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						snow.setMatrix( mat )
						y += 0.2
						snow.setParent(self.cyl1)
						water.setParent(self.cyl1)
						self.cyl1.setParent(self.tower1)
					self.cyl1.collideMesh()
					self.cyl1.enable(viz.COLLIDE_NOTIFY)

					self.barricade11 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade11.setParent(self.tower1)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,-0.48)
					self.barricade11.setMatrix( mat )
					self.barricade11.collideMesh()
					self.barricade11.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade12 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade12.setParent(self.tower1)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,0.48)
					self.barricade12.setMatrix( mat )
					self.barricade12.collideMesh()
					self.barricade12.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade13 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade13.setParent(self.tower1)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(0.48,0.7,0)
					self.barricade13.setMatrix( mat )
					self.barricade13.collideMesh()
					self.barricade13.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade14 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade14.setParent(self.tower1)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(-0.48,0.7,0)
					self.barricade14.setMatrix( mat )
					self.barricade14.collideMesh()
					self.barricade14.enable(viz.COLLIDE_NOTIFY)
					
				#City tower		
				elif (self.maze[r][c] == 7):
					self.tower3 = vizshape.addCube( size=1, color=[.43,.49,.50] )
					mat = viz.Matrix()
					mat.postScale(1,0.5,1)
					mat.postTrans(c+.5,0.25,r+.5)
					self.tower3.setMatrix( mat )
					y = 0.4
					self.cyl3 = vizshape.addCylinder( height=15.2, radius = 0.375, color=[1,1,1], alpha=0 )
					
					for i in range(19):
						sand = vizshape.addCylinder( height = 0.2, radius = 0.375, slices = 20, stacks = 20, color= [0.31, 0.31, 0.31] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						sand.setMatrix( mat )
						y += 0.2
						pyra = vizshape.addCube( size=0.6, color=[0.88, 0.88, 0.88] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						pyra.setMatrix( mat )
						y += 0.2
						sand.setParent(self.cyl3)
						pyra.setParent(self.cyl3)
						self.cyl3.setParent(self.tower3)
					self.cyl3.collideMesh()
					self.cyl3.enable(viz.COLLIDE_NOTIFY)
										
					self.barricade21 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade21.setParent(self.tower3)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,-0.48)
					self.barricade21.setMatrix( mat )
					self.barricade21.collideMesh()
					self.barricade21.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade22 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade22.setParent(self.tower3)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,0.48)
					self.barricade22.setMatrix( mat )
					self.barricade22.collideMesh()
					self.barricade22.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade23 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade23.setParent(self.tower3)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(0.48,0.7,0)
					self.barricade23.setMatrix( mat )
					self.barricade23.collideMesh()
					self.barricade23.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade24 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade24.setParent(self.tower3)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(-0.48,0.7,0)
					self.barricade24.setMatrix( mat )
					self.barricade24.collideMesh()
					self.barricade24.enable(viz.COLLIDE_NOTIFY)
				
				#Desert tower		
				elif (self.maze[r][c] == 8):
					self.tower2 = vizshape.addCube( size=1, color=[.92,.90,.68])
					mat = viz.Matrix()
					mat.postScale(1,0.5,1)
					mat.postTrans(c+.5,0.25,r+.5)
					self.tower2.setMatrix( mat )
					y = 0.4
					self.cyl2 = vizshape.addCylinder( height=15.2, radius = 0.375, color=[1,1,1], alpha=0 )
					
					for i in range(19):
						street = vizshape.addCylinder( height = 0.2, radius = 0.375, slices = 20, stacks = 20, color= [0.74, 0.49, 0.24] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						street.setMatrix( mat )
						y += 0.2
						pole = vizshape.addCube( size=0.6, color=[0.86, 0.72, 0.58] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						pole.setMatrix( mat )
						y += 0.2
						street.setParent(self.cyl2)
						pole.setParent(self.cyl2)
						self.cyl2.setParent(self.tower2)
					self.cyl2.collideMesh()
					self.cyl2.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade31 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade31.setParent(self.tower2)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,-0.48)
					self.barricade31.setMatrix( mat )
					self.barricade31.collideMesh()
					self.barricade31.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade32 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade32.setParent(self.tower2)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,0.48)
					self.barricade32.setMatrix( mat )
					self.barricade32.collideMesh()
					self.barricade32.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade33 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade33.setParent(self.tower2)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(0.48,0.7,0)
					self.barricade33.setMatrix( mat )
					self.barricade33.collideMesh()
					self.barricade33.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade34 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade34.setParent(self.tower2)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(-0.48,0.7,0)
					self.barricade34.setMatrix( mat )
					self.barricade34.collideMesh()
					self.barricade34.enable(viz.COLLIDE_NOTIFY)
						
				#Forrest tower
				elif (self.maze[r][c] == 9):
					self.tower4 = vizshape.addCube( size=1, color=[.27,.40,.20])
					mat = viz.Matrix()
					mat.postScale(1,0.5,1)
					mat.postTrans(c+.5,0.25,r+.5)
					self.tower4.setMatrix( mat )
					y = 0.4
					self.cyl4 = vizshape.addCylinder( height=15.2, radius = 0.375, color=[1,1,1], alpha=0 )

					for i in range(19):
						grass = vizshape.addCylinder( height = 0.2, radius = 0.375, slices = 20, stacks = 20, color= [0.88, 1, 0.18] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						grass.setMatrix( mat )
						y += 0.2
						leaf = vizshape.addCube( size=0.6, color=[0.00, 0.46, 0.00] )
						mat = viz.Matrix()
						mat.postTrans(0,y,0)
						leaf.setMatrix( mat )
						y += 0.2
						grass.setParent(self.cyl4)
						leaf.setParent(self.cyl4)
						self.cyl4.setParent(self.tower4)
					self.cyl4.collideMesh()
					self.cyl4.enable(viz.COLLIDE_NOTIFY)
						
					self.barricade41 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade41.setParent(self.tower4)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,-0.48)
					self.barricade41.setMatrix( mat )
					self.barricade41.collideMesh()
					self.barricade41.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade42 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade42.setParent(self.tower4)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.postTrans(0,0.7,0.48)
					self.barricade42.setMatrix( mat )
					self.barricade42.collideMesh()
					self.barricade42.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade43 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade43.setParent(self.tower4)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(0.48,0.7,0)
					self.barricade43.setMatrix( mat )
					self.barricade43.collideMesh()
					self.barricade43.enable(viz.COLLIDE_NOTIFY)
					
					self.barricade44 = vizshape.addCube( size=0.2, color=[0.93,0.82,0.008] )
					self.barricade44.setParent(self.tower4)
					mat = viz.Matrix()
					mat.postScale(1,1,0.4)
					mat.setAxisAngle(0,1,0,90)
					mat.postTrans(-0.48,0.7,0)
					self.barricade44.setMatrix( mat )
					self.barricade44.collideMesh()
					self.barricade44.enable(viz.COLLIDE_NOTIFY)
					
				#Pink track	
				elif (self.maze[r][c] == 1):
					box = vizshape.addCube( size=1, color= [0.85, 0.44, .57] )
					mat = viz.Matrix()
					mat.postScale(1,0.5,1)
					mat.postTrans(c+.5,0.25,r+.5)
					box.setMatrix( mat )
					
				#pink track with mesh
				elif (self.maze[r][c] == 10):
					box = vizshape.addCube( size=1, color= [0.85, 0.44, .57] )
					mat = viz.Matrix()
					mat.postScale(1,0.5,1)
					mat.postTrans(c+.5,0.25,r+.5)
					box.setMatrix( mat )
					box.collideMesh()
					box.enable(viz.COLLIDE_NOTIFY)
					
				#Snow floor
				elif (self.maze[r][c] == 3):
					box = vizshape.addCube( size=1, color=[1,.98,.98] )
					mat = viz.Matrix()
					mat.postScale(1,.1,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
					
				elif (self.maze[r][c] == 13):
					box = vizshape.addCube( size=1, color=[1,.98,.98] )
					mat = viz.Matrix()
					mat.postScale(1,10,1)
					mat.postTrans(c+.5,0.05,r+.75)
					box.setMatrix( mat )
					
				#City floor
				elif (self.maze[r][c] == 4):
					box = vizshape.addCube( size=1, color=[.43,.49,.50] )
					mat = viz.Matrix()
					mat.postScale(1,.1,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
					
				elif (self.maze[r][c] == 12):
					box = vizshape.addCube( size=1, color=[.43,.49,.50] )
					mat = viz.Matrix()
					mat.postScale(1,10,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
					
				#Outside Forrest floor
				elif (self.maze[r][c] == 5):
					box = vizshape.addCube( size=1, color=[.27,.40,.20] )
					mat = viz.Matrix()
					mat.postScale(1,.1,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
				elif (self.maze[r][c] == 14):
					box = vizshape.addCube( size=1, color=[.27,.40,.20] )
					mat = viz.Matrix()
					mat.postScale(1,10,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
				
				#Inside Forrest floor
				elif (self.maze[r][c] == 6):
					box = vizshape.addCube( size=1, color=[.325,.478,.239] )
					mat = viz.Matrix()
					mat.postScale(1,.1,1)
					mat.postTrans(c+.5,0.05,r+.5)
					box.setMatrix( mat )
					
				
		box = vizshape.addCube( size=1, color=[0,0,0] )
		mat = viz.Matrix()
		mat.postScale(18,5,.25)
		mat.postTrans(10,0.05,0)
		box.setMatrix( mat )
		self.mode = "thirdperson"
					
	# Key pressed down event code.
	def onKeyDown(self,key):
		if (key == viz.KEY_LEFT):
			# turn self.avatar ccw, as viewed from above
			self.ship.yrot -= 2 
			self.theta -= 2
		elif (key == viz.KEY_RIGHT):
			# turn self.avatar cw, as viewed from above
			self.ship.yrot += 2 
			self.theta += 2
		elif (key == viz.KEY_UP):
			# move avatar forward 
			dx = 0.2*math.sin( math.radians( self.theta ) )
			dz = 0.2*math.cos( math.radians( self.theta ) )
			self.ship.x = self.ship.x + dx
			self.ship.z = self.ship.z + dz
			self.x = self.x + dx
			self.z = self.z + dz
		elif (key == viz.KEY_DOWN):
			# increase the velocity of the ball
			dx = 0.2*math.sin( math.radians( self.theta ) )
			dz = 0.2*math.cos( math.radians( self.theta ) )
			self.ship.x = self.ship.x - dx
			self.ship.z = self.ship.z - dz
			self.x = self.x - dx
			self.z = self.z - dz
			
		elif (key == "1"):
			self.start.remove()
			
			pic = viz.addTexture('snow.jpg') 
			# Create surface to wrap the texture on 
			self.snow = viz.addTexQuad() 
			mat = viz.Matrix()
			mat.postScale(1.995,1.5,1.5)
			self.snow.setMatrix( mat )
			self.snow.setPosition([0, 0, 0]) #put quad in view 
			# Wrap texture on quad 
			self.snow.texture(pic)
			self.mylight.color(.3,.3,.3)
			view = viz.MainView
			mat = viz.Matrix()
			mat.postTrans(0,0,-1.9)
			view.setMatrix(mat)
			self.t1.remove()
			self.t.remove()
			self.t = viz.addText("Score:" + "" + `self.score` , viz.SCREEN, pos = [0,0,0])
			self.t.fontSize(100)
			self.t.font('Chiller')
			self.t1 = viz.addText("Lives:" + "" + `self.life` , viz.SCREEN, pos = [0.8,0,0])
			self.t1.fontSize(100)
			self.t1.font('Chiller')
			
		elif (key == "2"):
			self.mode = 2
			self.t.remove()
			self.t1.remove()
			view = viz.MainView
			mat = viz.Matrix()
			mat.postTrans(0,0,-1.9)
			view.setMatrix(mat)
			view.setMatrix(mat)
			viz.playSound('soundtrack.wav')
			self.start.remove()
			pic = viz.addTexture('maze.png') 
			# Create surface to wrap the texture on 
			self.maze = viz.addTexQuad() 
			mat = viz.Matrix()
			mat.postScale(1.995,1.5,1.5)
			mat.postTrans(0,0,1.5)
			self.maze.setMatrix( mat )
			self.maze.setPosition([0, 0, 0]) #put quad in view 
			# Wrap texture on quad 
			self.maze.texture(pic)
			
			
		
		elif key == 'w':
			if self.deskPressed:
				self.desk.setOrientation(self.desk.getX(), self.desk.getY(), self.desk.getZ()+1, 1, 90)
			elif self.shelfPressed:
				self.shelf.setOrientation(self.shelf.getX(), self.shelf.getY(), self.shelf.getZ()+1, 1, 0)
		elif key == 'a':
			if self.deskPressed:
				self.desk.setOrientation(self.desk.getX()-1, self.desk.getY(), self.desk.getZ(), 1, 90)
			elif self.shelfPressed:
				self.shelf.setOrientation(self.shelf.getX()-1, self.shelf.getY(), self.shelf.getZ(), 1, 0)
		elif key == 's':
			if self.deskPressed:
				self.desk.setOrientation(self.desk.getX(), self.desk.getY(), self.desk.getZ()-1, 1, 90)
			elif self.shelfPressed:
				self.shelf.setOrientation(self.shelf.getX(), self.shelf.getY(), self.shelf.getZ()-1, 1, 0)
		elif key == 'd':
			if self.deskPressed:
				self.desk.setOrientation(self.desk.getX()+1, self.desk.getY(), self.desk.getZ(), 1, 90)
			elif self.shelfPressed:
				self.shelf.setOrientation(self.shelf.getX()+1, self.shelf.getY(), self.shelf.getZ(), 1, 0)
				
		elif (key == " "):
			if self.life > 0:
				self.boolean = True
				self.bullet = vizshape.addSphere( radius = .07, color = viz.BLACK)
				mat = viz.Matrix()
				mat.postTrans(self.ship.getX(),self.ship.getY(),self.bZ + 0.05)
				self.bullet.setMatrix(mat)
				self.bullet.collideSphere(bounce = 3)
				self.bullet.enable( viz.COLLIDE_NOTIFY)
				self.bullet.setVelocity([0,0,5])
		
			
		elif (key == viz.KEY_RETURN):
			if self.mode == 2:
				self.maze.remove()
				self.mode = "firstperson"
			else:
				if self.tower ==1:
					self.snow.remove()
					view = viz.MainView
					mat = viz.Matrix()
					mat.postAxisAngle(1,0,0,30)
					mat.postTrans(4.5,3.5,.5)
					view.setMatrix(mat)
					viz.playSound('start.wav')
				elif self.tower ==2:
					self.egypt.remove()
					view = viz.MainView
					mat = viz.Matrix()
					mat.postAxisAngle(1,0,0,30)
					mat.postTrans(4.5,3.5,7.5)
					view.setMatrix(mat)
					viz.playSound('start.wav')
				elif self.tower ==3:
					self.city.remove()
					view = viz.MainView
					mat = viz.Matrix()
					mat.postAxisAngle(1,0,0,30)
					mat.postTrans(13.5,3.5,7.5)
					view.setMatrix(mat)
					viz.playSound('start.wav')
				elif self.tower ==4:
					self.forest7.remove()
					view = viz.MainView
					mat = viz.Matrix()
					mat.postAxisAngle(1,0,0,30)
					mat.postTrans(13.5,3.5,0.5)
					view.setMatrix(mat)
					viz.playSound('start.wav')

		if (self.mode == "firstperson"):
			self.start.remove()
			self.mylight.color(.7,.7,.7)
			dx =  0.1*math.sin( math.radians( self.theta ) )
			dz =  0.1*math.cos( math.radians( self.theta ) )
			view = viz.MainView
			mat = viz.Matrix()
			mat.postAxisAngle(0,1,0,self.theta)
			mat.postTrans(self.x,self.y,self.z+0.15)
			view.setMatrix(mat)
			self.ship.setOrientation(4.5,-17,4,0.06,180)
		self.ship.setTransMatrix()	
		
	
	def onTimer(self,num):
		mat = viz.Matrix()
		mat.postScale(1,0.5,1)
		mat.postAxisAngle(0,1,0,self.ang)
		mat.postTrans(4.5 ,0.25,5.5)
		self.tower1.setMatrix(mat)
		
		mat = viz.Matrix()
		mat.postScale(1,0.5,1)
		mat.postAxisAngle(0,1,0,self.ang)
		mat.postTrans(4.5 ,0.25,12.5)
		self.tower2.setMatrix(mat)
		
		mat = viz.Matrix()
		mat.postScale(1,0.5,1)
		mat.postAxisAngle(0,1,0,self.ang)
		mat.postTrans(13.5 ,0.25,12.5)
		self.tower3.setMatrix(mat)
		
		mat = viz.Matrix()
		mat.postScale(1,0.5,1)
		mat.postAxisAngle(0,1,0,self.ang)
		mat.postTrans(13.5 ,0.25,5.5)
		self.tower4.setMatrix(mat)
		
		self.ang += 10
	
	def onCollideBegin(self,e):			
		if (e.obj1 == self.cyl1) and self.cyl1hei >= -7.6 and self.tower == 1:
			self.cyl1hei -= 0.2
			mat = viz.Matrix()
			mat.postTrans(0,self.cyl1hei,0)
			self.cyl1.setMatrix( mat )
			self.score +=2
			self.t.remove()
			self.t = viz.addText("Score:" + "" + `self.score` , viz.SCREEN, pos = [0,0,0])
			self.t.fontSize(100)
			self.t.font('Chiller')
			e.obj2.remove()
			if (self.cyl1hei <= -7.6) and self.tower == 1:
				self.cyl1hei = 0
				self.ship.move(4.5,.7,11,5)
				self.ship.setOrientation(4.5,.7,11,0.06,180)
				self.bZ = self.ship.getZ() + 0.05
				self.tower = 2
				viz.playSound('level.wav')
				view = viz.MainView
				mat = viz.Matrix()
				mat.postTrans(0,0,-1.9)
				view.setMatrix(mat)
				pic = viz.addTexture('egypt.jpg') 
				# Create surface to wrap the texture on 
				self.egypt = viz.addTexQuad() 
				mat = viz.Matrix()
				mat.postScale(1.995,1.5,1.5)
				self.egypt.setMatrix( mat )
				self.egypt.setPosition([0, 0, 0]) #put quad in view 
				# Wrap texture on quad 
				self.egypt.texture(pic)
				mat = viz.Matrix()
				mat.postTrans(0,self.cyl1hei,0)
				self.cyl1.setMatrix( mat )
			
				
				
		elif (e.obj1 == self.cyl2) and self.cyl1hei >= -7.6 and self.tower == 2:
			self.cyl1hei -= 0.2
			mat = viz.Matrix()
			mat.postTrans(0,self.cyl1hei,0)
			self.cyl2.setMatrix( mat )
			self.score +=2
			self.t.remove()
			self.t = viz.addText("Score:" + "" + `self.score` , viz.SCREEN, pos = [0,0,0])
			self.t.fontSize(100)
			self.t.font('Chiller')
			e.obj2.remove()
			if (self.cyl1hei <= -7.6) and self.tower == 2:
				self.cyl1hei = 0
				self.ship.move(13.5,.7,11,5)
				self.ship.setOrientation(13.5,.7,11,0.06,180)
				self.bZ = self.ship.getZ() + 0.05
				self.tower = 3
				viz.playSound('level.wav')
				view = viz.MainView
				mat = viz.Matrix()
				mat.postTrans(0,0,-1.9)
				view.setMatrix(mat)
				pic = viz.addTexture('city.jpg') 
				# Create surface to wrap the texture on 
				self.city = viz.addTexQuad() 
				mat = viz.Matrix()
				mat.postScale(1.995,1.5,1.5)
				self.city.setMatrix( mat )
				self.city.setPosition([0, 0, 0]) #put quad in view 
				# Wrap texture on quad 
				self.city.texture(pic)
				mat = viz.Matrix()
				mat.postTrans(0,self.cyl1hei,0)
				self.cyl2.setMatrix( mat )
				
		elif (e.obj1 == self.cyl3) and self.cyl1hei >= -7.6 and self.tower == 3:
			self.cyl1hei -= 0.2
			mat = viz.Matrix()
			mat.postTrans(0,self.cyl1hei,0)
			self.cyl3.setMatrix( mat )
			self.score +=2
			self.t.remove()
			self.t = viz.addText("Score:" + "" + `self.score` , viz.SCREEN, pos = [0,0,0])
			self.t.fontSize(100)
			self.t.font('Chiller')
			e.obj2.remove()
			if (self.cyl1hei <= -7.6) and self.tower == 3:
				self.cyl1hei = 0
				self.ship.move(13.5,.7,4,5)
				self.ship.setOrientation(13.5,.7,4,0.06,180)
				self.bZ = self.ship.getZ() + 0.05
				self.tower = 4
				viz.playSound('level.wav')
				view = viz.MainView
				mat = viz.Matrix()
				mat.postTrans(0,0,-1.9)
				view.setMatrix(mat)
				pic = viz.addTexture('forest.jpg') 
				# Create surface to wrap the texture on 
				self.forest7 = viz.addTexQuad() 
				mat = viz.Matrix()
				mat.postScale(1.995,1.5,1.5)
				self.forest7.setMatrix( mat )
				self.forest7.setPosition([0, 0, 0]) #put quad in view 
				# Wrap texture on quad 
				self.forest7.texture(pic)
				mat = viz.Matrix()
				mat.postTrans(0,self.cyl1hei,0)
				self.cyl3.setMatrix( mat )
				
		elif (e.obj1 == self.cyl4) and self.cyl1hei >= -7.6 and self.tower == 4:
			self.cyl1hei -= 0.2
			mat = viz.Matrix()
			mat.postTrans(0,self.cyl1hei,0)
			self.cyl4.setMatrix( mat )
			self.score +=2
			self.t.remove()
			self.t = viz.addText("Score:" + "" + `self.score` , viz.SCREEN, pos = [0,0,0])
			self.t.fontSize(100)
			self.t.font('Chiller')
			e.obj2.remove()
			if (self.cyl1hei <= -7.6) and self.tower == 4:
				self.cyl1hei = 0
				self.ship.move(4.5,.7,4,5)
				self.ship.setOrientation(4.5,.7,4,0.06,180)
				self.bZ = self.ship.getZ() + 0.05
				self.tower = 1
				viz.playSound('level.wav')
				view = viz.MainView
				mat = viz.Matrix()
				mat.postTrans(0,0,-1.9)
				view.setMatrix(mat)
				pic = viz.addTexture('snow.jpg') 
				# Create surface to wrap the texture on 
				self.snow = viz.addTexQuad() 
				mat = viz.Matrix()
				mat.postScale(1.995,1.5,1.5)
				self.snow.setMatrix( mat )
				self.snow.setPosition([0, 0, 0]) #put quad in view 
				# Wrap texture on quad 
				self.snow.texture(pic)
				mat = viz.Matrix()
				mat.postTrans(0,self.cyl1hei,0)
				self.cyl4.setMatrix( mat )
				
		elif self.bullet!= None and ((e.obj1 == self.barricade11 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade12 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade13 and e.obj2 == self.bullet)\
			or (e.obj1 == self.barricade14 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade21 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade22 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade23 and e.obj2 == self.bullet)\
			or (e.obj1 == self.barricade24 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade31 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade32 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade33 and e.obj2 == self.bullet)\
			or (e.obj1 == self.barricade34 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade41 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade42 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade43 and e.obj2 == self.bullet)\
			or (e.obj1 == self.barricade44 and e.obj2 == self.bullet)):
			self.t1.remove()
			viz.playSound('oof.wav')
			self.life -= 1
			self.t1 = viz.addText("Lives:" + "" + `self.life` , viz.SCREEN, pos = [0.8,0,0])
			self.t1.fontSize(100)
			self.t1.font('Chiller')
			if self.life <= 0:
				viz.playSound('over.wav')
				pic = viz.addTexture('end.png') 
				# Create surface to wrap the texture on 
				self.end = viz.addTexQuad() 
				mat = viz.Matrix()
				mat.postScale(1.995,1.5,1.5)
				self.end.setMatrix( mat )
				self.end.setPosition([0, 0, 0]) #put quad in view 
				# Wrap texture on quad 
				self.end.texture(pic)
				view = viz.MainView
				mat = viz.Matrix()
				mat.postTrans(0,0,-1.9)
				self.t.remove()
				view.setMatrix(mat)
				self.t2 = viz.addText("Final Score:" + `self.score` , viz.SCREEN, pos = [0.15,0.3,0])
				self.t2.fontSize(200)
				self.t2.font('Chiller')
				self.t.remove()
				self.t1.remove()
		
			
		elif self.bullet!= None and ((e.obj1 == self.barricade21 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade22 and e.obj2 == self.bullet) \
			or (e.obj1 == self.barricade23 and e.obj2 == self.bullet)\
			or (e.obj1 == self.barricade24 and e.obj2 == self.bullet)):
			self.t1.remove()
			self.life -= 1
			self.t1 = viz.addText("Lives:" + "" + `self.life` , viz.SCREEN, pos = [0.8,0,0])
			self.t1.fontSize(100)
			self.t1.font('Chiller')
