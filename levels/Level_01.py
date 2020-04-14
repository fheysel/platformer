from Level import Level
from Platform import Platform, MovingPlatform
from Enemy import Enemy
 
 
BLOCK_WIDTH = 210 
BLOCK_HEIGHT = 70


class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        self.level_limit = -6000
        BLOCK_WIDTH = 210
        self.block_height = 70
        # Array with width, height, x, and y of platform
        level = [[BLOCK_WIDTH, BLOCK_HEIGHT, 500, 500],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 800, 400],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 1000, 500],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 1120, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 1500, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 2000, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 2500, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 3000, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 3500, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 4000, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 4500, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 5000, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 5500, 280],
                 [BLOCK_WIDTH, BLOCK_HEIGHT, 60000, 280],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
        # Add a custom moving platform
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom enemy
        enemy =  Enemy(30, 30)
        enemy.rect.x = 900
        enemy.rect.y = 300
        enemy.boundary_left = 800
        enemy.boundary_right = 1000
        enemy.change_x = 1
        enemy.player = self.player
        enemy.level = self
        self.enemy_list.add(enemy)

