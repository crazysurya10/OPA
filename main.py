import pygame
from constants import *
from entites import *
from cam import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT)) 
        self.FPS = 60 
        self.clock = pygame.time.Clock()
        self.load("Images/map3.tmx")
    
    
    
    def load(self, filename):   
        self.filename = filename    
        self.map = TiledMap(filename) 
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        
        self.camera = Camera(self.map.width, self.map.height)

    def check_win(self):
        if self.filename == "Images/map4.tmx":
            if self.player.rect.x >= 5071 and self.player.rect.x <= 5112:
                if self.player.rect.y == 1350:
                    return True 
                
                else:
                    return False
        else:
            return
    
    def new_level(self):
        i = 0 
        while i <= 1500:
            self.win.fill((0, 0, 0))
            
            pygame.display.update()
            i += 1        
    
    def change_phase(self, text, color, bgcolor):
        i = 0 
        while i <= 500:
            self.win.fill(bgcolor)
            cool_font = pygame.font.SysFont("", 100)
            message = cool_font.render(f"{text}", 1, color)
            self.win.blit(message, (WIDTH/2-message.get_width()/2, HEIGHT/2-message.get_height()/2))
            pygame.display.update()
            i += 1
        self.menu()
        
    def menu(self):
        self.game = False
        run = True
        font = pygame.font.SysFont("comicsans", 100)
        title = font.render("WHY I ", 1, (0, 0, 0))
        heart = pygame.transform.scale(pygame.image.load("Images/heart.png"), (80, 80))
        OPA = pygame.transform.scale(pygame.image.load("Images/OPA.jpg"), (140, 140))
        btn = pygame.Rect(WIDTH/2 -175, 480, 350, 70)
        click = False
        play = font.render("PLAY", 1, (153, 204, 255))
        while run:
            self.win.fill((255, 255, 255))
            self.win.blit(title, (WIDTH/2 - title.get_width()/2, 20))
            self.win.blit(heart, (615, 13))
            self.win.blit(OPA, (490, 130))
            self.win.blit(play, (WIDTH/2 -120, 480))
            pygame.draw.rect(self.win, (0, 0, 0), btn, 6)
            mx, my = pygame.mouse.get_pos() 
            if btn.collidepoint(mx, my):
                click = True
            
            # Create button 
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if click:
                        run = False
            
            pygame.display.update()
            
        self.main()
            
            
    def new(self):
        self.all_sprites = pygame.sprite.Group() 
        self.walls = pygame.sprite.Group() 
        self.door = pygame.sprite.Group()
        self.pencils = []
        '''
        # open the map 
        y = 0
        for row in self.CAM.game_map:
            x = 0
            for tile in row:
                if tile == "P":
                    self.player = player(x, y, self)
                if tile == "1":         
                    wall(x, y, self)
                x += 1
            y += 1
            
        
        for row, tiles in enumerate(CAM.game_map):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = player(x, y, self)
                if tile == "1":
                    wall(x, y, self)
            
        
            '''
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "wall":
                wall(tile_object.x, tile_object.y,tile_object.width, tile_object.height, self)
            if tile_object.name == "player":
                self.player = player(tile_object.x, tile_object.y, self)
            if tile_object.name == "door":
                self.door = door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            
            if tile_object.name == "pencil":
                self.pencil = pencil(self, tile_object.x, tile_object.y)
                self.pencils.append(self.pencil)
            
            
        
    def update(self):
        self.all_sprites.update() 
        self.door.update()
        self.camera.update(self.player)
    
    def draw_info(self):
        font = pygame.font.SysFont("aerial", 80)
        text = font.render(f"PENCILS: {self.player.pencil}", 1, (0, 0, 0))
        self.win.blit(text, (WIDTH/2-text.get_width(), 20))
    
    def draw(self):
        self.win.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        self.draw_info()
        for sprite in self.all_sprites:
            self.win.blit(sprite.image, self.camera.apply(sprite))
        
        pygame.display.update() 
    
    def run(self):
        self.game = True
        while self.game:
            self.dt = self.clock.tick(self.FPS)/1000
            self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.check_win():
                self.change_phase("YOU WON !", (255, 153, 102), (153, 255, 204))
            
            self.clock.tick(self.FPS)
            self.draw()
    
    def main(self):
        while True:
            self.new()
            self.run()

# Game loop
game = Game()
game.menu()