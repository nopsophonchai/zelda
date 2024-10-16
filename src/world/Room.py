import random

from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.world.Doorway import Doorway
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.StateMachine import StateMachine
from src.GameObject import GameObject
from src.object_defs import *
import pygame
import time


class Room:
    def __init__(self, player):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.currentPot = None

        self.puzzle = False
        self.solved = False
        self.firstNum = -1
        self.secondNum = -1
        self.answerOne = -1
        self.answerTwo = -1
        self.select = 0
        self.switch = None

        self.tiles = []
        self.GenerateWallsAndFloors()

        self.entities = []
        self.GenerateEntities()

        self.objects = []
        self.GenerateObjects()

        self.doorways = []
        self.doorways.append(Doorway('top', False, self))
        self.doorways.append(Doorway('botoom', False, self))
        self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway('right', False, self))

        self.explosion = gExplosion['explosion'].images
        self.explodeAni = Animation(self.explosion,looping=False)
        # print(self.explosion)


        # for collisions
        self.player = player
        self.die = False

        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.render_entity=True

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

        self.solveTimer = pygame.USEREVENT + 1  
        self.switchCooldown = pygame.USEREVENT + 2 
        self.solveLimit = 10000  
        self.cooldown = 5000
        self.showTime = None
        self.timeLeft = 10
        self.enable = True
        

    def GenerateWallsAndFloors(self):
        for y in range(1, self.height+1):
            self.tiles.append([])
            for x in range(1, self.width+1):
                id = TILE_EMPTY

                # Wall Corner
                if x == 1 and y == 1:
                    id = TILE_TOP_LEFT_CORNER
                elif x ==1 and y == self.height:
                    id = TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    id = TILE_TOP_RIGHT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_RIGHT_CORNER

                #Wall, Floor
                elif x==1:
                    id = random.choice(TILE_LEFT_WALLS)
                elif x == self.width:
                    id = random.choice(TILE_RIGHT_WALLS)
                elif y == 1:
                    id = random.choice(TILE_TOP_WALLS)
                elif y == self.height:
                    id = random.choice(TILE_BOTTOM_WALLS)
                else:
                    id = random.choice(TILE_FLOORS)

                self.tiles[y-1].append(id)

    def GenerateEntities(self):
        types = ['skeleton']

        for i in range(NUMBER_OF_MONSTER):
            type = random.choice(types)

            conf = EntityConf(animation = ENTITY_DEFS[type].animation,
                              walk_speed = ENTITY_DEFS[type].walk_speed,
                              x=random.randrange(MAP_RENDER_OFFSET_X+TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48),
                              y=random.randrange(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE)+MAP_RENDER_OFFSET_Y - TILE_SIZE - 48),
                              width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height, health=ENTITY_DEFS[type].health)

            self.entities.append(EntityBase(conf))

            self.entities[i].state_machine = StateMachine()
            self.entities[i].state_machine.SetScreen(pygame.display.get_surface())
            self.entities[i].state_machine.SetStates({
                "walk": EntityWalkState(self.entities[i]),
                "idle": EntityIdleState(self.entities[i])
            })

            self.entities[i].ChangeState("walk")

    def GenerateObjects(self):
        switch = GameObject(GAME_OBJECT_DEFS['switch'],
                            x=random.randint(MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH-TILE_SIZE*2 - 48),
                            y=random.randint(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 48))
        for i in range(random.randint(3,5)):
            self.pot = GameObject(GAME_OBJECT_DEFS['pot'],x=random.randint(MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH-TILE_SIZE*2 - 48), y=random.randint(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 48))
            def pot_fucntion():
                self.pot.objectBump = True
            self.pot.on_collide = pot_fucntion
            self.objects.append(self.pot)
        def switch_function():
            if switch.state == "unpressed" and self.enable:
                self.puzzle = True
                pygame.time.set_timer(self.solveTimer, self.solveLimit)
                self.showTime = pygame.time.get_ticks()
                # switch.state = "pressed"
                
                # for doorway in self.doorways:
                #     doorway.open = True
                # gSounds['door'].play()

        switch.on_collide = switch_function
        
        
        self.objects.append(switch)
        self.switch = switch
        print(self.objects)
        


    def update(self, dt, events):
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return
        print(pygame.time.get_ticks()//1000)
        if self.puzzle and not self.solved:
            currentTime = pygame.time.get_ticks()
            self.timeLeft = self.solveLimit // 1000 - max(0, (currentTime - self.showTime) // 1000)

            if self.firstNum == -1 and self.secondNum == -1:
                
                self.firstNum = random.randint(0,49)
                self.secondNum = random.randint(0,49)
                self.answerOne = 0
                self.answerTwo = 0
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.select == 0:
                            self.answerOne += 1
                            if self.answerOne > 9:
                                self.answerOne = 0
                        else:
                            self.answerTwo += 1
                            if self.answerTwo > 9:
                                self.answerTwo = 0
                    if event.key == pygame.K_DOWN:
                        if self.select == 0:
                            self.answerOne -= 1
                            if self.answerOne < 0:
                                self.answerOne = 9
                        else:
                            self.answerTwo -= 1
                            if self.answerTwo < 0:
                                self.answerTwo = 9
                    if event.key == pygame.K_LEFT:
                        if self.select == 0:
                            self.select = 1
                        else:
                            self.select = 0
                    if event.key == pygame.K_RIGHT:
                        if self.select == 0:
                            self.select = 1
                        else:
                            self.select = 0
                    if event.key == pygame.K_RETURN:
                        if self.firstNum + self.secondNum == (self.answerOne*10+self.answerTwo):
                            self.switch.state = 'pressed'
                            for doorway in self.doorways:
                                doorway.open = True
                            gSounds['door'].play()
                            self.puzzle = False
                            pygame.time.set_timer(self.solveTimer,0)
                        else:
                            self.puzzle = False
                            if self.enable:
                                pygame.time.set_timer(self.switchCooldown,self.cooldown)
                                pygame.time.set_timer(self.solveTimer,0)
                            self.enable = False
                            self.switch.state = 'pressed'
                            
                
            if self.timeLeft == 0 :
                self.puzzle = False
                pygame.time.set_timer(self.solveTimer,0)
                self.switch.state = 'pressed'
                if self.enable:
                    print('Time set')
                    pygame.time.set_timer(self.switchCooldown,self.cooldown)
                    
                self.enable = False
            # curTime = pygame.time.get_ticks() // 1000
            # print(curTime)



        else:
            self.player.update(dt, events)

            for event in events:
                if event.type == self.switchCooldown:
                    self.enable = True
                    self.switch.state = 'unpressed'

            for entity in self.entities:
                if entity.health <= 0:
                    print('Dead')
                    entity.is_dead = True
                    self.entities.remove(entity)

                elif not entity.is_dead:
                    entity.ProcessAI({"room":self}, dt)
                    entity.update(dt, events)

                if not entity.is_dead and self.player.Collides(entity) and not self.player.invulnerable:
                    gSounds['hit_player'].play()
                    self.player.Damage(1)
                    self.player.SetInvulnerable(1.5)

            for object in self.objects:
                object.update(dt)
                # print(object)
                if not object.exist:
                    if object.width < 128 and object.height < 80:
                        object.width *= 2
                        object.height *= 2
                    object.rect.width = object.width
                    object.rect.height = object.height
                    object.rect.x = object.x
                    object.rect.y = object.y
                    print(f'Width:{object.width} Height:{object.height}')
                    
                    self.explodeAni.update(dt)
                    for i in self.entities:
                        if i.Collides(object):
                            # print('Collides')

                            i.Damage(100)
                    # time.sleep(1)
                    # self.objects.remove(object)

                if self.player.Collides(object):
                    if object.type == 'pot': 
                        # print('hi')
                        self.player.collidePot = True
                        #print(self.player.collidePot)
                        self.currentPot = object
                        if object.exist:
                            if self.player.direction == 'left':
                                self.player.x += PLAYER_WALK_SPEED * dt
                            elif self.player.direction == 'right':
                                self.player.x -= PLAYER_WALK_SPEED * dt 
                            elif self.player.direction == 'up':
                                self.player.y += PLAYER_WALK_SPEED * dt
                            elif self.player.direction == 'down':
                                self.player.y -= PLAYER_WALK_SPEED * dt  
                    if object.type == 'heart':
                        if self.player.health < 5:
                            self.player.health += 2
                        elif self.player.health == 5:
                            self.player.health += 1
                        object.exist = False
                        self.objects.remove(object)
                        
                        
                    else:
                        object.on_collide()



    def render(self, screen, x_mod, y_mod, shifting):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                # need to access tile_id - 1  <-- actual list is start from 0
                screen.blit(gRoom_image_list[tile_id-1], (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                            y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod))


        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)


        for object in self.objects:
            if not object.exist and object.type =='pot':
                # gExplosion['explosion'].render(screen,object.x,object.y)
                screen.blit(self.explodeAni.image,(object.x,object.y))
                if self.explodeAni.times_played > 0:
                    self.explodeAni.Refresh()
                    if random.choice([True,False]):
                        self.objects.append(GameObject(GAME_OBJECT_DEFS['heart'],object.x,object.y))
                    self.objects.remove(object)
                    
            else:
                object.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)
        

        if not shifting:
            for entity in self.entities:
                if not entity.is_dead:
                    entity.render(self.adjacent_offset_x, self.adjacent_offset_y + y_mod)
            if self.player:
                self.player.render()
        if self.puzzle:
            pygame.draw.rect(screen,(105,0,0),(WIDTH//2-WIDTH//4,HEIGHT//10,WIDTH//2,HEIGHT//1.25))
            t_press_enter = gFonts['zelda_small'].render("Solve", False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 4.75))
            screen.blit(t_press_enter, rect)

            t_press_enter = gFonts['zelda_small'].render(str(self.firstNum), False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 3, HEIGHT / 2.5))
            screen.blit(t_press_enter, rect)
            t_press_enter = gFonts['zelda_small'].render(str(self.secondNum), False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 1.5, HEIGHT / 2.5))
            screen.blit(t_press_enter, rect)
            t_press_enter = gFonts['zelda_small'].render('+', False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 2.5))
            screen.blit(t_press_enter, rect)
            firstColor = (255,255,255) if self.select == 0 else (100,100,100)
            secondColor = (255,255,255) if self.select == 1 else (100,100,100)
                
            t_press_enter = gFonts['zelda_small'].render(str(self.answerOne), False, firstColor)
            rect = t_press_enter.get_rect(center=(WIDTH / 2.10, HEIGHT / 1.5))
            screen.blit(t_press_enter, rect)
            t_press_enter = gFonts['zelda_small'].render(str(self.answerTwo), False, secondColor)
            rect = t_press_enter.get_rect(center=(WIDTH / 1.90, HEIGHT / 1.5))
            screen.blit(t_press_enter, rect)

            t_press_enter = gFonts['zelda_xsmall'].render('Press Enter to Solve', False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 1.25))
            screen.blit(t_press_enter, rect)

            t_press_enter = gFonts['zelda_xsmall'].render(str(self.timeLeft), False, (255, 255, 255))
            rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 1.15))
            screen.blit(t_press_enter, rect)
            
