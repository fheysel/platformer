import pygame
from constants import *
from Platform import Platform, MovingPlatform


class Player(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
 
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # Level player is in
        self.level = None

        # Set players health
        self.health = 3
        self.safe_time = 0

        # Bools to store whether a second jump or boost is available
        self.double_jump = True

        # The player's ability to boost and how much time remains in the boost
        self.boostable = True
        self.boost_level = 0

    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Decrease safe time
        self.safe_time -= 1

        ### Horizontal Movement
        self.rect.x += self.change_x
 
        # Horizontal object collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.avoid_object_x(block)

        # Horizontal enemy collision
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if self.safe_time < 0:
            if len(enemy_hit_list) > 0:
                self.safe_time = 100
            for enemy in enemy_hit_list:
                self.health -= 1
                #  self.avoid_object_x(enemy)
        else:
            # TODO Flash character sprite
            pass

        ### Verticle Movement
        self.rect.y += self.change_y
 
        # Verticle object collision
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.avoid_object_y(block)
            self.change_y = 0
 
            # Move with moving blocks
            if isinstance(block, MovingPlatform): 
                self.rect.x += block.change_x
        
        # Verticle enemy collision
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False)
        if self.safe_time < 0:
            if len(enemy_hit_list) > 0:
                self.safe_time = 300
            for enemy in enemy_hit_list:
                self.health -= 1
                #  self.avoid_object_y(enemy)
        
 
        # If dead restart level
        if self.health <= 0:
            print("DIE MOTHER FUCKERRRRR") 
            self.safe_time = -1
            self.double_jump = True
            self.boostable = True
            self.boost_level = 0
            return  
        
        if self.boost_level > 0:
            self.boost_level -= 1
        else:
            if self.boostable is False:
                # when boost runs out reset speed and boostable flag
                self.boostable = True
                self.change_x = direction(self.change_x) * PLAYER_SPEED
        

    def avoid_object_x(self, obj):
        # If we are moving right,
        # set our right side to the left side of the item we hit
        if self.change_x > 0:
            self.rect.right = obj.rect.left
        elif self.change_x < 0:
            # Otherwise if we are moving left, do the opposite.
            self.rect.left = obj.rect.right

    def avoid_object_y(self, obj):
        # Reset our position based on the top/bottom of the object.
        if self.change_y > 0:
            self.rect.bottom = obj.rect.top
            if isinstance(obj, Platform): 
                self.double_jump = True
        elif self.change_y < 0:
            self.rect.top = obj.rect.bottom

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.double_jump = True
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    # def restart_level(self):
    #     self.health = 3
    #     self.rect.x = self.level.level_start[0]
    #     self.rect.y = self.level.level_start[1]
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -PLAYER_SPEED
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = PLAYER_SPEED
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it on ground or if double jump hasnt been used, set Players speed upwards
        if (len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT):
            self.change_y = -10
        elif self.double_jump == True:
            self.double_jump = False
            self.change_y = -10

    def boost(self):
        """ Called when the user hits 'boost' button. """
        if self.change_x == 0: # If not already moving dont boost
            return 

        if self.boostable == True and self.boost_level <= 0:
            self.boostable = False 
            self.boost_level = 10
        else:
            return

        direction = self.change_x / abs(self.change_x) 
        self.change_x = direction * PLAYER_SPEED * 2


# Helper functions
def direction(x):
    if x == 0:
        return 0
    return x / abs(x)