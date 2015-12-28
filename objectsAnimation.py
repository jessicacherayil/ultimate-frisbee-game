# Bella Nikom & Maja Svanberg
# CS111 Final Project
# 2015 May 05
# objectsAnimation.py

import Tkinter as tk
import animation

#class used to create initial disc pull
class BigDisc(animation.AnimatedObject):
    
    def __init__(self,canvas,x,y,speed, filename):
        self.canvas = canvas
        self.photo = tk.PhotoImage(file = filename)
        #adds in the image to the file with specified coordinates
        self.disc = self.canvas.create_image(x,y, image=self.photo)
        self.speed = speed 
        self.deltaY = self.speed*10
        self.id = self.disc
        
    def move(self):
        """move down towards blue team and stay there"""
        #get coordinates of photo-since it is a photo it only has a center x and y
        x1, y1 =  self.canvas.coords(self.disc)
        if y1 >= 320: # if the disc is still sort of around the blue team
            self.deltaY = 0 # stop moving down
        self.canvas.move(self.disc, 0, +self.deltaY) # move up toward ceiling

#class for the disc used for animation with red and blue dots
class Disc(animation.AnimatedObject):
    
    def __init__(self, canvas, x, y, size, speed, color):
        self.canvas = canvas
        self.size = size
        self.speed = speed 
        self.deltaX = self.speed*20   
        self.deltaY = 1.6    
        self.color = color
        
        #Drawing disc
        self.disc = self.canvas.create_oval(x,y, x+size, y+size, fill = color, outline = color)
        self.id = self.disc
        
    def move(self):
        """move up disc to position where it meets the players"""
        xy =  self.canvas.coords(self.disc)
        the_lower_y = xy[3]
        the_left_x = xy[0]
        if the_lower_y <= 200 and the_left_x <= 100: # if point is reached
            self.deltaX = 0 # stop moving up
            self.deltaY = 0 # stop moving sideways
        self.canvas.move(self.disc, -self.deltaY, -self.deltaX)  

#only draws the red and blue teams
class Players(animation.AnimatedObject):
    
    def __init__(self, canvas, x, y, size, speed, color):
        self.size = size
        self.canvas = canvas            
        self.color = color
        self.speed = speed 
        self.deltaY = self.speed*20
        self.deltaX = 7.2
        #draw players
        self.player = self.canvas.create_oval(x, y, x+size, y+size, fill = color, outline = color)
        self.id = self.player
    
    def move(self):
        pass
      
class CutterO(Players):
            
    def move(self):
        xy =  self.canvas.coords(self.player)
        the_lower_y = xy[3]
        if the_lower_y == 20: # if reached upper turning point
            self.deltaY = -self.deltaY # move downwards instead of upwards
        if the_lower_y >= 190: # if reached lower point, stop
            self.deltaX = 0
            self.deltaY = 0
        self.canvas.move(self.player, -self.deltaX, -self.deltaY)
        
class BadCutterO(CutterO):
    
    def move(self):
        CutterO.move(self)
        self.deltaX += -.15 # slow down little by little so cutterD wins

class CutterD(Players):
    
    def move(self):
        xy =  self.canvas.coords(self.player)
        the_lower_y = xy[3]
        if the_lower_y == 20: # if reached upper turning point
            self.deltaY = -self.deltaY # move downwards instead of upwards
        if the_lower_y >= 190:# if reached lower point, stop
            self.deltaX = 0
            self.deltaY = 0
        self.canvas.move(self.player, -self.deltaX, -self.deltaY)
         
class BadCutterD(CutterD):
    def move(self):
        CutterD.move(self)
        self.deltaX += -.20 # slow down little by little so cutterO wins
        