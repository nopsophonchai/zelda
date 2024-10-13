from src.constants import *
from src.states.entity.EntityWalkState import EntityWalkState
import pygame, time

class PlayerPotState(EntityWalkState):
    def __init__(self, player,dungeon):
        super(PlayerPotState, self).__init__(player)
        self.dungeon = dungeon
        self.entity.ChangeAnimation('down')
        self.object = None
        self.throw = False
        self.ogX = 0
        self.ogY = 0

    def Exit(self):
        pass

    def Enter(self, params):
        self.object = params['pot']
        self.originalSpeed = self.entity.walk_speed
        if self.object != None:
            self.object.holding = True
    def update(self, dt, events):
        #print('You are in pot state')
        if self.object != None:
            if self.object.holding:
                self.object.x = self.entity.x
                self.object.y = self.entity.y - TILE_SIZE
                self.ogX = self.object.x
                self.ogY = self.object.y
                
            if self.object.throwing:
                self.object.x += self.object.velox * dt
                self.object.y += self.object.veloy * dt
                print(f'Object X:{self.object.x}\tObject Y:{self.object.x}')
                

                if self.object.horizontal:
                    self.object.veloy += self.object.gravity *dt

            pressedKeys = pygame.key.get_pressed()
            if pressedKeys[pygame.K_LEFT]:
                self.entity.walk_speed = self.originalSpeed
                self.entity.direction = 'left'
                self.entity.ChangeAnimation('left')
            elif pressedKeys[pygame.K_RIGHT]:
                self.entity.walk_speed = self.originalSpeed
                self.entity.direction = 'right'
                self.entity.ChangeAnimation('right')
            elif pressedKeys[pygame.K_DOWN]:
                self.entity.walk_speed = self.originalSpeed
                self.entity.direction = 'down'
                self.entity.ChangeAnimation('down')
            elif pressedKeys[pygame.K_UP]:
                self.entity.walk_speed = self.originalSpeed
                self.entity.direction = 'up'
                self.entity.ChangeAnimation('up')
            else:
                self.entity.walk_speed = 0
                #self.entity.ChangeState('idle')




            distance_traveled = ((self.object.x - self.ogX) ** 2 + (self.object.y - self.ogY) ** 2) ** 0.5
            MAX_DISTANCE = 100
            if distance_traveled >= MAX_DISTANCE:
                self.object.velox = 0
                self.object.veloy = 0
                self.object.throwing = False
                self.entity.ChangeState('walk')

            if self.object.x < 0:
                self.object.x = 0
                self.object.velox = 0  
                self.object.throwing = False 
                self.entity.ChangeState('walk')
            elif self.object.x > WIDTH - TILE_SIZE:
                self.object.x = WIDTH - TILE_SIZE
                self.object.velox = 0
                self.object.throwing = False
                self.entity.ChangeState('walk')
            if self.object.y < 0:
                self.object.y = 0
                self.object.veloy = 0  
                self.object.throwing = False
                self.entity.ChangeState('walk')
            elif self.object.y > HEIGHT - TILE_SIZE:
                self.object.y = HEIGHT - TILE_SIZE
                self.object.veloy = 0
                self.object.throwing = False
                self.entity.ChangeState('walk')

            for event in events:
                if event.type == pygame.KEYDOWN:
                    print('called')
                    if event.key == pygame.K_SPACE:
                        print(f'Og X:{self.ogX}\tOg Y:{self.ogY}')
                        self.object.throwing = True
                        self.object.holding = False
                        if self.entity.direction == 'left':
                            self.object.velox = -300
                            self.object.horizontal = True
                        elif self.entity.direction == 'right':
                            self.object.velox = -300
                            self.object.horizontal = True
                        elif self.entity.direction == 'up':
                            self.object.velox = 0
                            self.object.veloy = -300
                        elif self.entity.direction == 'down':
                            self.object.velox = 0
                            self.object.veloy = 300
                        self.entity.collidePot = False
            
           

            

        #move and bump to the wall check
        super().update(dt, events)


        if self.bumped:
            if self.entity.direction == 'left':
                #temporal move to the wall (bumping effect)
                self.entity.x = self.entity.x - PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.y + 12
                        self.dungeon.BeginShifting(-WIDTH, 0)

                self.entity.x = self.entity.x + PLAYER_WALK_SPEED * dt

            elif self.entity.direction == 'right':
                self.entity.x = self.entity.x + PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.y + 12
                        self.dungeon.BeginShifting(WIDTH, 0)

                self.entity.x = self.entity.x - PLAYER_WALK_SPEED * dt

            elif self.entity.direction == 'up':
                self.entity.y = self.entity.y - PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.x + 24
                        self.dungeon.BeginShifting(0,  -HEIGHT)

                self.entity.y = self.entity.y + PLAYER_WALK_SPEED * dt

            else:
                self.entity.y = self.entity.y + PLAYER_WALK_SPEED * dt

                for doorway in self.dungeon.current_room.doorways:
                    if self.entity.Collides(doorway) and doorway.open:
                        self.entity.y = doorway.x + 24
                        self.dungeon.BeginShifting(0,  HEIGHT)

                self.entity.y = self.entity.y - PLAYER_WALK_SPEED * dt