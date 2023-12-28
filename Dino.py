# Example file showing a circle moving on screen
import pygame
from random import randint
# pygame setup
pygame.init()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound('sounds/jump.mp3') 
fire_sound = pygame.mixer.Sound('sounds/shoot.mp3')
explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')
pygame.mixer.music.load('sounds/game_over_effect.wav')
pygame.mixer.music.set_volume(0.5)


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
GRAVITY = 1.5
line_color = (230, 190, 190)
start_point = (0, 580)  # (x, y)
end_point = (1280, 580)
line_thickness = 1
is_jumping=False
jump_height = -26
range=1
groud_level = 580
passed_hurdle = False
collided_hurdle = False
ORANGE = (255, 165, 0)
shoot_fireball = False
fb = None
obj_destroyed = False


class Hurdles():
    def __init__(self, size, speed) -> None:
        self.size = size
        self.speed = speed
        self.left = 1600
        self.width = 5*self.size
        self.height = 7*self.size
        self.top = 580-self.height
    def draw(self):
        pygame.draw.rect(screen, (211,211,211), (self.left, self.top, self.width, self.height))
    def update_pos(self):
        self.left-=self.speed
    def erase_hurdle(self):
        self.left = -80
    def get_dimensions(self):
        return (self.left, self.top, self.width, self.height)


class FireBall():
    def __init__(self, xpos, ypos) -> None:
        self.size = 15
        self.xpos = xpos
        self.ypos = ypos
        self.speed = randint(10, 15)
    def draw(self):
        pygame.draw.circle(screen, ORANGE, (self.xpos, self.ypos), self.size)
    def update_pos(self):
        self.xpos += self.speed
    def get_dimensions(self):
        return (self.xpos, self.ypos, self.size)



player_pos = pygame.Rect(screen.get_width() / 2 - 200, groud_level-40, 40, 40)
inital_x = player_pos.x
obj_list = [Hurdles(randint(10,15), randint(10,14))]
obj = obj_list.pop()
# game_over = False
score = 0
max_score=0
def reset_game():
    global player_pos, score
    score=0
    pygame.mixer.music.play() 
    return (player_pos, score)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    font = pygame.font.Font('freesansbold.ttf', 22)
    text_score = font.render(f'Score: {str(score)}', True, (220,220,220), (110,110,110))
    text_score_max = font.render(f'Max Score: {str(max_score)}', True, (220,220,220), (110,110,110))
    screen.blit(text_score, (1100,50))
    screen.blit(text_score_max, (1100,70))
    
    pygame.draw.line(screen, line_color, start_point, end_point, line_thickness)
    pygame.draw.rect(screen, (211,211,211), player_pos)

    if obj_destroyed:
       score+=10
       explosion_sound.play()
       obj.erase_hurdle()
       obj.draw()
       obj.update_pos()
       obj_destroyed = False
       
    
    if obj is not None:
        if obj.left==1600:
            obj.draw()
            obj.update_pos()
        elif obj.left<=-80:    
            obj_list.append(Hurdles(randint(10,15), randint(10,14)))
            obj = obj_list.pop()
            collided_hurdle = False
        else:
            obj.draw()
            obj.update_pos()
    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping=True
        jump_sound.play()
        vertical_vel = jump_height
        horizontal_vel = range
        # player_pos.y -= 1000 * dt
    elif not keys[pygame.K_SPACE] and not is_jumping:
        if player_pos.x<=inital_x:
            pass
        else:
            player_pos.x -= 3
    
    if is_jumping:
        player_pos.y+=vertical_vel
        player_pos.x+=horizontal_vel
        vertical_vel += GRAVITY

        if player_pos.colliderect(obj.get_dimensions()):
            if max_score<=score:
                max_score = score
            player_pos, score = reset_game()
            collided_hurdle = True
        
         # Check if the player has passed the hurdle
        elif not collided_hurdle and not passed_hurdle and player_pos.x > obj.left + obj.width:
            passed_hurdle = True
            score += 10
        
        if player_pos.y >= groud_level-40:
            player_pos.y = groud_level-40
            # if player_pos.x>temp:
            #     player_pos.x -= range
            is_jumping = False
            # score+=10
            vertical_vel = 0
            horizontal_vel = 0
    
    # Reset passed_hurdle flag when the player is behind the hurdle
    if player_pos.x < obj.left:
        passed_hurdle = False
    
    if player_pos.colliderect(obj.get_dimensions()):
        if max_score<=score:
            max_score = score
        collided_hurdle = True
        player_pos, score = reset_game()

    if (score!=0 and score % 30 == 0) or fb is not None:
        mfont = pygame.font.Font(None, 36)
        message_color = (255, 255, 255)  
        message = font.render("You've earned a fireball! Press 'F' to shoot", True, message_color)
        message_rect = message.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(message, message_rect)
        if fb is None and not is_jumping:
            fb = FireBall(player_pos.centerx, player_pos.centery)


        new_key = pygame.key.get_pressed()
        if new_key[pygame.K_f] and not shoot_fireball and player_pos.x < obj.left:
            shoot_fireball = True
            fire_sound.play()
            # fb = FireBall(player_pos.centerx, player_pos.centery)
        if fb is not None and shoot_fireball:
            fb.draw()
            if fb.xpos + 8 < obj.left:
                fb.update_pos()
            else:
                fb = None
                shoot_fireball = False
                obj_destroyed = True
                
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()