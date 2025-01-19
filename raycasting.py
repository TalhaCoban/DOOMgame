import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
        
    def get_objects_to_render(self):
        self.objects_to_render = []
        max_ray = len(self.ray_casting_result) / CROSS
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset, top = values
            wall_column = self.textures[texture].subsurface(
                offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
            )
            ray %= max_ray
            wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, top)
            self.objects_to_render.append((depth, wall_column, wall_pos))
        
    def ray_cast(self):
        self.ray_casting_result = []
        pos = self.game.player.pos
        map_pos = self.game.player.map_pos
        
        for cross in reversed(range(CROSS)):
            texture_hor, texture_vert = 1, 1
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
                        texture_hor = self.game.map.world_map[tile_hor]
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
                        texture_vert = self.game.map.world_map[tile_vert]
                        break
                    
                    x_vert += dx
                    y_vert += dy
                    depth_vert += delta_depth
                
                # depth, texture
                if depth_vert < depth_hor:
                    depth, texture = depth_vert, texture_vert
                    y_vert %= 1
                    offset = y_vert if cos_a > 0 else (1 - y_vert)
                else:
                    depth, texture = depth_hor, texture_hor
                    x_hor %= 1
                    offset = (1 - x_hor) if sin_a > 0 else x_hor
                
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
                    top -= proj_height - 2
                if (cross == 2):
                    top -= proj_height * 2 - 2
                
                # pg.draw.rect(self.game.screen, color, 
                #             (hor_ray * SCALE, top, SCALE, proj_height))
                
                # ray casting result
                self.ray_casting_result.append((depth, proj_height, texture, offset, top))
                
                hor_ray_angle += HORIZONTAL_DELTA_ANGLE

        
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()