import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        
    def ray_cast(self):
        pos = self.game.player.pos
        map_pos = self.game.player.map_pos
        
        for cross in reversed(range(CROSS)):
            hor_ray_angle = self.game.player.hor_angle - HALF_HORIZONTAL_FOV + 0.00001
            for hor_ray in range(HORIZONTAL_NUM_OF_RAYS):
                pz, px, py = pos
                z_map, x_map, y_map = map_pos
                
                sin_a = math.sin(hor_ray_angle)
                cos_a = math.cos(hor_ray_angle)

                # horizontal
                y_hor, dy = (y_map + 1, 1) if (sin_a > 0) else (y_map - 1e-6, -1)
                depth_hor = (y_hor - py) / sin_a
                x_hor = px + depth_hor * cos_a
                
                delta_depth = dy / sin_a
                dx = delta_depth * cos_a
                for i in range(MAX_DEPTH):
                    tile_hor = int(cross), int(x_hor), int(y_hor)
                    if (tile_hor in self.game.map.world_map):
                        break
                    
                    x_hor += dx
                    y_hor += dy
                    depth_hor += delta_depth
                
                # vertical
                x_vert, dx = (x_map + 1, 1) if (cos_a) > 0 else (x_map - 1e-6, -1)
                depth_vert = (x_vert - px) / cos_a
                y_vert = py + depth_vert * sin_a
                
                delta_depth = dx / cos_a
                dy = delta_depth * sin_a
                for i in range(MAX_DEPTH):
                    tile_vert = int(cross), int(x_vert), int(y_vert)
                    if (tile_vert in self.game.map.world_map):
                        break
                    
                    x_vert += dx
                    y_vert += dy
                    depth_vert += delta_depth
                
                # depth
                depth = min(depth_hor, depth_vert)
                
                # remove fishbowl effect
                depth = math.sqrt(depth ** 2 + (cross + 1 - pz) ** 2)
                
                depth *= math.cos(self.game.player.hor_angle - hor_ray_angle)
                
                # projection
                screen_dist = math.sqrt(SCREEN_DIST ** 2 + (cross + 1 - pz) ** 2)
                proj_height = screen_dist / (depth + 0.00001)
                
                # draw walls
                color = [255 / (1 + depth ** 5 * 0.00002)] * 3
                top = HALF_HEIGHT - proj_height // 2
                if (cross == 1):
                    top -= proj_height
                if (cross == 2):
                    top -= proj_height * 2
                
                pg.draw.rect(self.game.screen, color, 
                            (hor_ray * SCALE, top, SCALE, proj_height))
                
                hor_ray_angle += HORIZONTAL_DELTA_ANGLE

    
    def update(self):
        self.ray_cast()