import pygame 
from constants import *


class player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.game.all_sprites)
        pygame.mixer.pre_init(44100, -16, 2, 512)
        self.player = pygame.transform.scale2x(pygame.image.load("Images/Player/Player1.png"))
        self.x = x 
        self.y = y 
        self.image =  self.player
        self.rect = self.image.get_rect()
        self.vel = [0, 0]   
        self.jump = False
        self.jumpcount = 0
        self.pencil = 0
        self.animation_countr = 0
        self.animation_countl = 0
        self.aircount = 0
        self.load()
        
    def load(self):
        player1_img_right = pygame.transform.scale2x(pygame.image.load("Images/Player/Player1.png")) 
        player2_img_right = pygame.transform.scale2x(pygame.image.load("Images/Player/Player2.png"))
        player3_img_right = pygame.transform.scale2x(pygame.image.load("Images/Player/Player3.png"))
        player4_img_left = pygame.transform.scale2x(pygame.image.load("Images/Player/Player4.png"))
        self.animations_right = [player1_img_right, player1_img_right, player2_img_right, player2_img_right, player3_img_right, player3_img_right, player4_img_left]
        
        player1_img_left = pygame.transform.scale2x(pygame.transform.flip(pygame.image.load("Images/Player/Player1.png"), True, False))
        player2_img_left = pygame.transform.scale2x(pygame.transform.flip(pygame.image.load("Images/Player/Player2.png"), True, False))
        player3_img_left = pygame.transform.scale2x(pygame.transform.flip(pygame.image.load("Images/Player/Player3.png"), True, False))
        player4_img_left = pygame.transform.scale2x(pygame.transform.flip(pygame.image.load("Images/Player/Player4.png"), True, False))
        self.animations_left = [player1_img_left, player1_img_left, player2_img_left, player2_img_left, player3_img_left, player3_img_left, player4_img_left]
        
        self.jump_sound = pygame.mixer.Sound('Images\jump.wav')
        
    def get_keys(self):
        
        self.vel = [0, 0]
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_a]:
            self.vel[0] = -PLAYERSPEED
        if keys[pygame.K_d]:
            self.vel[0] = PLAYERSPEED
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            # Jump 
            self.jump = True
            self.jump_sound.play()

        
        
    def animations(self):
        if self.vel[0] > 0:
            # Right
            if self.animation_countr + 1 >= 14:
                self.animation_countr = 0
                
            self.image = self.animations_right[self.animation_countr//2]
            self.animation_countr += 1
             
        if self.vel[0] < 0:
            # Left
            if self.animation_countl + 1 >= 14:
                self.animation_countl = 0
                
            self.image = self.animations_left[self.animation_countl//2]
            self.animation_countl += 1
    
    def collide_with_wall(self, tiles):
        hit_list = []
        for wall in tiles:
            if wall.rect.colliderect(self.rect):
                hit_list.append(wall)
        return hit_list

    def movement(self):
        # Collision on the x axis 
        self.rect.x = self.x 
        hit_list = self.collide_with_wall(self.game.walls)
        for wall in hit_list:
            if self.vel[0] > 0:
                self.rect.right = wall.rect.left 
            elif self.vel[0] < 0:
                self.rect.left = wall.rect.right
        
        self.rect.y = self.y 
        hit_list = self.collide_with_wall(self.game.walls)
        for wall in hit_list:
            if self.vel[1] > 0:
                self.rect.down = wall.rect.top 
            elif self.vel[1] < 0:
                self.rect.top = wall.rect.down   
    
    def collision(self, dir):
        self.bottom = False
        if dir == "x":
            hit = pygame.sprite.spritecollide(self, self.game.walls, False)
            if hit:
                if self.vel[0] > 0:
                    # Moving to the right
                    
                    self.x = hit[0].rect.left - self.rect.width
                if self.vel[0] < 0:
                    # Moving to the Left
                    
                    self.x = hit[0].rect.right
                self.vel[0] = 0
                self.rect.x = self.x
        if dir == "y":
                hit = pygame.sprite.spritecollide(self, self.game.walls, False)
                if hit:
                    if self.vel[1] > 0:
                        # Moving to the Down
                        self.bottom = True
                        self.y = hit[0].rect.top - self.rect.height
                    if self.vel[1] < 0:
                        # Moving to the UP
                        
                        self.y = hit[0].rect.bottom
                    self.vel[1] = 0
                    self.rect.y = self.y
                
        
    def update(self):
        self.get_keys()
        self.animations()
        self.vel[1] += self.jumpcount 
        self.jumpcount += 25
        if self.jumpcount > 1500:
            # This when you fall of
            self.jumpcount = 1500
            self.game.change_phase("YOU LOST", (255, 0, 102), (153, 51, 255))
        self.x += self.vel[0] * self.game.dt
        self.y += self.vel[1] * self.game.dt
        
        
        

        
        self.rect.x = self.x 
        self.collision("x")
        self.rect.y = self.y
        self.collision("y")

        if self.bottom:
            self.jumpcount = 0 
            self.aircount = 0
        else:
            self.aircount += 1
        
        
        if self.jump:
            if self.aircount < 22:
                self.jumpcount = -490
            else:
                
                self.jump = False
                

class wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, width, height, game):
        self.group = game.walls
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game 
        self.x = x 
        self.y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.x = x 
        self.rect.y = y
        
        
class door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.group = game.door 
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game 
        self.rect = pygame.Rect(x, y, w, h)
    
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.new_level()
            self.game.load("Images/map4.tmx")
            self.game.new()

class pencil(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.group = game.all_sprites 
        pygame.sprite.Sprite.__init__(self, self.group)
        self.pencil_image = pygame.image.load("Images/pencil.png")
        font = pygame.font.SysFont("", 50)
        text = font.render("MUSIC", 1,  (0, 0, 0))
        self.image = self.pencil_image
        self.game = game
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y 
    
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.player.jumpcount = -520
            self.kill()
            self.game.player.pencil += 1