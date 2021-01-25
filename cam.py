from constants import *
import pygame
import pytmx


class MAP():
    def __init__(self, filename):
        with open (filename, 'r') as f:
            self.game_map = []
            for i in f:
                self.game_map.append(i.strip())
        
        self.height = len(self.game_map) * TILESIZE 
        self.width = len(self.game_map[0]) * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
    
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid 
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth, y*self.tmxdata.tileheight))
    
    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
            

class Camera():
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)
    
    def apply(self, sprite):
        return sprite.rect.move(self.camera.topleft)
    
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        x = - target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        x = min(0,x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height-HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)