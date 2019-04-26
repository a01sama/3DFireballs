import viz
import vizshape
import vizcam
import math
import vizact


# An instance of this class reads a model in from
# adds a file and adds it to the scene.  It keeps
# track of the models x,y,z location, scale, and
# rotation.
# 
class Model():

	# Constructor 
	def __init__(self, filename):
		# read model data from file and add to scene graph 
		self.node = viz.add(filename)
		# model's location in world
		self.x = 0
		self.y = 0
		self.z = 0
		# model's scale
		self.s = 1
		# model's rotation about the Y axis (in degrees)
		self.yrot = 0
		self.setTransMatrix()

	# setter for location of the model	
	def setLocation(self, x, y, z ):
		self.x = x
		self.y = y
		self.z = z
		self.setTransMatrix()
	
	# getters for the coordinates of the model's location
	def getX(self):
		return self.x
		
	def getY(self):
		return self.y
		
	def getZ(self):
		return self.z
		
	# setter and getter for the model's (uniform) scale
	def setScale(self, s ):
		self.s = s
		self.setTransMatrix()
	def getScale(self):
		return self.s
		
	# setter and getter for the model's rotation about Y axis
	# in degrees
	def setYRotation(self, yrot ):
		self.yrot = yrot
		self.setTransMatrix()
		
	def getYRotation(self):
		return self.yrot
		
	# get the model's scene graph node
	def getNode(self):
		return self.node
		
	# set model's x,y,z, scale and rotation
	def setOrientation(self,x,y,z,s,yrot):
		self.x = x
		self.y = y
		self.z = z
		self.s = s
		self.yrot = yrot
		self.setTransMatrix()
	
	def setzScale(self,z):
		mat = viz.Matrix()
		mat.postScale(0.07,0.08,0.1)
		#mat.postScale(self.s,self.s,self.s)
		mat.postAxisAngle(0,1,0,90)
		mat.postTrans(10.5,0.2,8.9)
		self.node.setMatrix( mat )
	
	def setTransMatrix(self):
		mat = viz.Matrix()
		mat.postScale(self.s,self.s,self.s)
		mat.postAxisAngle(0,1,0,self.yrot)
		mat.postTrans(self.x,self.y,self.z)
		self.node.setMatrix( mat )
		
	def move(self, x, y, z, s):
		action1 = vizact.moveTo([x,y,z],speed =s)
		self.node.addAction(action1)
		self.x =x
		self.y = y
		self.z = z
	
		
		
		
		