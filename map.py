import pygame as pg
from settings import *




class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()
        
    def get_map(self):
        for d, level in enumerate(self.mini_map):
            for j, row in enumerate(level):
                for i, value in enumerate(row):
                    if value:
                        self.world_map[(d, i, j)] = value

                    
    def draw(self):
        for z, x, y in self.world_map:
            color = "darkgray" if z == 0 else "white"
            pg.draw.rect(self.game.screen, color, (x * WALL_PIXELS, y * WALL_PIXELS, WALL_PIXELS, WALL_PIXELS), 2)