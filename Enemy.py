import pygame
from constants import *


class Enemy(pygame.sprite.Sprite):
    """ Enemy Duh DUh DUUUUHHHH"""
 
    def __init__(self, width, height):
        """ Enemy. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(RED)
 
        self.rect = self.image.get_rect()
 
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the enemy.
            If the player is in the way, the player will restart the level """
 
        # Move left/right up/down
        self.rect.x += self.change_x
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Restart the level
            self.player.rect.x = 120
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
