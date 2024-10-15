import pygame

class GameObject:
    def __init__(self, conf, x, y):
        self.type = conf.type

        self.image = conf.image
        self.frame = conf.frame

        # obstacle
        self.solid = conf.solid

        self.default_state = conf.default_state
        self.state = self.default_state
        self.state_list = conf.state_list

        self.x = x
        self.y = y
        self.width = conf.width
        self.height = conf.height
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

        self.on_collide = None
        self.holding = False
        self.throwing = False
        self.velox = 0
        self.veloy = 0
        self.gravity = 300
        self.horizontal = False
        self.picked = False

        self.objectBump = False
        self.exist = True
        
        #there can be on_attack


    def update(self, dt):
        pass

    def render(self, screen, adjacent_offset_x, adjacent_offset_y):
        if self.exist:
            screen.blit(self.image[self.state_list[self.state]], (self.x + adjacent_offset_x, self.y + adjacent_offset_y))

