"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
From:
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
 
Explanation video: http://youtu.be/YKdOD5VkY48
 
Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""
import time
import pygame

from constants import *
from Player import Player
from levels.Level_01 import Level_01
from levels.Level_02 import Level_02
 
 
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    # Name the window
    pygame.display.set_caption("Platformer with moving platforms")

    # Create a font object (font, size)
    font = pygame.font.Font('freesansbold.ttf', 32) 

    # Create the player
    player = Player()

    # Create player health bar 
    health_bar = font.render(str(player.health), True, WHITE, BLACK)
    health_bar_visual = health_bar.get_rect()
    health_bar_visual.center = (20 , 20)

 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
 
    # Set up the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = current_level.level_start[0]
    player.rect.y = current_level.level_start[1]
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # KEYBOARD INTERRUPTS
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: 
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right() 
                if event.key == pygame.K_SPACE:
                    player.jump()
                if event.key == pygame.K_LSHIFT:
                    player.boost()
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # if player health is zero restart level
        if player.health <= 0:
            player.health = 3
            current_level.__init__(player)
            you_died_animation()
            continue
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_end[0]: 
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.rect.x = current_level.level_start[0]
                player.rect.y = current_level.level_start[1]
                player.level = current_level
            else:
                # FIXME: Out of levels. This just exits the program.
                done = True
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        health_bar = font.render(str(player.health), True, WHITE, BLACK)
        screen.blit(health_bar, health_bar_visual)
    
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

def you_died_animation():
    font = pygame.font.Font('freesansbold.ttf', 32) 
    text = font.render("YOU DIED", True, RED, BLACK)
    text_box = text.get_rect()
    text_box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    time.sleep(3)

    

 
if __name__ == "__main__":
    main()
