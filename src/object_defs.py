from src.recourses import *
import pygame
class ObjectConf:
    def __init__(self, type, img, frame, solid, default_state, states, width, height):
        self.type = type
        self.image = img
        self.frame = frame
        self.solid = solid
        self.default_state = default_state
        self.state_list = states
        self.width = width
        self.height = height

#ObjectConf('switch')


GAME_OBJECT_DEFS = {
    'switch': ObjectConf('switch', gSwitch_image_list, 2, False, "unpressed", {'unpressed':1, 'pressed':0}, width=48, height=48),
    'pot': ObjectConf('pot', [pygame.image.load('/Users/noppynorthside/zelda/zelda/graphics/pot.png'),pygame.image.load('/Users/noppynorthside/zelda/zelda/graphics/pot.png')],1,True,"unlifted",{'unlifted':0,'lifted':1}, width=64,height=40),
    'heart': ObjectConf('heart',[pygame.image.load('./graphics/heart.png')],0,False,"heart",{'heart':0},40,40)
}