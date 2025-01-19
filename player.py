import pygame as pg
from settings import *
from utils.vector import Vector
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.z, self.x, self.y = PLAYER_POS
        self.hor_angle = PLAYER_HORZONTAL_ANGLE
        self.ver_angle = PLAYER_VERTIAL_ANGLE
    
    def movement(self):
        sin_a = math.sin(self.hor_angle)
        cos_a = math.cos(self.hor_angle)
        
        movement_vector = Vector(0, 0)

        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        forward = (speed_cos, speed_sin)
        backward = (-speed_cos, -speed_sin)
        left = (speed_sin, -speed_cos)
        right = (-speed_sin, speed_cos)
        
        
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            forward_vector = Vector(forward[0], forward[1])
            movement_vector = movement_vector + forward_vector
        if keys[pg.K_s]:
            backward_vector = Vector(backward[0], backward[1])
            movement_vector = movement_vector + backward_vector
        if keys[pg.K_a]:
            left_vector = Vector(left[0], left[1])
            movement_vector = movement_vector + left_vector
        if keys[pg.K_d]:
            right_vector = Vector(right[0], right[1])
            movement_vector = movement_vector + right_vector
        
        self.check_wall_collision(movement_vector.x, movement_vector.y)
        
        if keys[pg.K_LEFT]:
            self.hor_angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.hor_angle += PLAYER_ROT_SPEED * self.game.delta_time
            
        if keys[pg.K_UP]:
            if (self.ver_angle - PLAYER_ROT_SPEED * self.game.delta_time > MIN_VER_ANGLE):
                self.ver_angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_DOWN]:
            if (self.ver_angle + PLAYER_ROT_SPEED * self.game.delta_time < MAX_VER_ANGLE):
                self.ver_angle += PLAYER_ROT_SPEED * self.game.delta_time
                
        self.hor_angle %= math.tau
    
    def check_wall(self, z, x, y):
        return (z, x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        if (self.check_wall(int(self.z), int(self.x + dx), int(self.y))):
            self.x += dx
        if (self.check_wall(int(self.z), int(self.x), int(self.y + dy))):
            self.y += dy
        
    def draw(self):
        pg.draw.line(self.game.screen, "yellow", (self.x * WALL_PIXELS, self.y * WALL_PIXELS), 
                    (self.x * WALL_PIXELS + WIDTH * math.cos(self.hor_angle), self.y * WALL_PIXELS + WIDTH * math.sin(self.hor_angle)), 2)
        pg.draw.circle(self.game.screen, "green", (self.x * WALL_PIXELS, self.y * WALL_PIXELS), 15)

    def update(self):
        self.movement()
        
    @property
    def pos(self):
        return self.z, self.x, self.y

    @property
    def map_pos(self):
        return int(self.z), int(self.x), int(self.y)